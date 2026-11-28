"""Tahap 4–6 — pilih observasi Gold, bentuk panel, dan integrasikan nasional."""
from pathlib import Path

from src.gold.panel import bentuk_panel_gold

GOLD_DIR = Path(__file__).resolve().parents[2] / "data" / "gold"


def jalankan(silver):
    """Bangun dan simpan panel provinsi serta tabel nasional terpilih."""
    if silver is None or (isinstance(silver, dict) and not silver):
        raise ValueError("Gold memerlukan DataFrame Silver yang tidak kosong.")

    GOLD_DIR.mkdir(parents=True, exist_ok=True)
    panel_provinsi, selected_national, selection_counts = bentuk_panel_gold(silver)
    panel_provinsi.to_parquet(GOLD_DIR / "panel_provinsi_bencana.parquet", index=False)
    selected_national.to_parquet(GOLD_DIR / "gold_nasional.parquet", index=False)

    from src.gold import muat_sql, nasional

    integrasi = nasional.jalankan(selected_national)
    integrasi["panel_provinsi"] = panel_provinsi
    integrasi["nasional_terpilih"] = selected_national
    integrasi["gold_selection_counts"] = selection_counts
    integrasi["baris_sql"] = muat_sql.jalankan(silver)
    return integrasi
