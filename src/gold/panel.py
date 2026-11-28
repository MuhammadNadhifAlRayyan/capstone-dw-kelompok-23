"""Modul pembentukan kerangka panel 38 provinsi x periode (Tahap 4).

Penanggung Jawab: Nabila Nur Azizah (NIM: 124450048)
Fokus: Transformasi dan Panel
"""
import numpy as np
import pandas as pd

from src.gold.aturan import pilih_observasi_gold
from src.gold.skema import (
    PROVINSI_38_2025,
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
    """Transformasi log1p nilai rupiah nominal; nilai negatif tidak ditutup-tutupi."""
    numerik = pd.to_numeric(seri, errors="raise")
    if (numerik.dropna() < 0).any():
        raise ValueError("log1p nilai rupiah tidak terdefinisi untuk nilai negatif.")
    return np.log1p(numerik)


def pisahkan_nasional(df_silver):
    """Memisahkan level nasional dari provinsi tanpa menjumlahkan rincian."""
    provincial, national, _ = pilih_observasi_gold(df_silver)
    return provincial, national


def bentuk_panel_gold(df_silver):
    """Bentuk panel, tabel nasional terpilih, dan jumlah Silver yang dikecualikan."""
    observations, national, selection_counts = pilih_observasi_gold(df_silver)
    grid = buat_grid_provinsi_periode()
    grid = grid.rename(columns={"tahun": "periode"})
    grid["periode"] = grid["periode"].astype(str)

    for indicator, rows in observations.groupby("_indikator", sort=True):
        if rows.duplicated(["wilayah_kode", "periode"]).any():
            raise ValueError(
                f"Aturan Gold menghasilkan lebih dari satu nilai untuk {indicator}."
            )
        columns = ["wilayah_kode", "periode", "nilai"]
        rows = rows[
            columns
            + [
                "_berkas_raw",
                "_sha256_raw",
                "_lineage",
                "flag_outlier",
                "flag_patahan",
            ]
        ]
        rows = rows.rename(
            columns={
                "nilai": indicator,
                "_berkas_raw": f"{indicator}__berkas_raw",
                "_sha256_raw": f"{indicator}__sha256_raw",
                "_lineage": f"{indicator}__lineage",
                "flag_outlier": f"{indicator}__flag_outlier",
                "flag_patahan": f"{indicator}__flag_patahan",
            }
        )
        grid = grid.merge(
            rows,
            on=["wilayah_kode", "periode"],
            how="left",
            validate="one_to_one",
        )

    grid["tahun"] = grid.pop("periode").astype(int)
    for indicator in ("nilai_kerugian", "nilai_kerusakan"):
        if indicator in grid:
            grid[f"log_{indicator}"] = transformasi_log1p(grid[indicator])
    return grid, national, selection_counts
