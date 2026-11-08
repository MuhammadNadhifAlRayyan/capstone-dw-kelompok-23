"""Tahap 4–6 — Reshape, integrasi, dan penyimpanan ke Gold.

Penanggung Jawab Komponen Transformasi dan Panel (Tahap 4):
Nabila Nur Azizah (NIM: 124450048) — Koordinator

Keluaran:
- data/gold/panel_provinsi_bencana.parquet (panel 38 provinsi x periode x indikator)
- data/gold/gold_nasional.parquet (agregat nasional pembanding)
- data/gold/gold.sqlite (basis data relasional)
"""
from pathlib import Path

from src.gold.panel import (
    bentuk_panel_gold,
    buat_grid_provinsi_periode,
    pisahkan_nasional,
    transformasi_log1p,
)
from src.gold.skema import PROVINSI_38_2025, SERI_UTAMA_K23

GOLD_DIR = Path(__file__).resolve().parents[2] / "data" / "gold"


def jalankan(silver):
    """Menerima tabel Silver, membentuk panel Gold 38 provinsi x periode, dan menyimpannya.

    Args:
        silver: DataFrame Silver atau dictionary keluaran tahap sebelumnya.

    Returns:
        dict: {'panel_provinsi': DataFrame, 'nasional': DataFrame}
    """
    if silver is None or (isinstance(silver, dict) and not silver):
        raise NotImplementedError(
            "Tahap 4: Menunggu keluaran Silver lengkap dari Sprint 1 untuk pembentukan panel final."
        )

    GOLD_DIR.mkdir(parents=True, exist_ok=True)
    panel_provinsi, df_nasional = bentuk_panel_gold(silver)

    jalur_panel = GOLD_DIR / "panel_provinsi_bencana.parquet"
    jalur_nasional = GOLD_DIR / "gold_nasional.parquet"

    panel_provinsi.to_parquet(jalur_panel, index=False)
    df_nasional.to_parquet(jalur_nasional, index=False)

    return {"panel_provinsi": panel_provinsi, "nasional": df_nasional}
