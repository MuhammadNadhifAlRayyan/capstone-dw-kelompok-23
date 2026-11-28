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

## Berkas

- `data/gold/panel.parquet`: 5,244 baris (panjang, termasuk sel kosong).
- `data/gold/panel_lebar.parquet`: 608 baris x 16 kolom (hanya sel terisi; satu kolom per indikator, satuan per indikator di `docs/data-dictionary.md`).
