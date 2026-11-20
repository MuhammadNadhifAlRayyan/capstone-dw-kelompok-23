"""Pembaca berkas JSON datastore BNPB dan metadata CKAN.

Bagian dari Tahap 1 — Ekstraksi (Milik tim Kelompok 23).
Tugas modul ini:
1. Membaca metadata CKAN (package & resource) dari data/raw/bnpb/.../ckan/.
2. Membaca seluruh data JSON datastore BNPB (38 berkas) dari data/raw/bnpb/.../datastore/.
3. Menjaga keaslian kolom mentah (tanpa pembersihan).
4. Menempelkan kolom lineage wajib: `_berkas_raw` dan `_sha256_raw`.
"""
import json
from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd

from src.common.manifest import RAW, sha256_raw

BNPB_RAW = RAW / "bnpb" / "2026-10-20"
CKAN_FILE = BNPB_RAW / "ckan" / "package_search-pusdatinkom-01.json"
DATASTORE_DIR = BNPB_RAW / "datastore"


def baca_metadata_ckan(path: Path = CKAN_FILE) -> pd.DataFrame:
    """Membaca metadata CKAN package_search menjadi DataFrame daftar resource."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    baris = []
    for pkg in data.get("result", {}).get("results", []):
        pkg_id = pkg.get("id")
        pkg_name = pkg.get("name")
        pkg_title = pkg.get("title")
        for res in pkg.get("resources", []):
            baris.append({
                "package_id": pkg_id,
                "package_name": pkg_name,
                "package_title": pkg_title,
                "resource_id": res.get("id"),
                "resource_name": res.get("name"),
                "resource_format": res.get("format"),
                "resource_description": res.get("description"),
                "resource_url": res.get("url"),
                "created": res.get("created"),
                "last_modified": res.get("last_modified"),
            })

    df = pd.DataFrame(baris)
    rel_path = path.relative_to(RAW).as_posix()
    df["_berkas_raw"] = rel_path
    df["_sha256_raw"] = sha256_raw(rel_path)
    return df


def peta_metadata_resource(path: Path = CKAN_FILE) -> Dict[str, dict]:
    """Peta resource_id -> info metadata dari CKAN."""
    df_ckan = baca_metadata_ckan(path)
    peta = {}
    for _, row in df_ckan.iterrows():
        peta[row["resource_id"]] = {
            "package_id": row["package_id"],
            "package_name": row["package_name"],
            "package_title": row["package_title"],
            "resource_name": row["resource_name"],
            "resource_format": row["resource_format"],
        }
    return peta


def baca_berkas_datastore(path: Path, raw_root: Path = RAW) -> pd.DataFrame:
    """Membaca satu berkas JSON datastore menjadi DataFrame mentah."""
    with open(path, encoding="utf-8") as f:
        isi = json.load(f)

    records = []
    for hal in isi.get("halaman", []):
        records.extend(hal.get("result", {}).get("records", []))

    df = pd.DataFrame(records)
    rel_path = path.relative_to(raw_root).as_posix()
    df["_berkas_raw"] = rel_path
    df["_sha256_raw"] = sha256_raw(rel_path)
    return df


def baca_semua_datastore(
    datastore_dir: Path = DATASTORE_DIR,
    raw_root: Path = RAW
) -> Dict[str, pd.DataFrame]:
    """Membaca seluruh berkas JSON di folder datastore.
    
    Mengembalikan dict: {rel_path: DataFrame mentah}.
    """
    hasil = {}
    berkas_list = sorted(list(datastore_dir.rglob("*.json")))
    for berkas in berkas_list:
        rel = berkas.relative_to(raw_root).as_posix()
        df = baca_berkas_datastore(berkas, raw_root=raw_root)
        hasil[rel] = df
    return hasil


def rekap_bnpb_json() -> List[dict]:
    """Rekapitulasi pembacaan seluruh berkas JSON BNPB (CKAN dan Datastore)."""
    peta = peta_metadata_resource()
    rekap = []

    # 1. CKAN metadata
    df_ckan = baca_metadata_ckan()
    rekap.append({
        "jenis": "ckan",
        "berkas": CKAN_FILE.name,
        "rel_path": CKAN_FILE.relative_to(RAW).as_posix(),
        "seri_nama": "Metadata Pencarian Paket & Resource CKAN (Pusdatinkom)",
        "baris": len(df_ckan),
        "sha256": sha256_raw(CKAN_FILE.relative_to(RAW).as_posix()),
    })

    # 2. Datastore JSON
    ds_dict = baca_semua_datastore()
    for rel_path, df in ds_dict.items():
        stem = Path(rel_path).stem
        meta = peta.get(stem, {})
        rekap.append({
            "jenis": "datastore",
            "berkas": Path(rel_path).name,
            "rel_path": rel_path,
            "seri_nama": meta.get("resource_name", "-"),
            "baris": len(df),
            "sha256": sha256_raw(rel_path),
        })

    return rekap


if __name__ == "__main__":
    rekap = rekap_bnpb_json()
    total_datastore = sum(r["baris"] for r in rekap if r["jenis"] == "datastore")
    print(f"Total berkas BNPB JSON terbaca: {len(rekap)} berkas (1 CKAN + {len(rekap)-1} Datastore)")
    print(f"Total baris data records pada Datastore: {total_datastore} baris")
    print("\n| No | Berkas | Baris | Seri / Judul Resource |")
    print("|---|---|---|---|")
    for idx, r in enumerate(rekap, 1):
        print(f"| {idx} | `{r['berkas']}` | {r['baris']} | {r['seri_nama']} |")
