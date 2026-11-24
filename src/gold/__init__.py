"""Tahap 4–6 — Gold: panel provinsi x periode x indikator, tabel nasional, rekonsiliasi, dan SQL.

Urutan: daftar pasangan (Sprint 1, reports/pasangan-rekonsiliasi.md) -> panel Gold -> tabel nasional Gold
-> tabel rekonsiliasi -> Silver dan Gold dimuat ke DuckDB.
"""
from src.gold import muat_sql, nasional, nasional_gold


def jalankan(silver):
    hasil = nasional.jalankan(silver)
    hasil["nasional"] = nasional_gold.jalankan(silver)
    hasil["baris_sql"] = muat_sql.jalankan(silver)
    return hasil
