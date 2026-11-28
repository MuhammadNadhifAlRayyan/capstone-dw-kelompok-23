# Panel Gold provinsi x periode x indikator

Dihasilkan `python pipeline.py` (`src/gold/panel.py`) dari Silver, grid, dan kategori anomali Sprint 1.

## Aturan satu nilai per sel

1. **Snapshot**: seri yang ada di dua snapshot memakai snapshot terbaru; angka snapshot lain dibandingkan di `reports/snapshot-bps.csv` (bila ada).
2. **Rincian**: satu indikator = satu deret utama (`total`, atau rincian di `DERET`). Rincian lain tetap di Silver.
3. **Berkas**: bila satu sel punya beberapa berkas, `URUTAN_BERKAS` memilih satu (`reports/deret-berkas.csv`).
4. **Periode**: disimpan apa adanya; tidak dirata-rata ke tahunan.
5. **Penanda**: outlier, patahan, dan galat input dari Sprint 1 ikut sebagai kolom `penanda`; nilainya tidak diubah.

Baris Silver provinsi yang tidak masuk panel (rincian lain atau berkas lain): 14,988.

## Indikator

| indikator | satuan | periode | jumlah_periode | sel | terisi | ditandai |
|---|---|---|---|---|---|---|
| fasyankes_rusak [jumlah] | unit | 2010–2025 | 16 | 608 | 106 | 26 |
| jembatan_rusak [jumlah] | unit | 2010–2025 | 16 | 608 | 106 | 1 |
| kantor_rusak [jumlah] | unit | 2010–2025 | 16 | 608 | 106 | 9 |
| kejadian [jumlah] | kejadian | 2010–2025 | 16 | 608 | 608 | 62 |
| kios_toko_rusak [jumlah] | unit | 2010–2024 | 15 | 570 | 38 | 4 |
| nilai_kerugian [jumlah] | rupiah | 2015–2024 | 10 | 380 | 131 | 18 |
| nilai_kerusakan [jumlah] | rupiah | 2015–2024 | 10 | 380 | 131 | 14 |
| pabrik_rusak [jumlah] | unit | 2024 | 1 | 38 | 38 | 3 |
| rumah_ibadat_rusak [jumlah] | unit | 2010–2025 | 16 | 608 | 106 | 6 |
| rumah_rusak [jumlah] | unit | 2010–2025 | 16 | 608 | 144 | 7 |
| rumah_terendam [jumlah] | unit | 2021–2022 | 2 | 76 | 68 | 2 |
| satuan_pendidikan_rusak [jumlah] | unit | 2021–2025 | 4 | 152 | 106 | 6 |

## Status sel

| indikator | belum_ada | terisi | tidak_diterbitkan |
|---|---|---|---|
| fasyankes_rusak [jumlah] | 55 | 106 | 447 |
| jembatan_rusak [jumlah] | 55 | 106 | 447 |
| kantor_rusak [jumlah] | 55 | 106 | 447 |
| kejadian [jumlah] | 0 | 608 | 0 |
| kios_toko_rusak [jumlah] | 55 | 38 | 477 |
| nilai_kerugian [jumlah] | 26 | 131 | 223 |
| nilai_kerusakan [jumlah] | 26 | 131 | 223 |
| pabrik_rusak [jumlah] | 0 | 38 | 0 |
| rumah_ibadat_rusak [jumlah] | 55 | 106 | 447 |
| rumah_rusak [jumlah] | 55 | 144 | 409 |
| rumah_terendam [jumlah] | 8 | 68 | 0 |
| satuan_pendidikan_rusak [jumlah] | 8 | 106 | 38 |

`terisi` = ada angka; kategori lain berasal dari grid Sprint 1 (`reports/kelengkapan-panel.md`). Sel kosong tidak diisi: tidak ada interpolasi di Gold.

## Berkas dan Rekonsiliasi dengan SQL

- `data/gold/panel.parquet`: 5.244 baris (panjang, memuat 1.688 sel terisi dan 3.556 sel kosong berkategori).
- `data/gold/panel_lebar.parquet`: 608 baris x 16 kolom (pivot dari sel terisi: 38 provinsi x 16 periode 2010–2025).

### Rekonsiliasi Baris Panel Parquet vs SQL Gold

| Berkas / Tabel | Media | Jumlah Baris | Penjelasan & Rujukan |
|---|---|---|---|
| `data/gold/panel.parquet` | Parquet (Panjang) | **5,244** | Panel provinsi x periode x 12 indikator (`baris_gold` pada metrik NIM 124450048) |
| `data/gold/panel_lebar.parquet` | Parquet (Lebar) | **608** | Pivot dari 1,688 sel terisi (38 provinsi x 16 periode) |
| `gold_panel` | DuckDB Table | **5,244** | Tabel relasional hasil muat langsung dari `panel.parquet` (PK: `indikator, wilayah_kode, periode`) |
| `gold_nasional` | DuckDB Table | **28** | Tabel seri nasional (`nasional.parquet`) |
| `rekonsiliasi` | DuckDB Table | **33** | Tabel pasangan rekonsiliasi BNPB vs WDI (`rekonsiliasi.parquet`) |
| **Total Lapis Gold di DuckDB** | **DuckDB (Semua Tabel Gold)** | **5.305** | **Agregat: 5,244 (`gold_panel`) + 28 (`gold_nasional`) + 33 (`rekonsiliasi`)** (`baris_sql_gold` pada metrik NIM 124450071) |

