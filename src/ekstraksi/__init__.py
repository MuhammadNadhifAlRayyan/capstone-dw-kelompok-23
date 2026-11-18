"""Tahap 1 — Ekstraksi data mentah (Kasus 23).

Membaca berkas mentah BNPB (XLSX tangan/ dan JSON datastore/) menjadi dictionary DataFrame mentah,
lengkap dengan kolom silsilah:
- `_berkas_raw`: jalur relatif terhadap data/raw/
- `_sha256_raw`: hash SHA-256 dari MANIFEST.csv
"""

from pathlib import Path
from typing import Any, Dict
import json
import pandas as pd

from src.common.manifest import sha256_raw

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"


def ekstraksi_xlsx_2025() -> Dict[str, Any]:
    """Ekstraksi berkas rekap rumah rusak 2025."""
    rel = "bnpb/2026-10-20/tangan/kompilasi-data-kejadian-dan-dampak-bencana-2025/43b83e79-c8b6-4b9a-b2f0-d1cbd9cfa636-jumlah-rumah-rusak-akibat-bencana-menurut-provinsi-2025.xlsx"
    df = pd.read_excel(RAW / rel, sheet_name="Rumah Rusak 2025", header=1)
    return {"df": df, "_berkas_raw": rel, "_sha256_raw": sha256_raw(rel), "periode": "2025"}


def ekstraksi_datastore_2024() -> Dict[str, Any]:
    """Ekstraksi berkas datastore rumah rusak 2024."""
    rel = "bnpb/2026-10-20/datastore/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/b5e3d843-cf11-4333-b8e3-233a2279b65a.json"
    with open(RAW / rel, encoding="utf-8") as f:
        recs = json.load(f)["halaman"][0]["result"]["records"]
    df = pd.DataFrame(recs)
    return {"df": df, "_berkas_raw": rel, "_sha256_raw": sha256_raw(rel), "periode": "2024"}


def ekstraksi_xlsx_2021() -> Dict[str, Any]:
    """Ekstraksi tabel rekap 2021 per provinsi."""
    rel = "bnpb/2026-10-20/tangan/data-bencana/0c165adc-5be2-489d-8b1a-e90c6715e73e-tabel-jumlah-kejadian-korban-dan-kerusakan-akibat-bencana-tahun-2021-per-provinsi.xlsx"
    df = pd.read_excel(RAW / rel, header=None).iloc[5:]
    return {"df": df, "_berkas_raw": rel, "_sha256_raw": sha256_raw(rel), "periode": "2021"}


def ekstraksi_xlsx_2022() -> Dict[str, Any]:
    """Ekstraksi tabel rekap 2022 per provinsi."""
    rel = "bnpb/2026-10-20/tangan/data-bencana/692df9e1-a8f8-49b3-a78f-de5795fb6e79-tabel-jumlah-kejadian-korban-dan-kerusakan-akibat-bencana-tahun-2022-per-provinsi.xlsx"
    df = pd.read_excel(RAW / rel, header=None).iloc[5:]
    return {"df": df, "_berkas_raw": rel, "_sha256_raw": sha256_raw(rel), "periode": "2022"}


def jalankan() -> Dict[str, Any]:
    """Eksekusi pembaca seluruh format mentah tahap 1."""
    hasil = {
        "rr_2025": ekstraksi_xlsx_2025(),
        "rr_2024": ekstraksi_datastore_2024(),
        "rr_2021": ekstraksi_xlsx_2021(),
        "rr_2022": ekstraksi_xlsx_2022(),
    }
    return hasil
