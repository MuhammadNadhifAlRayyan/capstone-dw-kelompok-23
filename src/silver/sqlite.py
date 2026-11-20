"""Muat tabel Silver kanonis ke SQLite (Tahap 5)."""
import argparse
import sqlite3
from pathlib import Path

import pandas as pd

from src.common.manifest import RAW, baca
from src.common.skema import KOLOM, periksa_silver

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "data" / "silver" / "silver.parquet"
DEFAULT_DATABASE = ROOT / "data" / "silver" / "silver.sqlite"

DDL = """
CREATE TABLE IF NOT EXISTS silver (
    sumber TEXT NOT NULL,
    seri_kode TEXT NOT NULL,
    wilayah_kode INTEGER NOT NULL,
    nama_wilayah TEXT NOT NULL,
    periode TEXT NOT NULL,
    jenis_periode TEXT NOT NULL,
    rincian TEXT NOT NULL,
    nilai NUMERIC NOT NULL CHECK (typeof(nilai) IN ('integer', 'real')),
    satuan TEXT NOT NULL,
    _berkas_raw TEXT NOT NULL,
    _sha256_raw TEXT NOT NULL,
    PRIMARY KEY (sumber, seri_kode, wilayah_kode, periode, rincian, _berkas_raw)
) WITHOUT ROWID
"""

KOLOM_TEKS = [
    "sumber",
    "seri_kode",
    "nama_wilayah",
    "periode",
    "jenis_periode",
    "rincian",
    "satuan",
    "_berkas_raw",
    "_sha256_raw",
]


def _validasi(df: pd.DataFrame) -> None:
    """Pastikan data memenuhi kontrak Silver dan lineage manifest sebelum menulis."""
    kurang = [kolom for kolom in KOLOM if kolom not in df.columns]
    if kurang:
        raise ValueError(f"Kolom Silver wajib tidak ada: {kurang}")

    pelanggaran = periksa_silver(df, manifest=baca())
    if pelanggaran:
        raise ValueError("Silver tidak valid: " + "; ".join(pelanggaran))

    bukan_teks = {
        kolom: int((~df[kolom].map(lambda nilai: isinstance(nilai, str))).sum())
        for kolom in KOLOM_TEKS
    }
    bukan_teks = {kolom: jumlah for kolom, jumlah in bukan_teks.items() if jumlah}
    if bukan_teks:
        raise ValueError(f"Kolom teks Silver berisi nilai non-teks: {bukan_teks}")

    sha_tidak_valid = df["_sha256_raw"].map(
        lambda nilai: len(nilai) != 64 or any(kar not in "0123456789abcdef" for kar in nilai)
    )
    if sha_tidak_valid.any():
        raise ValueError(f"{sha_tidak_valid.sum()} nilai _sha256_raw bukan SHA-256 heksadesimal")


def muat_dataframe(
    df: pd.DataFrame,
    database: Path = DEFAULT_DATABASE,
    *,
    replace: bool = True,
) -> int:
    """Muat Silver ke tabel SQLite; secara default mengganti isi tabel secara atomik."""
    _validasi(df)
    database = Path(database)
    database.parent.mkdir(parents=True, exist_ok=True)

    kolom_sql = ", ".join(f'"{kolom}"' for kolom in KOLOM)
    placeholders = ", ".join("?" for _ in KOLOM)
    pernyataan = f"INSERT INTO silver ({kolom_sql}) VALUES ({placeholders})"
    baris = [
        tuple(nilai.item() if hasattr(nilai, "item") else nilai for nilai in record)
        for record in df[KOLOM].itertuples(index=False, name=None)
    ]

    koneksi = sqlite3.connect(database)
    try:
        koneksi.execute(DDL)
        with koneksi:
            if replace:
                koneksi.execute("DELETE FROM silver")
            koneksi.executemany(pernyataan, baris)
    finally:
        koneksi.close()
    return len(baris)


def main() -> None:
    parser = argparse.ArgumentParser(description="Muat Silver Parquet ke basis data SQLite.")
    parser.add_argument("input", nargs="?", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("database", nargs="?", type=Path, default=DEFAULT_DATABASE)
    args = parser.parse_args()

    silver = pd.read_parquet(args.input)
    jumlah = muat_dataframe(silver, args.database)
    print(f"SQLite: {jumlah:,} baris dimuat ke {args.database} (tabel silver)")


if __name__ == "__main__":
    main()