#### Pembuktian Himpunan Baris Identik

Himpunan baris pada `data/gold/panel.parquet` dan tabel `gold_panel` di DuckDB terbukti **100% identik** (tidak ada sel yang hilang, berubah, atau duplikat):
1. **Validasi Pipeline Otomatis**: Fungsi `_muat()` pada `src/gold/muat_sql.py` memvalidasi `n == len(df)` saat pipeline berjalan; perbedaan baris akan langsung menghentikan pipeline (`AssertionError`).
2. **Uji Selisih Himpunan (EXCEPT)**: Perbandingan dua arah antara `read_parquet('data/gold/panel.parquet')` dan `gold_panel` di DuckDB menghasilkan tepat 0 selisih.
3. **Keterkaitan Metrik**: `baris_gold: 5244` pada NIM 124450048 merujuk secara presisi ke panel provinsi `panel.parquet` / `gold_panel`, sedangkan `baris_sql_gold: 5305` pada NIM 124450071 merujuk ke total seluruh tabel lapis Gold di SQL.

### Rekonsiliasi Baris Panel Parquet vs SQL Gold

| Berkas / Tabel | Media | Jumlah Baris | Penjelasan & Rujukan |
|---|---|---|---|
| `data/gold/panel.parquet` | Parquet (Panjang) | **5.244** | Panel provinsi x periode x 12 indikator (`baris_gold` pada metrik NIM 124450048) |
| `data/gold/panel_lebar.parquet` | Parquet (Lebar) | **608** | Pivot dari 1.688 sel terisi (38 provinsi x 16 periode) |
| `gold_panel` | DuckDB Table | **5.244** | Tabel relasional hasil muat langsung dari `panel.parquet` (PK: `indikator, wilayah_kode, periode`) |
| `gold_nasional` | DuckDB Table | **28** | Tabel seri nasional (`nasional.parquet`) |
| `rekonsiliasi` | DuckDB Table | **33** | Tabel pasangan rekonsiliasi BNPB vs WDI (`rekonsiliasi.parquet`) |
| **Total Lapis Gold di DuckDB** | **DuckDB (Semua Tabel Gold)** | **5.305** | **Agregat: 5.244 (`gold_panel`) + 28 (`gold_nasional`) + 33 (`rekonsiliasi`)** (`baris_sql_gold` pada metrik NIM 124450071) |

#### Pembuktian Himpunan Baris Identik

Himpunan baris pada `data/gold/panel.parquet` dan tabel `gold_panel` di DuckDB terbukti **100% identik** (tidak ada sel yang hilang, berubah, atau duplikat):
1. **Validasi Pipeline Otomatis**: Fungsi `_muat()` pada `src/gold/muat_sql.py` memvalidasi `n == len(df)` saat pipeline berjalan; perbedaan baris akan langsung menghentikan pipeline (`AssertionError`).
2. **Uji Selisih Himpunan (EXCEPT)**:
   ```sql
   -- Selisih Parquet terhadap DuckDB = 0
   SELECT count(*) FROM (
       SELECT indikator, seri_kode, rincian, wilayah_kode, periode, status_sel, nilai 
       FROM read_parquet('data/gold/panel.parquet')
       EXCEPT
       SELECT indikator, seri_kode, rincian, wilayah_kode, periode, status_sel, nilai 
       FROM gold_panel
   ); -- Hasil: 0

   -- Selisih DuckDB terhadap Parquet = 0
   SELECT count(*) FROM (
       SELECT indikator, seri_kode, rincian, wilayah_kode, periode, status_sel, nilai 
       FROM gold_panel
       EXCEPT
       SELECT indikator, seri_kode, rincian, wilayah_kode, periode, status_sel, nilai 
       FROM read_parquet('data/gold/panel.parquet')
   ); -- Hasil: 0
   ```
3. **Keterkaitan Metrik**:
   - `results/124450048/metrics.json` mencatat `baris_gold: 5244` (fokus pada panel provinsi yang dihasilkan di Tahap 4).
   - `results/124450071/metrics.json` mencatat `baris_sql_gold: 5305` (fokus pada total baris seluruh tabel lapis Gold di DuckDB pada Tahap 5).
   - Kedua metrik berasal dari keluaran pipeline yang sama dan saling konsisten secara matematis.
