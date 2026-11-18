"""Aturan validasi khas Kasus 23 (panduan kelompok bagian 4.4), plus empat aturan peringatan.

Setiap fungsi menerima Silver dan mengembalikan baris yang melanggar (kosong = lolos). Berkas yang angkanya
dijumlahkan dari kab/kota dibaca dari reports/bnpb-agregasi.csv (ditulis src/silver/bangun.py).
"""
import pandas as pd

from src.laporan import ROOT

KUNCI = ["seri_kode", "wilayah_kode", "periode", "rincian"]
CACAH = {"kejadian", "rumah_rusak", "rumah_terendam", "fasyankes_rusak", "satuan_pendidikan_rusak", "jembatan_rusak",
         "kantor_rusak", "rumah_ibadat_rusak", "kios_toko_rusak", "pabrik_rusak"}
REKAP_NILAI = "fefc94c0-"      # Rekapitulasi Nilai Kerusakan dan Kerugian ... 2015–2024


def _bnpb(silver):
    return silver[silver["sumber"] == "bnpb"]


def berkas_kabkota():
    jalur = ROOT / "reports" / "bnpb-agregasi.csv"
    return set(pd.read_csv(jalur)["_berkas_raw"]) if jalur.exists() else set()


def cacah_bilangan_bulat(silver):
    """Jumlah kejadian dan unit rusak adalah bilangan bulat (galat titik mengambang rumus Excel sudah dibulatkan)."""
    b = _bnpb(silver)
    b = b[b["seri_kode"].isin(CACAH)]
    return b[b["nilai"] != b["nilai"].round()][KUNCI + ["nilai", "_berkas_raw"]]


def jenis_menjumlah_ke_total(silver):
    """Di berkas yang memuat baris Total dan baris per jenis, jumlah jenis = Total."""
    b = _bnpb(silver)
    k = ["seri_kode", "wilayah_kode", "periode", "_berkas_raw"]
    total = b[b["rincian"] == "total"].set_index(k)["nilai"].rename("total")
    jenis = b[b["rincian"].str.startswith("jenis_bencana=") & ~b["rincian"].str.contains(";")]
    jml = jenis.groupby(k)["nilai"].sum().rename("jumlah_jenis")
    g = pd.concat([total, jml], axis=1, join="inner")
    return g[(g["total"] - g["jumlah_jenis"]).abs() > 1e-9].reset_index()


def rumah_rusak_tingkat_sama_tabel_jenis(silver):
    """2025, Indonesia: berat + sedang + ringan (rekap nasional) = rumah rusak per jenis (tabel provinsi 2025)."""
    b = _bnpb(silver)
    r = b[(b["seri_kode"] == "rumah_rusak") & (b["periode"] == "2025") & (b["wilayah_kode"] == 9999)]
    rekap = r[r["_berkas_raw"].str.contains("rekapitulasi") & r["rincian"].str.contains("jenis_bencana=.*;", regex=True)]
    jml = rekap.assign(jenis=rekap["rincian"].str.split(";").str[0]).groupby("jenis")["nilai"].sum().rename("berat_sedang_ringan")
    tabel = r[r["_berkas_raw"].str.contains("rumah-rusak") & ~r["rincian"].str.contains(";")].set_index("rincian")["nilai"]
    g = pd.concat([jml, tabel.rename("tabel_per_jenis")], axis=1, join="inner")
    return g[g["berat_sedang_ringan"] != g["tabel_per_jenis"]].reset_index()


def _kab_vs_prov(silver):
    b = _bnpb(silver)
    kab = berkas_kabkota()
    a = b[b["_berkas_raw"].isin(kab)]
    p = b[~b["_berkas_raw"].isin(kab) & (b["wilayah_kode"] != 9999)]
    m = a.merge(p, on=KUNCI, suffixes=("_kabkota", "_provinsi"))
    m["selisih"] = m["nilai_kabkota"] - m["nilai_provinsi"]
    return m[KUNCI + ["nilai_kabkota", "nilai_provinsi", "selisih", "_berkas_raw_kabkota", "_berkas_raw_provinsi"]]


