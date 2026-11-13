"""Tahap 1 — Ekstraksi (Milik tim).

Membaca seluruh 58 berkas di data/raw/ kasus 23 menjadi DataFrame mentah yang setia pada sumbernya:
1. 15 berkas XLSX BNPB di tangan/ (multi-level header, matriks spasial, rekapitulasi)
2. 38 berkas JSON CKAN Datastore BNPB di datastore/ (paginasi dan rincian transaksi/agregat)
3. 1 berkas metadata CKAN BNPB di ckan/ (katalog dataset dan metadata resource)
4. 4 berkas JSON WDI Bank Dunia di wdi/ (data observasi dan metadata indikator)

Setiap baris membawa kolom lineage `_berkas_raw` dan `_sha256_raw` dari `src.common.manifest`.
"""
from src.ekstraksi.baca_datastore import (
    baca_berkas_datastore,
    baca_metadata_ckan,
    baca_semua_datastore,
)
from src.ekstraksi.baca_wdi import baca_semua_wdi, baca_wdi_data
from src.ekstraksi.baca_xlsx import baca_berkas_xlsx, baca_semua_xlsx

__all__ = [
    "baca_berkas_xlsx",
    "baca_semua_xlsx",
    "baca_berkas_datastore",
    "baca_semua_datastore",
    "baca_metadata_ckan",
    "baca_wdi_data",
    "baca_semua_wdi",
    "jalankan",
]


def jalankan():
    """Kembalikan {nama_sumber: data mentah} untuk seluruh berkas kasus 23."""
    return {
        "bnpb_xlsx": baca_semua_xlsx(),
        "bnpb_datastore": baca_semua_datastore(),
        "bnpb_ckan": baca_metadata_ckan(),
        "wdi": baca_semua_wdi(),
    }
