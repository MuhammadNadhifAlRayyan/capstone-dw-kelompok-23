"""Tahap 8 — Validasi dan Dokumentasi (Milik Tim, Fokus NIM 124450063).

Modul ini bertanggung jawab memvalidasi mutu dataset di lapis Silver dan Gold:
1. Skema Pandera Silver (11 kolom wajib, tipe data, non-negatif, kode wilayah 38 provinsi).
2. Aturan Kamus Kategori Rincian Rumah Rusak (Check Pandera terhadap docs/data-dictionary.md).
3. Uji Penjumlahan Agregasi Kabupaten/Kota ke Provinsi vs Rekap Provinsi BNPB.
4. Lineage sha256 terhadap MANIFEST.csv.

Dapat dipanggil dari pipeline.py maupun dijalankan mandiri:
    python -m src.validasi
"""

import sys
from pathlib import Path
from typing import Any, Dict, Optional
import pandas as pd

from src.validasi.skema_silver import validasi_dataframe_silver
from src.validasi.agregasi import jalankan_semua_uji_agregasi
from src.common.hasil import tulis_hasil

ROOT = Path(__file__).resolve().parents[2]
SILVER_PATH = ROOT / "data" / "silver" / "silver.parquet"


def jalankan(silver: Optional[pd.DataFrame] = None, gold: Optional[Any] = None) -> Dict[str, Any]:
    """Menjalankan seluruh validasi Silver dan Agregasi.

    Args:
        silver: DataFrame Silver (jika None, membaca data/silver/silver.parquet bila ada)
        gold: Objek Gold (opsional untuk Sprint 1)

    Returns:
        Dict hasil validasi dan metrik untuk Workbench.
    """
    print("=" * 70)
    print("  TAHAP 8: VALIDASI MUTU DATASET (PANDERA & AGREGASI KASUS 23)")
    print("=" * 70)

    # 1. Baca Silver jika tidak diberikan langsung
    df_silver = silver
    if df_silver is None and SILVER_PATH.exists():
        print(f"[*] Membaca tabel Silver dari: {SILVER_PATH}")
        df_silver = pd.read_parquet(SILVER_PATH)

    aturan_diuji = 0
    aturan_lolos = 0
    laporan_skema = {}
    errors_skema = []

    # 2. Validasi Skema Silver
    if df_silver is not None:
        sukses_skema, errors_skema, laporan_skema = validasi_dataframe_silver(df_silver)
        aturan_diuji += len(laporan_skema)
        aturan_lolos += sum(1 for v in laporan_skema.values() if v)

        print("\n--- [1] Hasil Evaluasi Skema Pandera Silver ---")
        for aturan, lolos in laporan_skema.items():
            status = "LOLOS " if lolos else "GAGAL "
            print(f"  [{status}] {aturan}")
        if errors_skema:
            print("\nCatatan Pelanggaran Skema:")
            for err in errors_skema:
                print(f"  - {err}")
    else:
        print("\n[!] Perhatian: data/silver/silver.parquet belum ditemukan.")
        print("    Validasi skema Pandera pada Silver ditangguhkan hingga Silver terbentuk.")

    # 3. Uji Agregasi Kabupaten/Kota ke Provinsi
    print("\n--- [2] Uji Agregasi Kabupaten/Kota ke Provinsi vs Rekap BNPB ---")
    sukses_agregasi, hasil_agregasi = jalankan_semua_uji_agregasi()

    # Terdapat 3 pengujian agregasi: 2021, 2022, 2024
    aturan_diuji += 3
    if hasil_agregasi[0]["cocok"]:
        aturan_lolos += 1
        print("  [LOLOS ] Rekap 2021: Sum Kab/Kota == Rekap Provinsi (Selisih = 0 unit)")
    else:
        print("  [GAGAL ] Rekap 2021: Ada selisih")

    if hasil_agregasi[1]["cocok"]:
        aturan_lolos += 1
        print("  [LOLOS ] Rekap 2022: Sum Kab/Kota == Rekap Provinsi (Selisih = 0 unit)")
    else:
        print("  [GAGAL ] Rekap 2022: Ada selisih")

    if hasil_agregasi[2]["cocok_nasional"]:
        aturan_lolos += 1
        print("  [LOLOS ] Rekap 2024: Sum Kab/Kota == Rekap Provinsi Nasional (Net Selisih = 0 unit)")
        print(f"           Catatan wilayah: {hasil_agregasi[2]['catatan']}")
    else:
        print("  [GAGAL ] Rekap 2024: Selisih nasional terdeteksi")

    print("\n" + "=" * 70)
    print(f"  RINGKASAN: {aturan_lolos}/{aturan_diuji} aturan validasi lolos.")
    print("=" * 70)

    ringkasan = {
        "aturan_validasi": aturan_diuji,
        "aturan_lolos": aturan_lolos,
        "sukses_skema": len(errors_skema) == 0 if df_silver is not None else False,
        "sukses_agregasi": sukses_agregasi,
        "detail_skema": laporan_skema,
        "detail_agregasi": hasil_agregasi,
    }
    return ringkasan


if __name__ == "__main__":
    hasil = jalankan()
    # Simpan metrik jika diminta
    if "--catat" in sys.argv or "--hasil" in sys.argv:
        tulis_hasil(
            nim="124450063",
            metrik={
                "aturan_validasi": hasil["aturan_validasi"],
                "aturan_lolos": hasil["aturan_lolos"],
            },
        )
        print("\n[OK] Metrik artefak berhasil disimpan ke results/124450063/metrics.json")
