"""Tahap 1 — Ekstraksi (pertemuan X). Milik tim.

Baca setiap berkas di data/raw/ (CSV, JSON WebAPI BPS, XLSX BNPB, SDMX ILO, JSON WDI) menjadi
DataFrame mentah yang setia pada sumbernya: jangan membersihkan di sini, cukup ratakan struktur
dan catat asal tiap baris (`_berkas_raw` relatif data/raw/, `_sha256_raw` dari src.common.manifest).
"""


from .bnpb_json import (
    baca_metadata_ckan,
    baca_berkas_datastore,
    baca_semua_datastore,
    rekap_bnpb_json,
)

__all__ = [
    "baca_metadata_ckan",
    "baca_berkas_datastore",
    "baca_semua_datastore",
    "rekap_bnpb_json",
    "jalankan",
]


def jalankan():
    """Kembalikan {nama_sumber: DataFrame mentah}."""
    # Menyediakan hasil pembacaan JSON BNPB (CKAN & Datastore)
    ckan = baca_metadata_ckan()
    datastore = baca_semua_datastore()
    return {
        "bnpb_ckan": ckan,
        "bnpb_datastore": datastore,
    }
