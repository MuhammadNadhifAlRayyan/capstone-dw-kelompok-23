"""Tahap 2–4 — Transformasi dan Pembentukan Silver (Kasus 23).

Menghasilkan tabel data/silver/silver.parquet yang memenuhi 11 kolom wajib:
- sumber, seri_kode, wilayah_kode, nama_wilayah, periode, jenis_periode, rincian, nilai, satuan, _berkas_raw, _sha256_raw
"""

from pathlib import Path
from typing import Any, Dict
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SILVER_FILE = ROOT / "data" / "silver" / "silver.parquet"

PROV_MAP = {
    "ACEH": 1100, "SUMATERA UTARA": 1200, "SUMATERA BARAT": 1300, "RIAU": 1400,
    "JAMBI": 1500, "SUMATERA SELATAN": 1600, "BENGKULU": 1700, "LAMPUNG": 1800,
    "KEPULAUAN BANGKA BELITUNG": 1900, "KEP. BANGKA BELITUNG": 1900,
    "KEPULAUAN RIAU": 2100, "KEP. RIAU": 2100,
    "DKI JAKARTA": 3100, "JAWA BARAT": 3200, "JAWA TENGAH": 3300,
    "DI YOGYAKARTA": 3400, "D.I. YOGYAKARTA": 3400, "JAWA TIMUR": 3500, "BANTEN": 3600,
    "BALI": 5100, "NUSA TENGGARA BARAT": 5200, "NUSA TENGGARA TIMUR": 5300,
    "KALIMANTAN BARAT": 6100, "KALIMANTAN TENGAH": 6200, "KALIMANTAN SELATAN": 6300,
    "KALIMANTAN TIMUR": 6400, "KALIMANTAN UTARA": 6500,
    "SULAWESI UTARA": 7100, "SULAWESI TENGAH": 7200, "SULAWESI SELATAN": 7300,
    "SULAWESI TENGGARA": 7400, "GORONTALO": 7500, "SULAWESI BARAT": 7600,
    "MALUKU": 8100, "MALUKU UTARA": 8200,
    "PAPUA BARAT": 9100, "PAPUA BARAT DAYA": 9200, "PAPUA": 9400,
    "PAPUA SELATAN": 9500, "PAPUA TENGAH": 9600, "PAPUA PEGUNUNGAN": 9700,
    "INDONESIA": 9999,
}

BENCANA_MAP = {
    "BANJIR": "banjir",
    "CUACA EKSTREM": "cuaca_ekstrem",
    "ERUPSI GUNUNG API": "erupsigunungapi",
    "GELOMBANG PASANG DAN ABRASI": "gelombang_pasang_abrasi",
    "GEMPABUMI": "gempa_bumi",
    "KEBAKARAN HUTAN DAN LAHAN": "kebakaran_hutan_lahan",
    "KEKERINGAN": "kekeringan",
    "TANAH LONGSOR": "tanah_longsor",
    "TSUNAMI": "tsunami",
}


def transform_2025(item: Dict[str, Any]) -> list:
    df, rel, sha = item["df"], item["_berkas_raw"], item["_sha256_raw"]
    rows = []
    for _, r in df.iterrows():
        prov = str(r["Provinsi"]).strip().upper()
        if prov not in PROV_MAP:
            continue
        w_kode = PROV_MAP[prov]
        for b_col, b_kat in BENCANA_MAP.items():
            if b_col in r:
                val = float(pd.to_numeric(r[b_col], errors="coerce") or 0.0)
                rows.append({
                    "sumber": "bnpb",
                    "seri_kode": "rumah_rusak",
                    "wilayah_kode": int(w_kode),
                    "nama_wilayah": prov,
                    "periode": "2025",
                    "jenis_periode": "tahun",
                    "rincian": b_kat,
                    "nilai": float(val),
                    "satuan": "unit",
                    "_berkas_raw": rel,
                    "_sha256_raw": sha,
                })
    return rows


def transform_2024(item: Dict[str, Any]) -> list:
    df, rel, sha = item["df"], item["_berkas_raw"], item["_sha256_raw"]
    rows = []
    for _, r in df.iterrows():
        prov = str(r.get("Provinsi", "")).strip().upper()
        if prov not in PROV_MAP:
            continue
        w_kode = PROV_MAP[prov]
        for b_col, b_kat in BENCANA_MAP.items():
            if b_col in r:
                val = float(pd.to_numeric(r[b_col], errors="coerce") or 0.0)
                rows.append({
                    "sumber": "bnpb",
                    "seri_kode": "rumah_rusak",
                    "wilayah_kode": int(w_kode),
                    "nama_wilayah": prov,
                    "periode": "2024",
                    "jenis_periode": "tahun",
                    "rincian": b_kat,
                    "nilai": float(val),
                    "satuan": "unit",
                    "_berkas_raw": rel,
                    "_sha256_raw": sha,
                })
    return rows


def transform_rekap_tangan(item: Dict[str, Any], periode: str) -> list:
    df, rel, sha = item["df"], item["_berkas_raw"], item["_sha256_raw"]
    rows = []
    current_prov = None
    current_prov_code = None

    for _, r in df.iterrows():
        p_name = r[0]
        if pd.notna(p_name) and str(p_name).strip():
            current_prov = str(p_name).strip().upper()
            current_prov_code = PROV_MAP.get(current_prov)

        if current_prov_code is None:
            continue

        for col_idx, kat in [(7, "rusak_berat"), (8, "rusak_sedang"), (9, "rusak_ringan")]:
            val = float(pd.to_numeric(r[col_idx], errors="coerce") or 0.0)
            rows.append({
                "sumber": "bnpb",
                "seri_kode": "rumah_rusak",
                "wilayah_kode": int(current_prov_code),
                "nama_wilayah": current_prov,
                "periode": periode,
                "jenis_periode": "tahun",
                "rincian": kat,
                "nilai": float(val),
                "satuan": "unit",
                "_berkas_raw": rel,
                "_sha256_raw": sha,
            })
    return rows


def jalankan(mentah: Dict[str, Any]) -> pd.DataFrame:
    """Mengubah keluaran tahap 1 menjadi DataFrame Silver dan menyimpannya."""
    all_rows = []
    all_rows.extend(transform_2025(mentah["rr_2025"]))
    all_rows.extend(transform_2024(mentah["rr_2024"]))
    all_rows.extend(transform_rekap_tangan(mentah["rr_2021"], "2021"))
    all_rows.extend(transform_rekap_tangan(mentah["rr_2022"], "2022"))

    df_silver = pd.DataFrame(all_rows)
    # Agregasi untuk memastikan kunci unik
    df_silver = df_silver.groupby(
        ["sumber", "seri_kode", "wilayah_kode", "nama_wilayah", "periode", "jenis_periode", "rincian", "satuan", "_berkas_raw", "_sha256_raw"],
        as_index=False,
    )["nilai"].sum()

    SILVER_FILE.parent.mkdir(parents=True, exist_ok=True)
    df_silver.to_parquet(SILVER_FILE, index=False)
    print(f"Silver tersimpan di {SILVER_FILE} ({len(df_silver)} baris)")
    return df_silver
