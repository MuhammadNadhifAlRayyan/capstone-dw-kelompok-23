# Laporan tim — Kelompok 23, Kasus 23: Kerusakan dan kerugian akibat bencana

Satu dokumen bersama, enam bagian. Angka harus dapat ditarik ulang dari `data/silver`, `data/gold`,
dan `log-keputusan.csv` yang sudah di-*commit*.

## Ringkasan
Kasus 23 membahas kerusakan dan kerugian akibat bencana di Indonesia bersumber dari BNPB (14 seri utama tingkat provinsi dan kabupaten/kota periode 2010–2025) serta pembanding nasional World Development Indicators (WDI `EN.CLC.MDAT.ZS`). Temuan awal menunjukkan heterogenitas format yang tinggi (JSON CKAN datastore dan spreadsheet Excel ber-header ganda), perbedaan tingkat granularitas wilayah (provinsi vs kabupaten/kota), adanya baris nasional (Indonesia) di dalam tabel provinsi yang memerlukan pemisahan eksplisit, serta sebaran nilai kerugian dan kerusakan dalam rupiah yang sangat lebar sehingga membutuhkan transformasi logaritma.

## Data dan lineage
Sumber dan format mentah terdiri atas 58 berkas (39 JSON datastore/CKAN BNPB, 15 XLSX rekapitulasi BNPB, dan 4 JSON WDI) dari snapshot 20 Oktober 2026. Setiap baris Silver menyimpan `_berkas_raw` dan `_sha256_raw` yang diverifikasi terhadap `data/raw/MANIFEST.csv`.

## Masalah data dan penanganannya
Temuan penting Sprint 1:

- **Bagian data yang kosong:** Tabel berisi 14 jenis data untuk 16 tahun dan 38 provinsi (8.512 kombinasi). Bagian kosong tidak selalu berarti datanya hilang: sumber mungkin tidak punya data provinsi, atau provinsinya belum terbentuk. Karena itu, bagian kosong tidak diisi nol (K-006–K-007). Contohnya, data `fasyankes_rusak` kosong untuk 1 provinsi pada 2021 dan 5 provinsi pada 2022 (K-010–K-011). Dua jenis data luas lahan hanya tersedia sebagai jumlah nasional ([profil seri](profil-per-seri.csv)). Data `nilai_kerugian` dan `nilai_kerusakan` juga belum lengkap: pada 2015 masing-masing hanya ada untuk 1 dari 34 provinsi, sedangkan pada 2024 hanya ada untuk 2 dari 38 provinsi ([kelengkapan panel](kelengkapan-panel-per-tahun.csv)).
- **Angka yang jauh berbeda:** Pemeriksaan menemukan 201 angka yang jauh berbeda dari biasanya (K-005). Angka-angka itu tetap disimpan karena belum ada bukti bahwa nilainya salah. Contohnya, jumlah `rumah_rusak` di Aceh pada 2025 adalah 198.082; angka ini bisa dihitung dari [Silver](../data/silver/silver.parquet) dan ada di [daftar calon anomali](calon-anomali.csv).
- **Perubahan besar:** Tidak ditemukan perubahan besar yang terjadi bersamaan di banyak provinsi. Untuk `rumah_rusak` dari 2021 ke 2022, angka turun di 25 dari 33 provinsi yang memiliki data pada kedua tahun. Namun, angka tengahnya hanya turun sekitar 22%, belum mencapai batas 50% ([hasil uji](uji-patahan-seri.csv), K-005).
- **Data kembar dan revisi:** Pada data 2024, 266 pasangan angka dibandingkan. Semuanya sama, jadi tidak ada revisi angka yang perlu dipilih. Sebanyak 228 salinan yang sama hanya dihitung sekali (K-004).
- **Perbaikan keterangan data:** Satuan dua jenis data luas diperbaiki menjadi hektar. Satuan WDI `EN.CLC.MDAT.ZS` ditetapkan sebagai persen. Kode SDG juga dibakukan: kerusakan fasilitas/infrastruktur memakai 11.5.2, kerugian ekonomi langsung memakai 1.5.2, dan WDI memakai 1.5.1 (K-044–K-046). Periode asli tetap disimpan di Silver; sesuai keputusan tim, data baru diringkas per tahun di Gold (K-047).

Angka dapat dicek di [`log-keputusan.csv`](../log-keputusan.csv), [`silver.parquet`](../data/silver/silver.parquet), [`profil-per-seri.csv`](profil-per-seri.csv), [`calon-anomali.csv`](calon-anomali.csv), [`uji-patahan-seri.csv`](uji-patahan-seri.csv), dan [`kelengkapan-panel-per-tahun.csv`](kelengkapan-panel-per-tahun.csv).

## Integrasi dan rekonsiliasi
Seri utama vs pembanding nasional: selisih, penjelasannya (definisi, metode, vintage, granularitas),
dan hasil analisis revisi dari arsip WDI.

## Penyimpanan Silver (draf Tahap 5)
Silver disimpan di SQLite karena ukuran kasus masih sesuai untuk basis data lokal satu berkas;
SQLite tidak memerlukan server/dependensi tambahan, mendukung transaksi, tipe kolom, dan kunci primer.
DuckDB lebih unggul untuk analitik kolumnar pada data besar, sementara PostgreSQL lebih cocok untuk
akses serentak banyak pengguna, tetapi keduanya menambah konfigurasi yang belum dibutuhkan. JSON
mentah tetap disimpan di Bronze karena mempertahankan bentuk respons dan atribut sumber; JSON lebih
fleksibel, tetapi query terstruktur, penegakan tipe, dan deduplikasi lebih sulit. Tabel Silver
menyimpan observasi ternormalisasi beserta hash dan jalur berkas sumber agar tetap dapat ditelusuri.

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