def kejadian_kabkota_tidak_kurang(silver):
    """Peringatan: kejadian hasil jumlah kab/kota < angka provinsi (kejadian lintas kab/kota dihitung di setiap
    kab/kota terdampak, jadi jumlah kab/kota boleh lebih besar, tidak boleh lebih kecil)."""
    m = _kab_vs_prov(silver)
    m = m[(m["seri_kode"] == "kejadian") & (m["selisih"] < 0)]
    return m.drop_duplicates(KUNCI + ["nilai_kabkota", "nilai_provinsi"])


def kerusakan_kabkota_sama_provinsi(silver):
    """Peringatan: unit rusak hasil jumlah kab/kota berbeda dari angka provinsi (satu rumah tidak dihitung dua kali)."""
    m = _kab_vs_prov(silver)
    m = m[(m["seri_kode"] != "kejadian") & (m["selisih"] != 0)]
    return m.drop_duplicates(KUNCI + ["nilai_kabkota", "nilai_provinsi"])


def indonesia_sama_lintas_berkas(silver):
    """Peringatan: baris Indonesia untuk seri, tahun, dan jenis yang sama berbeda antarberkas (berkas jumlahan
    kab/kota tidak ikut). Silver tidak diubah; berkas yang dipakai Gold diputuskan di Sprint 2."""
    b = _bnpb(silver)
    b = b[(b["wilayah_kode"] == 9999) & ~b["_berkas_raw"].isin(berkas_kabkota())]
    g = b.groupby(KUNCI)["nilai"].agg(["nunique", "min", "max", "size"])
    return g[g["nunique"] > 1].reset_index()


def nilai_rekap_sama_tabel_tahunan(silver):
    """Peringatan: nilai kerusakan/kerugian di rekapitulasi 2015–2024 berbeda dari tabel per tahun usulan untuk
    provinsi dan tahun kejadian yang sama (usulan tercatat dua kali, atau kab/kota yang berbeda di dua tabel)."""
    b = _bnpb(silver)
    n = b[b["seri_kode"].isin(["nilai_kerusakan", "nilai_kerugian"])]
    rekap = n[n["_berkas_raw"].str.contains(REKAP_NILAI)]
    tahun = n[~n["_berkas_raw"].str.contains(REKAP_NILAI)]
    m = rekap.merge(tahun, on=KUNCI, suffixes=("_rekap", "_tahunan"))
    return m[m["nilai_rekap"] != m["nilai_tahunan"]][KUNCI + ["nilai_rekap", "nilai_tahunan", "_berkas_raw_tahunan"]]


ATURAN = [
    ("cacah_bilangan_bulat", "kejadian dan unit rusak bilangan bulat", True, cacah_bilangan_bulat),
    ("jenis_menjumlah_ke_total", "jumlah per jenis = baris Total di berkas yang sama", True, jenis_menjumlah_ke_total),
    ("rumah_rusak_tingkat_sama_tabel_jenis", "2025: berat + sedang + ringan = rumah rusak per jenis", True,
     rumah_rusak_tingkat_sama_tabel_jenis),
    ("kejadian_kabkota_tidak_kurang", "kejadian jumlah kab/kota < provinsi (peringatan)", False, kejadian_kabkota_tidak_kurang),
    ("kerusakan_kabkota_sama_provinsi", "unit rusak jumlah kab/kota ≠ provinsi (peringatan)", False,
     kerusakan_kabkota_sama_provinsi),
    ("indonesia_sama_lintas_berkas", "baris Indonesia berbeda antarberkas (peringatan)", False, indonesia_sama_lintas_berkas),
    ("nilai_rekap_sama_tabel_tahunan", "nilai rekap 2015–2024 ≠ tabel per tahun (peringatan)", False,
     nilai_rekap_sama_tabel_tahunan),
]
