# AI_LOG — Kelompok 23

Satu baris per pemakaian AI yang bermakna (ChatGPT, Claude, Copilot, Bravais, dan sejenisnya).
Ringkas dan jujur; transkrip penuh tidak diminta. Yang dinilai bukan "pakai AI atau tidak",
melainkan "mengerti atau tidak" — isi kolom terakhir dengan apa yang Anda ubah dari keluarannya.

| Tanggal | Siapa (NIM) | Alat | Untuk apa | Apa yang diubah dari keluarannya |
|---|---|---|---|---|
| 2026-11-12 | 124450071 | ChatGPT | Penyusunan template script verifikasi SHA-256 dan ekstraksi batch | Menyesuaikan struktur direktori lokal kasus 23 dan memadukan pembacaan manifest CSV dengan skrip unduh |
| 2026-11-13 | 124450044 | Antigravity AI | Mengatasi batasan MAX_PATH Windows serta membangun modul pembaca XLSX, JSON Datastore, CKAN, dan WDI dengan lineage | Memverifikasi multi-level header XLSX, memastikan forward-fill pada merged cells wilayah, memvalidasi paginasi JSON datastore, dan mengintegrasikan orkestrasi ekstraksi di pipeline |
| 2026-11-15 | 124450091 | Claude | Skrip deteksi anomali (Tahap 2-3) dan visualisasi boxplot per seri | Mengganti metode deteksi outlier dari IQR murni ke ambang domain bencana, serta mengelompokkan grafik ke subfolder reports/gambar/ |
| 2026-11-17 | 124450080 | GitHub Copilot | Implementasi fungsi rekonsiliasi numerik Tahap 6 dan unit test nasional | Mengoreksi logika perbandingan agregat provinsi vs total nasional serta menyusun toleransi deviasi numerik |
| 2026-11-18 | 124450063 | ChatGPT | Aturan validasi schema Pandera dan penelusuran lineage baris ke berkas raw | Menyesuaikan tipe data nullable string dan float64 pada kolom nilai serta menyelaraskan kamus kategori di data-dictionary.md |
| 2026-11-18 | 124450048 | Claude | Standardisasi katalog 15 seri kanonik, penetapan kode SDG, dan penyusunan pipeline Silver | Mengoreksi satuan luas ke hektar, memetakan 38 kode provinsi BPS, dan memastikan skema Silver bebas kunci kembar |
| 2026-11-24 | 124450080 | Antigravity AI | Pembuatan tabel rekonsiliasi Tahap 6 di data/gold/rekonsiliasi.parquet dan sinkronisasi metrik | Menyesuaikan kategori penjelasan selisih (tanpa pasangan, tidak berselisih, definisi berbeda), memastikan WDI sebagai konteks, dan memutakhirkan metrik hasil Sprint 2 |
| 2026-11-25 | 124450080 | Antigravity AI | Penyusunan draf bagian Integrasi dan rekonsiliasi pada reports/tim.md (Tugas #28) | Menyederhanakan deskripsi tabel pasangan rekonsiliasi, merangkum median selisih (0.0%), dan menautkan rujukan angka ke data/gold/rekonsiliasi.parquet |
| 2026-11-25 | 124450048 | Claude | Pembentukan panel Gold provinsi 12 indikator, penanganan sel kosong, dan evaluasi skema | Memastikan aturan satu nilai per sel snapshot terbaru, mempertahankan penanda anomali Sprint 1, dan meloloskan 10 aturan validasi Gold |
| 2026-11-24 | 124450071 | Antigravity AI | Integrasi DDL SQL (DuckDB) untuk Silver dan Gold, uji primary key, serta dokumentasi di reports/tim.md (Tugas #23) | Memverifikasi kecocokan jumlah baris SQL dengan Parquet (18.187 Silver, 5.305 Gold, 43 JSON), menguji ConstraintException, dan merangkum alasan pemilihan DuckDB |
| 2026-11-27 | 124450071 | Antigravity AI | Uji reproduksi klon bersih sampai Gold, pembaruan DEMO.md Sprint 2, dan catatan Sprint 2 (Tugas #29) | Menyesuaikan perintah verifikasi DuckDB/Parquet untuk PowerShell Windows dan memvalidasi kesamaan 5 berkas Parquet hasil jalan ulang |

