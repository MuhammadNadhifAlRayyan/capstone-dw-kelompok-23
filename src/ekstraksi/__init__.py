"""Tahap 1 — Ekstraksi. Milik tim.

Membaca setiap berkas di data/raw/ (XLSX BNPB tangan/, JSON datastore/, CKAN metadata, dan JSON WDI)
menjadi DataFrame mentah yang setia pada sumbernya: jangan membersihkan di sini, cukup ratakan struktur
dan catat asal tiap baris (`_berkas_raw` relatif data/raw/, `_sha256_raw` dari src.common.manifest).
"""
from src.ekstraksi.baca_xlsx import baca_berkas_xlsx, baca_semua_xlsx

__all__ = ["baca_berkas_xlsx", "baca_semua_xlsx", "jalankan"]


def jalankan():
    """Kembalikan {nama_sumber: DataFrame mentah}."""
    hasil_xlsx = baca_semua_xlsx()
    return {
        "bnpb_xlsx": hasil_xlsx,
    }
