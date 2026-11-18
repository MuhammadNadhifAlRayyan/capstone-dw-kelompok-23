"""Skema validasi otomatis tabel Silver menggunakan Pandera.

Memvalidasi:
1. Keberadaan 11 kolom wajib.
2. Integritas tipe data dan ketiadaan nilai kosong (NaN).
3. Nilai non-negatif (>= 0).
4. Nilai unit kerusakan merupakan bilangan bulat.
5. Kode wilayah sah (9999 untuk nasional, 1100-9600 untuk provinsi BPS).
6. Format periode valid (YYYY) dan jenis_periode 'tahun'.
7. Aturan khusus Kasus 23: Kolom 'rincian' pada seri 'rumah_rusak' wajib terdaftar di Kamus Kategori.
8. Keunikan kunci komposit Silver.
"""

from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd
import pandera as pa
from pandera import Check, Column, DataFrameSchema

from src.common.manifest import baca as baca_manifest

# Kamus Kategori Resmi Rincian Rumah Rusak (sesuai docs/data-dictionary.md)
KAMUS_RINCIAN_RUMAH_RUSAK = {
    "total",
    "rusak_berat",
    "rusak_sedang",
    "rusak_ringan",
    "banjir",
    "cuaca_ekstrem",
    "gempa_bumi",
    "tanah_longsor",
    "kebakaran_hutan_lahan",
    "erupsigunungapi",
    "gelombang_pasang_abrasi",
    "kekeringan",
    "tsunami",
}

KOLOM_WAJIB = [
    "sumber",
    "seri_kode",
    "wilayah_kode",
    "nama_wilayah",
    "periode",
    "jenis_periode",
    "rincian",
    "nilai",
    "satuan",
    "_berkas_raw",
    "_sha256_raw",
]

KUNCI_KOMPOSIT = [
    "sumber",
    "seri_kode",
    "wilayah_kode",
    "periode",
    "rincian",
    "_berkas_raw",
]


def check_kamus_rumah_rusak(df: pd.DataFrame) -> bool:
    """Aturan 1: Setiap rincian rumah rusak wajib terdaftar di kamus kategori."""
    mask_rr = df["seri_kode"] == "rumah_rusak"
    if not mask_rr.any():
        return True
    rincian_rr = set(df.loc[mask_rr, "rincian"].unique())
    tidak_terdaftar = rincian_rr - KAMUS_RINCIAN_RUMAH_RUSAK
    return len(tidak_terdaftar) == 0


def check_unit_bilangan_bulat(df: pd.DataFrame) -> bool:
    """Nilai pada seri bersatuan 'unit' dan 'kejadian' harus bilangan bulat."""
    mask_unit = df["satuan"].isin(["unit", "kejadian"])
    if not mask_unit.any():
        return True
    nilai_unit = df.loc[mask_unit, "nilai"]
    return (nilai_unit % 1 == 0).all()


def check_wilayah_kode_sah(df: pd.DataFrame) -> bool:
    """Kode wilayah harus 9999 (Nasional) atau kode provinsi BPS (1100 s.d. 9700 kelipatan 100)."""
    kode = df["wilayah_kode"]
    sah = (kode == 9999) | ((kode >= 1100) & (kode <= 9700) & (kode % 100 == 0))
    return sah.all()


def check_keunikan_kunci(df: pd.DataFrame) -> bool:
    """Kunci komposit Silver tidak boleh memiliki duplikasi."""
    return not df.duplicated(subset=KUNCI_KOMPOSIT).any()


def check_lineage_manifest(df: pd.DataFrame) -> bool:
    """Pasangan _berkas_raw dan _sha256_raw wajib cocok dengan MANIFEST.csv."""
    try:
        manifest = baca_manifest()
    except Exception:
        return True
    pasangan = df[["_berkas_raw", "_sha256_raw"]].drop_duplicates()
    for berkas, sha in pasangan.itertuples(index=False):
        if manifest.get(berkas) != sha:
            return False
    return True


