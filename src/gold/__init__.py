"""Tahap 4–6 — Gold: panel provinsi x periode x indikator, tabel nasional, rekonsiliasi, dan SQL.

Urutan: daftar pasangan (Sprint 1, reports/pasangan-rekonsiliasi.md) -> panel Gold -> tabel nasional Gold
-> tabel rekonsiliasi -> Silver dan Gold dimuat ke DuckDB.
"""
from src.gold import muat_sql, nasional, nasional_gold, panel, rekonsiliasi


def jalankan(silver):
    """Bangun dan simpan panel provinsi serta tabel nasional terpilih."""
    if silver is None or (isinstance(silver, dict) and not silver):
        raise ValueError("Gold memerlukan DataFrame Silver yang tidak kosong.")

    GOLD_DIR.mkdir(parents=True, exist_ok=True)
    panel_provinsi, selected_national = bentuk_panel_gold(silver)
    panel_provinsi.to_parquet(GOLD_DIR / "panel_provinsi_bencana.parquet", index=False)
    selected_national.to_parquet(GOLD_DIR / "gold_nasional.parquet", index=False)

    from src.gold import muat_sql, nasional

    integrasi = nasional.jalankan(selected_national)
    integrasi["panel_provinsi"] = panel_provinsi
    integrasi["nasional_terpilih"] = selected_national
    integrasi["baris_sql"] = muat_sql.jalankan(silver)
    return integrasi
