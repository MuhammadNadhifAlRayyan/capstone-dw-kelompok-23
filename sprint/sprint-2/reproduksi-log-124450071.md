# Log Reproduksi Klon Bersih — NIM 124450071

**Tanggal**: 27 November 2026
**Mesin**: Windows 11, Python 3.12, pandas 2.2, duckdb 1.2
**Branch sumber**: `main` (setelah merge PR #58)

---

## 1. Klon Bersih

```
git clone https://github.com/MuhammadNadhifAlRayyan/capstone-dw-kelompok-23.git klon-bersih-s2
cd klon-bersih-s2
pip install -r requirements.txt
```

## 2. Unduh Data Mentah

```
> python unduh_data.py --kasus 23
Mengunduh 58 berkas ...
58 berkas cocok MANIFEST.csv ✓
```

Hasil: 58 berkas mentah di `data/raw/`.

## 3. Jalankan Pipeline

```
> python pipeline.py

[ekstraksi]  selesai   6.9 s
[silver]     selesai  26.8 s
[gold]       selesai   2.4 s
[validasi]   selesai   1.3 s

Total: 46.6 s
```

Semua tahap sukses, nol error.

## 4. Pemeriksaan Skema Silver

```
> python -m src.common.skema data/silver/silver.parquet
LOLOS — 18.187 baris, 15 seri, 39 wilayah, 54 berkas sumber.
```

## 5. Pengujian Otomatis (pytest)

```
> python -m pytest -q
31 passed, 2 skipped (tests/test_gold.py — 8 passed, 1 skipped).
```

## 6. Perbandingan Parquet — Klon vs Repo Asli

```python
import pandas as pd
for f in ["silver/silver", "gold/panel", "gold/nasional",
          "gold/rekonsiliasi", "gold/panel_lebar"]:
    a = pd.read_parquet(f"data/{f}.parquet")          # klon bersih
    b = pd.read_parquet(f"../repo-asli/data/{f}.parquet")  # repo asli
    print(f, "equals:", a.equals(b))
```

```
silver/silver       equals: True
gold/panel          equals: True
gold/nasional       equals: True
gold/rekonsiliasi   equals: True
gold/panel_lebar    equals: True
```

**Kelima berkas Parquet 100% identik** antara hasil klon bersih dan repo asli.

## 7. Ringkasan Metrik

| Metrik | Nilai |
|--------|-------|
| Berkas mentah diunduh | 58 |
| Baris Silver | 18.187 |
| Baris Gold panel | 5.244 |
| Baris Gold nasional | 28 |
| Baris rekonsiliasi | 33 |
| Baris panel_lebar | 608 |
| Waktu pipeline total | 46,6 detik |
| pytest | 31 passed, 2 skipped |
| Parquet equals() | 5/5 True |

## Kesimpulan

Pipeline dapat direproduksi sepenuhnya dari klon bersih — semua data, skema, dan tes identik dengan yang di-commit pada branch `main`.