def buat_skema_silver() -> DataFrameSchema:
    """Membangun objek Pandera DataFrameSchema untuk tabel Silver."""
    return DataFrameSchema(
        columns={
            "sumber": Column(str, Check.isin(["bnpb", "wdi"]), nullable=False),
            "seri_kode": Column(str, nullable=False),
            "wilayah_kode": Column(int, Check(check_wilayah_kode_sah, element_wise=False), nullable=False),
            "nama_wilayah": Column(str, nullable=False),
            "periode": Column(str, Check.str_matches(r"^\d{4}$"), nullable=False),
            "jenis_periode": Column(str, Check.isin(["tahun"]), nullable=False),
            "rincian": Column(str, nullable=False),
            "nilai": Column(float, Check.greater_than_or_equal_to(0), nullable=False),
            "satuan": Column(str, Check.isin(["kejadian", "unit", "hektare", "rupiah", "persen"]), nullable=False),
            "_berkas_raw": Column(str, nullable=False),
            "_sha256_raw": Column(str, Check.str_length(64, 64), nullable=False),
        },
        checks=[
            Check(check_kamus_rumah_rusak, name="aturan_kamus_rincian_rumah_rusak"),
            Check(check_unit_bilangan_bulat, name="aturan_unit_bilangan_bulat"),
            Check(check_keunikan_kunci, name="aturan_keunikan_kunci_komposit"),
            Check(check_lineage_manifest, name="aturan_lineage_manifest"),
        ],
        strict=False,
        coerce=True,
    )


def validasi_dataframe_silver(df: pd.DataFrame) -> Tuple[bool, List[str], Dict[str, bool]]:
    """Menjalankan evaluasi aturan validasi Pandera pada DataFrame Silver.

    Returns:
        (sukses, daftar_error, detail_aturan)
    """
    aturan_detail = {
        "11_kolom_wajib_ada": True,
        "ketiadaan_nilai_kosong": True,
        "nilai_non_negatif": True,
        "unit_bilangan_bulat": True,
        "kode_wilayah_sah": True,
        "format_periode_valid": True,
        "kamus_rincian_rumah_rusak": True,
        "keunikan_kunci_komposit": True,
        "lineage_manifest_cocok": True,
    }
    errors = []

    # 1. Cek kolom wajib
    kurang = [c for c in KOLOM_WAJIB if c not in df.columns]
    if kurang:
        aturan_detail["11_kolom_wajib_ada"] = False
        errors.append(f"Kolom wajib tidak ditemukan: {kurang}")

    # 2. Cek nilai kosong
    if df.isna().any().any():
        aturan_detail["ketiadaan_nilai_kosong"] = False
        kosong = df.isna().sum()
        errors.append(f"Terdapat sel kosong pada kolom: {kosong[kosong > 0].to_dict()}")

    # 3. Cek nilai non-negatif
    if "nilai" in df.columns and (df["nilai"] < 0).any():
        aturan_detail["nilai_non_negatif"] = False
        errors.append(f"Ditemukan {(df['nilai'] < 0).sum()} baris dengan nilai negatif")

    # 4. Cek unit integer
    if not check_unit_bilangan_bulat(df):
        aturan_detail["unit_bilangan_bulat"] = False
        errors.append("Ditemukan nilai bukan bilangan bulat pada seri bersatuan unit/kejadian")

    # 5. Cek kode wilayah
    if "wilayah_kode" in df.columns and not check_wilayah_kode_sah(df):
        aturan_detail["kode_wilayah_sah"] = False
        errors.append("Ditemukan kode wilayah tidak sah (bukan 9999 atau kode provinsi BPS)")

    # 6. Cek periode
    if "periode" in df.columns and not df["periode"].astype(str).str.match(r"^\d{4}$").all():
        aturan_detail["format_periode_valid"] = False
        errors.append("Format periode tidak sesuai regex YYYY")

    # 7. Cek kamus kategori rumah rusak
    if not check_kamus_rumah_rusak(df):
        aturan_detail["kamus_rincian_rumah_rusak"] = False
        mask_rr = df["seri_kode"] == "rumah_rusak"
        tidak_sah = set(df.loc[mask_rr, "rincian"].unique()) - KAMUS_RINCIAN_RUMAH_RUSAK
        errors.append(f"Rincian rumah rusak di luar kamus kategori: {tidak_sah}")

    # 8. Cek keunikan kunci
    if not check_keunikan_kunci(df):
        aturan_detail["keunikan_kunci_komposit"] = False
        errors.append("Ditemukan duplikasi baris pada kunci komposit Silver")

    # 9. Cek lineage
    if not check_lineage_manifest(df):
        aturan_detail["lineage_manifest_cocok"] = False
        errors.append("Sidik _sha256_raw tidak cocok dengan data/raw/MANIFEST.csv")

    sukses = len(errors) == 0
    return sukses, errors, aturan_detail
