# Laporan tim — Kelompok 23, Kasus 23: Kerusakan dan kerugian akibat bencana

Satu dokumen bersama, enam bagian. Angka harus dapat ditarik ulang dari `data/silver`, `data/gold`,
dan `log-keputusan.csv` yang sudah di-*commit*.

## Ringkasan
Kasus 23 membahas kerusakan dan kerugian akibat bencana di Indonesia bersumber dari BNPB (14 seri utama tingkat provinsi dan kabupaten/kota periode 2010–2025) serta pembanding nasional World Development Indicators (WDI `EN.CLC.MDAT.ZS`). Temuan awal menunjukkan heterogenitas format yang tinggi (JSON CKAN datastore dan spreadsheet Excel ber-header ganda), perbedaan tingkat granularitas wilayah (provinsi vs kabupaten/kota), adanya baris nasional (Indonesia) di dalam tabel provinsi yang memerlukan pemisahan eksplisit, serta sebaran nilai kerugian dan kerusakan dalam rupiah yang sangat lebar sehingga membutuhkan transformasi logaritma.

## Data dan lineage
Sumber dan format mentah terdiri atas 58 berkas (39 JSON datastore/CKAN BNPB, 15 XLSX rekapitulasi BNPB, dan 4 JSON WDI) dari snapshot 20 Oktober 2026. Setiap baris Silver menyimpan `_berkas_raw` dan `_sha256_raw` yang diverifikasi terhadap `data/raw/MANIFEST.csv`.

## Masalah data dan penanganannya
Tabel masalah yang ditemukan (missing, outlier, patahan seri, duplikat, format, wilayah) dengan
jumlah baris terdampak, keputusan, dan alternatif yang ditolak. Rujuk id di `log-keputusan.csv`.

## Integrasi dan rekonsiliasi
Seri utama vs pembanding nasional: selisih, penjelasannya (definisi, metode, vintage, granularitas),
dan hasil analisis revisi dari arsip WDI.

## Validasi dan reproduksibilitas
Skema validasi (aturan, hasil lolos/gagal), waktu `python pipeline.py` dari nol, perbandingan pandas
vs DuckDB/Dask, dan keterbatasan yang tersisa.

## Pembagian kerja
| Anggota | NIM | Komponen | Tugas sampingan | Bagian laporan yang ditulis |
|---|---|---|---|---|
| Nabila Nur Azizah | 124450048 | Transformasi dan panel (Tahap 4) | Koordinator | Ringkasan, Struktur & Skema Panel Gold |
| Fernando Dimetrius Barus | 124450063 | Validasi dan dokumentasi (Tahap 8) | Penjaga Data & Evaluasi | Validasi dan reproduksibilitas |
| Abigael Limbong | 124450080 | Integrasi, penyimpanan, dan skala (Tahap 5–7) | Analis Utama | Integrasi dan rekonsiliasi |
| Muhammad Nadhif Al Rayyan | 124450071 | Ekstraksi, profil, dan pembersihan (Tahap 1–3) | Integrator & Reproduksi | Data dan lineage, Masalah data |

