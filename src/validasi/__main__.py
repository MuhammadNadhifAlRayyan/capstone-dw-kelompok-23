"""Titik masuk eksekusi langsung modul validasi: python -m src.validasi"""
import sys
from src.validasi import jalankan
from src.common.hasil import tulis_hasil

if __name__ == "__main__":
    hasil = jalankan()
    if "--catat" in sys.argv or "--hasil" in sys.argv or len(sys.argv) == 1:
        # Jika dijalankan langsung, otomatis catat metrik bila aturan lolos
        tulis_hasil(
            nim="124450063",
            metrik={
                "aturan_validasi": hasil["aturan_validasi"],
                "aturan_lolos": hasil["aturan_lolos"],
            },
        )
        print(f"\n[OK] Metrik artefak tercatat: aturan_validasi={hasil['aturan_validasi']} aturan_lolos={hasil['aturan_lolos']}")
        print("     Lokasi: results/124450063/metrics.json")
