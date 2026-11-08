"""Modul pembentukan kerangka panel 38 provinsi x periode (Tahap 4).

Penanggung Jawab: Nabila Nur Azizah (NIM: 124450048)
Fokus: Transformasi dan Panel
"""
import numpy as np
import pandas as pd

from src.gold.skema import (
    KODE_NASIONAL,
    NAMA_NASIONAL,
    PROVINSI_38_2025,
    SERI_UTAMA_K23,
    TAHUN_AKHIR,
    TAHUN_AWAL,
)


def buat_grid_provinsi_periode(tahun_mulai=TAHUN_AWAL, tahun_akhir=TAHUN_AKHIR):
    """Membentuk grid master lengkap 38 provinsi x tahun (2010 s.d. 2025).

    Returns:
        pd.DataFrame dengan kolom ['wilayah_kode', 'nama_wilayah', 'tahun']
        terurut berdasarkan wilayah_kode dan tahun.
    """
    wilayah_df = pd.DataFrame(
        list(PROVINSI_38_2025.items()), columns=["wilayah_kode", "nama_wilayah"]
    )
    tahun_df = pd.DataFrame({"tahun": list(range(tahun_mulai, tahun_akhir + 1))})

    grid = wilayah_df.merge(tahun_df, how="cross")
    grid = grid.sort_values(["wilayah_kode", "tahun"]).reset_index(drop=True)
    return grid


def transformasi_log1p(seri):
    """Transformasi logaritma log1p untuk fitur dengan sebaran moneter sangat lebar."""
    return np.log1p(np.maximum(0, seri))


def pisahkan_nasional(df_silver):
    """Memisahkan observasi level nasional (9999) dari observasi level provinsi.

    Args:
        df_silver: DataFrame Silver dengan kolom 'wilayah_kode'

    Returns:
        (df_provinsi, df_nasional)
    """
    is_nasional = (df_silver["wilayah_kode"] == KODE_NASIONAL) | (
        df_silver["nama_wilayah"].str.upper() == NAMA_NASIONAL
    )
    df_nasional = df_silver[is_nasional].copy()
    df_provinsi = df_silver[~is_nasional].copy()
    return df_provinsi, df_nasional


def bentuk_panel_gold(df_silver):
    """Mereshape tabel Silver menjadi panel lebar (Gold) provinsi x periode x indikator.

    Draft kerangka transformasi:
    1. Memisahkan data nasional (kode 9999) ke tabel nasional.
    2. Membuat grid master lengkap 38 provinsi x rentang tahun.
    3. Menggabungkan observasi tiap seri utama ke dalam grid.
    4. Menghitung transformasi log1p untuk nilai kerugian dan kerusakan.
    """
    df_prov, df_nas = pisahkan_nasional(df_silver)

    # Inisialisasi grid master
    grid = buat_grid_provinsi_periode()

    # Catatan: Integrasi pengisian metrik per seri akan dilakukan
    # setelah tahap ekstraksi dan pembersihan Silver rampung di Sprint 1.
    return grid, df_nas
