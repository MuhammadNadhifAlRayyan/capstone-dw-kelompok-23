"""Pembaca berkas JSON Bank Dunia (WDI) di data/raw/wdi/.

Membaca data dan metadata World Development Indicators (WDI) tanpa membersihkan angka:
- Mengubah struktur larik respons API WDI menjadi DataFrame mentah.
- Menyediakan penyaringan untuk indikator pembanding kasus: EN.CLC.MDAT.ZS.
- Menempelkan kolom lineage `_berkas_raw` dan `_sha256_raw` dari `src.common.manifest`.
"""
import json
import sys
from pathlib import Path
from typing import Dict, Optional, Union

import pandas as pd

from src.common.manifest import RAW, sha256_raw


def _win_path(p: Path) -> Path:
    """Konversi ke path Windows extended jika berjalan di Windows."""
    s = str(p.resolve())
    if sys.platform == "win32" and not s.startswith("\\\\?\\") and not s.startswith("//"):
        return Path("\\\\?\\" + s)
    return p


def baca_wdi_data(
    jalur: Optional[Union[str, Path]] = None,
    raw: Path = RAW,
    filter_indikator: Optional[str] = "EN.CLC.MDAT.ZS",
) -> pd.DataFrame:
    """Membaca berkas data WDI kelompok-01-hal-01.json dan mengembalikan DataFrame mentah."""
    raw = Path(raw)
    p = Path(jalur) if jalur else raw / "wdi" / "2026-10-20" / "data" / "kelompok-01-hal-01.json"
    if not p.is_absolute():
        p = raw / p
    raw_path = raw.resolve()
    rel_posix = p.resolve().relative_to(raw_path).as_posix()
    sha = sha256_raw(rel_posix, raw=raw)

    win_p = _win_path(p)
    with open(win_p, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Larik respons WDI: [metadata_halaman, daftar_observasi]
    observasi = data[1] if isinstance(data, list) and len(data) > 1 else []

    baris = []
    for obs in observasi:
        ind_id = obs.get("indicator", {}).get("id")
        if filter_indikator and ind_id != filter_indikator:
            continue
        baris.append({
            "indicator_id": ind_id,
            "indicator_value": obs.get("indicator", {}).get("value"),
            "country_id": obs.get("country", {}).get("id"),
            "country_value": obs.get("country", {}).get("value"),
            "countryiso3code": obs.get("countryiso3code"),
            "date": obs.get("date"),
            "value": obs.get("value"),
            "unit": obs.get("unit"),
            "obs_status": obs.get("obs_status"),
            "decimal": obs.get("decimal"),
        })

    df = pd.DataFrame(baris)
    df["_berkas_raw"] = rel_posix
    df["_sha256_raw"] = sha
    return df


def baca_semua_wdi(raw: Path = RAW) -> Dict[str, pd.DataFrame]:
    """Membaca seluruh 4 berkas WDI (1 data observasi dan 3 metadata)."""
    raw = Path(raw)
    hasil = {}

    # 1. Data observasi
    p_data = raw / "wdi" / "2026-10-20" / "data" / "kelompok-01-hal-01.json"
    hasil[p_data.relative_to(raw).as_posix()] = baca_wdi_data(p_data, raw=raw, filter_indikator=None)

    # 2. Metadata sumber & indikator
    for meta_name in ["sumber.json", "sumber2_indikator.json", "sumber46_indikator.json"]:
        p_meta = raw / "wdi" / "2026-10-20" / "metadata" / meta_name
        rel_posix = p_meta.relative_to(raw).as_posix()
        sha = sha256_raw(rel_posix, raw=raw)
        win_p = _win_path(p_meta)
        with open(win_p, "r", encoding="utf-8") as f:
            d = json.load(f)
        items = d[1] if isinstance(d, list) and len(d) > 1 else []
        df_meta = pd.json_normalize(items)
        df_meta["_berkas_raw"] = rel_posix
        df_meta["_sha256_raw"] = sha
        hasil[rel_posix] = df_meta

    return hasil


if __name__ == "__main__":
    df_kasus = baca_wdi_data()
    print(f"Data WDI kasus 23 (EN.CLC.MDAT.ZS): {len(df_kasus)} observasi")
    print(df_kasus[df_kasus["value"].notna()][["date", "value", "indicator_id"]])

    semua_wdi = baca_semua_wdi()
    print(f"\nTotal berkas WDI terbaca: {len(semua_wdi)}")
    for b, d in semua_wdi.items():
        print(f"  {len(d):>5} baris | {b}")
