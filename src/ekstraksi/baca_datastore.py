"""Pembaca berkas JSON Datastore dan CKAN BNPB di data/raw/bnpb/.

Membaca 38 berkas JSON CKAN Datastore dan 1 berkas metadata CKAN tanpa membersihkan angka:
- Mengekstrak semua rekaman (records) dari seluruh halaman (paginasi).
- Menjaga kolom asal yang setia pada sumber mentah.
- Menempelkan kolom lineage `_berkas_raw` dan `_sha256_raw` dari `src.common.manifest`.
"""
import json
import sys
from pathlib import Path
from typing import Dict, Union

import pandas as pd

from src.common.manifest import RAW, sha256_raw


def _win_path(p: Path) -> Path:
    """Konversi ke path Windows extended jika berjalan di Windows."""
    s = str(p.resolve())
    if sys.platform == "win32" and not s.startswith("\\\\?\\") and not s.startswith("//"):
        return Path("\\\\?\\" + s)
    return p


def baca_berkas_datastore(jalur: Union[str, Path], raw: Path = RAW) -> pd.DataFrame:
    """Membaca satu berkas JSON datastore BNPB menjadi DataFrame mentah dengan lineage."""
    p = Path(jalur)
    if not p.is_absolute():
        p = raw / p
    raw_path = Path(raw).resolve()
    rel_posix = p.resolve().relative_to(raw_path).as_posix()
    sha = sha256_raw(rel_posix, raw=raw)

    win_p = _win_path(p)
    with open(win_p, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Kumpulkan seluruh record dari seluruh halaman
    records = []
    for hal in data.get("halaman", []):
        recs = hal.get("result", {}).get("records", [])
        records.extend(recs)

    df = pd.DataFrame(records)
    df["_berkas_raw"] = rel_posix
    df["_sha256_raw"] = sha
    return df


def baca_semua_datastore(raw: Path = RAW) -> Dict[str, pd.DataFrame]:
    """Membaca seluruh 38 berkas JSON datastore BNPB."""
    raw = Path(raw)
    berkas_json = sorted(list(raw.glob("bnpb/*/datastore/*/*.json")))
    hasil = {}
    for p in berkas_json:
        rel = p.relative_to(raw).as_posix()
        hasil[rel] = baca_berkas_datastore(p, raw=raw)
    return hasil


def baca_metadata_ckan(raw: Path = RAW) -> pd.DataFrame:
    """Membaca berkas metadata CKAN BNPB dan mengembalikan tabel pemetaan resource."""
    raw = Path(raw)
    p = raw / "bnpb" / "2026-10-20" / "ckan" / "package_search-pusdatinkom-01.json"
    rel_posix = p.relative_to(raw).as_posix()
    sha = sha256_raw(rel_posix, raw=raw)

    win_p = _win_path(p)
    with open(win_p, "r", encoding="utf-8") as f:
        data = json.load(f)

    baris = []
    for pkg in data.get("result", {}).get("results", []):
        pkg_id = pkg.get("id")
        pkg_title = pkg.get("title")
        pkg_notes = pkg.get("notes")
        for res in pkg.get("resources", []):
            baris.append({
                "package_id": pkg_id,
                "package_title": pkg_title,
                "package_notes": pkg_notes,
                "resource_id": res.get("id"),
                "resource_name": res.get("name"),
                "resource_description": res.get("description"),
                "resource_format": res.get("format"),
                "resource_created": res.get("created"),
                "resource_last_modified": res.get("last_modified"),
            })

    df = pd.DataFrame(baris)
    df["_berkas_raw"] = rel_posix
    df["_sha256_raw"] = sha
    return df


if __name__ == "__main__":
    semua_ds = baca_semua_datastore()
    print(f"Total berkas JSON datastore terbaca: {len(semua_ds)}")
    total_recs = 0
    for berkas, df in semua_ds.items():
        n = len(df)
        total_recs += n
        nama = berkas.split("/")[-1]
        print(f"  {n:>5} baris | {nama}")
    print(f"Total baris mentah JSON datastore: {total_recs}")

    df_ckan = baca_metadata_ckan()
    print(f"\nMetadata CKAN terbaca: {len(df_ckan)} resources dari {df_ckan['package_id'].nunique()} packages")
