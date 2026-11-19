"""Pembaca berkas Excel (XLSX) BNPB di data/raw/bnpb/.../tangan/.

Membaca 15 berkas XLSX rekapitulasi BNPB tanpa membersihkan atau mengubah angka:
- Menangani baris judul ganda (multi-level header) dan membaca rincian kerusakan secara eksplisit.
- Mengatasi sel gabungan (merged cells) pada kolom wilayah dengan forward-fill.
- Membaca tabel matriks spasial (provinsi & kabupaten) serta tabel rekapitulasi.
- Menempelkan kolom lineage `_berkas_raw` dan `_sha256_raw` dari `src.common.manifest`.
"""
import sys
from pathlib import Path
from typing import Dict, Union

import openpyxl
import pandas as pd

from src.common.manifest import RAW, sha256_raw


def _win_path(p: Path) -> str:
    """Konversi ke path Windows extended jika berjalan di Windows."""
    s = str(p.resolve())
    if sys.platform == "win32" and not s.startswith("\\\\?\\") and not s.startswith("//"):
        return "\\\\?\\" + s
    return s


def baca_berkas_xlsx(jalur: Union[str, Path], raw: Path = RAW) -> pd.DataFrame:
    """Membaca satu berkas XLSX BNPB menjadi DataFrame mentah dengan kolom asal dan lineage."""
    p = Path(jalur)
    if not p.is_absolute():
        p = raw / p
    raw_path = Path(raw).resolve()
    rel_posix = p.resolve().relative_to(raw_path).as_posix()
    sha = sha256_raw(rel_posix, raw=raw)

    win_p = _win_path(p)
    wb = openpyxl.load_workbook(win_p, data_only=True)

    # Pilih lembar data (abaikan lembar metadata seperti 'Keterangan')
    lembar_data = [s for s in wb.sheetnames if s.strip().lower() != "keterangan"]
    if not lembar_data:
        raise ValueError(f"Tidak ada lembar data di {rel_posix}")
    ws = wb[lembar_data[0]]

    fname = p.name.lower()
    baris_data = []

    # Kategori 1: data-bencana (multi-level header)
    if "data-bencana/" in rel_posix:
        is_kab = "kabupaten" in fname or "kabupten" in fname
        if not is_kab:
            # Rekap Provinsi 2021 & 2022
            # R1: Judul, R3: Header atas, R4: Subheader, R5: Satuan, R6+: Data
            headers = [
                "Provinsi",
                "Jenis Bencana",
                "Jumlah Kejadian",
                "Korban - Meninggal",
                "Korban - Hilang",
                "Korban - Luka-Luka",
                "Korban - Terdampak - Mengungsi",
                "Kerusakan - Rumah Rusak Berat",
                "Kerusakan - Rumah Rusak Sedang",
                "Kerusakan - Rumah Rusak Ringan",
                "Kerusakan - Rumah Terendam",
                "Kerusakan - Sarana Pendidikan",
                "Kerusakan - Sarana Peribadatan",
                "Kerusakan - Sarana Kesehatan",
                "Kerusakan - Perkantoran",
                "Kerusakan - Jembatan",
            ]
            last_prov = None
            for r in range(6, ws.max_row + 1):
                vals = [ws.cell(r, c).value for c in range(1, 17)]
                if not any(v is not None for v in vals):
                    continue
                if vals[0] is not None:
                    last_prov = vals[0]
                else:
                    vals[0] = last_prov
                baris_data.append(vals)
            df = pd.DataFrame(baris_data, columns=headers)
        else:
            # Rekap Kabupaten/Kota 2021 & 2022
            # 2021 mulai baris 5, 2022 mulai baris 6
            start_r = 5 if "2021" in fname else 6
            headers = [
                "Provinsi",
                "Kabupaten/Kota",
                "Jenis Bencana",
                "Jumlah Kejadian",
                "Korban - Meninggal",
                "Korban - Hilang",
                "Korban - Luka-Luka",
                "Korban - Terdampak - Mengungsi",
                "Kerusakan - Rumah Rusak Berat",
                "Kerusakan - Rumah Rusak Sedang",
                "Kerusakan - Rumah Rusak Ringan",
                "Kerusakan - Rumah Terendam",
                "Kerusakan - Sarana Pendidikan",
                "Kerusakan - Sarana Peribadatan",
                "Kerusakan - Sarana Kesehatan",
                "Kerusakan - Perkantoran",
                "Kerusakan - Jembatan",
            ]
            last_prov = None
            last_kab = None
            for r in range(start_r, ws.max_row + 1):
                vals = [ws.cell(r, c).value for c in range(1, 18)]
                if not any(v is not None for v in vals):
                    continue
                if vals[0] is not None:
                    last_prov = vals[0]
                else:
                    vals[0] = last_prov
                if vals[1] is not None:
                    last_kab = vals[1]
                else:
                    vals[1] = last_kab
                baris_data.append(vals)
            df = pd.DataFrame(baris_data, columns=headers)

    # Kategori 3: Rekapitulasi Nasional 2025
    elif "rekapitulasi" in fname:
        # R1: Judul, R2: Header (16 kolom non-kosong), R3+: Data
        num_cols = 16
        headers = [ws.cell(2, c).value for c in range(1, num_cols + 1)]
        for r in range(3, ws.max_row + 1):
            vals = [ws.cell(r, c).value for c in range(1, num_cols + 1)]
            if any(v is not None for v in vals):
                baris_data.append(vals)
        df = pd.DataFrame(baris_data, columns=headers)

    # Kategori 2: Matriks Spasial (Provinsi & Kabupaten) 2024 & 2025
    else:
        # R1: Judul, R2: Header (14 kolom: wilayah + 9 jenis bencana), R3+: Data
        num_cols = 14
        headers = [ws.cell(2, c).value for c in range(1, num_cols + 1)]
        for r in range(3, ws.max_row + 1):
            vals = [ws.cell(r, c).value for c in range(1, num_cols + 1)]
            if any(v is not None for v in vals):
                baris_data.append(vals)
        df = pd.DataFrame(baris_data, columns=headers)

    # Tempelkan kolom lineage
    df["_berkas_raw"] = rel_posix
    df["_sha256_raw"] = sha
    return df


def baca_semua_xlsx(raw: Path = RAW) -> Dict[str, pd.DataFrame]:
    """Membaca seluruh 15 berkas XLSX BNPB di data/raw/bnpb/.../tangan/."""
    raw = Path(raw)
    berkas_xlsx = sorted(list(raw.glob("bnpb/*/tangan/*/*.xlsx")))
    hasil = {}
    for p in berkas_xlsx:
        rel = p.relative_to(raw).as_posix()
        hasil[rel] = baca_berkas_xlsx(p, raw=raw)
    return hasil


if __name__ == "__main__":
    semua = baca_semua_xlsx()
    print(f"Total berkas XLSX terbaca: {len(semua)}")
    total_baris = 0
    for berkas, df in semua.items():
        n = len(df)
        total_baris += n
        nama = berkas.split("/")[-1]
        print(f"  {n:>5} baris | {nama}")
    print(f"Total baris mentah XLSX: {total_baris}")
