"""Aturan validasi Gold dan rekonsiliasi (Sprint 2), berlaku untuk semua kasus.

Setiap aturan = (nama, keterangan, keras, fungsi(silver, gold) -> DataFrame baris yang melanggar).
Aturan keras menghentikan pipeline bila ada baris yang melanggar. Diuji dengan Gold yang sengaja dirusak
di tests/test_gold.py.
"""
import pandas as pd

from src.gold.rekonsiliasi import KATEGORI
from src.silver.deret import JUMLAH

STATUS = {"terisi", "missing", "tidak_diterbitkan", "belum_ada", "batas_lama"}
KUNCI_PANEL = ["indikator", "wilayah_kode", "periode"]


def kunci_panel_unik(silver, gold):
    p = gold["panel"]
    return p[p.duplicated(KUNCI_PANEL, keep=False)]


def satu_satuan_per_indikator(silver, gold):
    p = gold["panel"]
    n = p.groupby("indikator")["satuan"].nunique()
    return p[p["indikator"].isin(n[n != 1].index) | p["satuan"].isna()]


def status_dan_nilai(silver, gold):
    p = gold["panel"]
    return p[~p["status_sel"].isin(STATUS) | ((p["status_sel"] == "terisi") != p["nilai"].notna())]


def tertelusur_ke_silver(silver, gold):
    """Setiap sel terisi punya baris Silver dengan seri, wilayah, periode, dan berkas yang sama (dan rincian yang
    sama, kecuali deret JUMLAH yang merupakan jumlah rincian satu berkas)."""
    p = gold["panel"]
    p = p[p["status_sel"] == "terisi"]
    s = silver[["seri_kode", "wilayah_kode", "periode", "rincian", "_berkas_raw", "nilai"]]
    biasa = p[p["rincian"] != JUMLAH].merge(s, on=["seri_kode", "wilayah_kode", "periode", "rincian", "_berkas_raw"],
                                            how="left", suffixes=("", "_silver"), indicator=True)
    jml = p[p["rincian"] == JUMLAH].merge(
        s.drop(columns=["rincian", "nilai"]).drop_duplicates(), on=["seri_kode", "wilayah_kode", "periode", "_berkas_raw"],
        how="left", indicator=True)
    buruk = pd.concat([biasa[biasa["_merge"] != "both"], jml[jml["_merge"] != "both"]])
    return buruk.drop(columns="_merge")


def nilai_sama_dengan_silver(silver, gold):
    p = gold["panel"]
    p = p[(p["status_sel"] == "terisi") & (p["rincian"] != JUMLAH)]
    m = p.merge(silver[["seri_kode", "wilayah_kode", "periode", "rincian", "_berkas_raw", "nilai"]],
                on=["seri_kode", "wilayah_kode", "periode", "rincian", "_berkas_raw"], suffixes=("", "_silver"))
    return m[(m["nilai"] - m["nilai_silver"]).abs() > 1e-9]


def nasional_unik(silver, gold):
    n = gold["nasional"]
    return n[n.duplicated(["seri_kode", "rincian", "periode"], keep=False)]


def kategori_baku(silver, gold):
    r = gold["rekonsiliasi"]
    return r[~r["kategori"].isin(KATEGORI) | r["penjelasan"].isna() | (r["penjelasan"].str.strip() == "")]


def selisih_konsisten(silver, gold):
    r = gold["rekonsiliasi"]
    h = r[r["selisih"].notna()]
    return h[(h["selisih"] - (h["nilai_utama"] - h["nilai_pembanding"])).abs() > 1e-6]


def berpasangan_dihitung(silver, gold):
    """Pasangan berjenis selisih: baris yang kedua nilainya ada harus punya selisih, kecuali tahun proyeksi
    atau satuan tanpa faktor konversi (dicatat di kolom catatan)."""
    r = gold["rekonsiliasi"]
    return r[(r["jenis"] == "selisih") & (r["asal"] == "keduanya") & r["selisih"].isna() & r["catatan"].isna()]


def periode_utama_tampil(silver, gold):
    """Setiap periode seri utama (sesudah pemetaan periode yang sama dengan rekonsiliasi) muncul di tabel
    rekonsiliasi untuk setiap pembandingnya: gabung luar, tidak ada periode utama yang dibuang."""
    from src import konfigurasi as K
    from src.gold.rekonsiliasi import daftar_pembanding, sisi_utama

    r, n = gold["rekonsiliasi"], gold["nasional"]
    hilang = []
    for p in K.PASANGAN:
        utama = p["utama"].split(",")[0].strip()
        ada = set(sisi_utama(n, p)["periode"])
        for seri_b, *_ in daftar_pembanding(n, p, None):
            tampil = set(r.loc[(r["pasangan_id"] == p["id"]) & (r["seri_pembanding"] == seri_b), "periode"])
            hilang += [{"pasangan_id": p["id"], "seri_pembanding": seri_b, "periode": x} for x in sorted(ada - tampil)]
    return pd.DataFrame(hilang)


ATURAN = [
    ("gold: kunci panel unik", "indikator + wilayah_kode + periode tidak kembar", True, kunci_panel_unik),
    ("gold: satu satuan per indikator", "satu indikator panel hanya punya satu satuan", True, satu_satuan_per_indikator),
    ("gold: status sel dan nilai", "status sel baku; nilai ada jika dan hanya jika sel terisi", True, status_dan_nilai),
    ("gold: sel tertelusur ke Silver", "setiap sel terisi punya baris Silver asal (seri, wilayah, periode, berkas)",
     True, tertelusur_ke_silver),
    ("gold: nilai sama dengan Silver", "nilai panel = nilai Silver asalnya (tidak ada nilai yang diubah di Gold)",
     True, nilai_sama_dengan_silver),
    ("gold: tabel nasional unik", "seri + rincian + periode tidak kembar", True, nasional_unik),
    ("rekonsiliasi: kategori baku", "kategori dari daftar baku; penjelasan tidak kosong", True, kategori_baku),
    ("rekonsiliasi: selisih = utama − pembanding", "selisih dihitung ulang dan cocok", True, selisih_konsisten),
    ("rekonsiliasi: baris berpasangan dihitung", "pasangan selisih dengan dua nilai punya selisih, atau catatan mengapa "
     "tidak", True, berpasangan_dihitung),
    ("rekonsiliasi: periode utama tidak dibuang", "setiap tahun seri utama di tabel nasional muncul di rekonsiliasi",
     True, periode_utama_tampil),
]
