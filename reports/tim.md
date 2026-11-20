# Laporan tim — Kelompok 23, Kasus 23: Kerusakan dan kerugian akibat bencana

Status: draf akhir Sprint 1. Angka di bawah dapat dicek dari Silver, hasil di `reports/`, metrik, dan `log-keputusan.csv`.

### Ringkasan
Kasus ini memakai 14 seri BNPB dan 1 seri WDI. Dua seri luas lahan dari BNPB hanya punya data total nasional. Silver pertama berisi 18.187 baris dari 15 seri. Masalah utama yang ditemukan adalah bentuk berkas yang beragam, data provinsi yang tidak selalu lengkap, perbedaan rincian rumah rusak, serta banyaknya angka yang jauh berbeda dari nilai biasanya. Data nilai kerusakan dan kerugian berasal dari usulan rehabilitasi dan rekonstruksi, bukan catatan lengkap semua dampak bencana.

### Data dan lineage
Tim memproses 58 berkas mentah: 39 JSON BNPB, 15 XLSX, dan 4 JSON WDI. Jumlah baris mentah yang tercatat adalah 15.058. Silver berisi 18.187 baris, 15 seri, 40 jenis rincian, dan 39 wilayah (Indonesia serta 38 provinsi). Setiap baris Silver menyimpan nama berkas sumber dan SHA-256 untuk penelusuran ke [MANIFEST](../data/raw/MANIFEST.csv). Angka ekstraksi dan Silver dapat dicek di [metrik NIM 124450071](../results/124450071/metrics.json) dan [metrik NIM 124450048](../results/124450048/metrics.json).

### Masalah data dan penanganannya

| Masalah | Bukti di repo | Penanganan | Jumlah/dampak | Log |
|---|---|---|---:|---|
| Bentuk berkas berbeda | XLSX memakai judul bertingkat dan sel wilayah yang digabung. | Judul dibaca secara eksplisit; nama wilayah diteruskan ke baris berikutnya saat diperlukan. | 0 baris berubah | [K-003](../log-keputusan.csv) |
| Bagian panel kosong | [Grid 14 seri × 16 tahun × 38 provinsi](grid-provinsi-tahap-3.csv). `fasyankes_rusak` kosong untuk 1 provinsi (2021) dan 5 (2022) di [kelengkapan panel](kelengkapan-panel-per-tahun.csv). | Tahun tanpa sumber provinsi dibedakan dari data yang benar-benar kosong. Bagian kosong tidak diisi nol. | [8.512 sel grid](grid-provinsi-tahap-3.csv); 1 dan 5 sel kosong | [K-006](../log-keputusan.csv), [K-010–K-011](../log-keputusan.csv) |
| Provinsi belum terbentuk | Data untuk [62 sel sebelum provinsi dibentuk](grid-provinsi-tahap-3.csv) tetap disimpan di `nilai_sumber_asli` untuk pemeriksaan, tetapi tidak dipakai sebagai nilai analisis. | Provinsi baru hanya dihitung sejak tahun terbentuk; Indonesia disimpan terpisah dari provinsi. | [514 baris terdampak](grid-provinsi-tahap-3.csv) | [K-001](../log-keputusan.csv), [K-007](../log-keputusan.csv) |
| Rincian rumah rusak berbeda | Sumber 2021–2022 memuat tingkat kerusakan, sedangkan sumber lain dapat hanya memuat total. | Nama kategori diseragamkan di [kamus rincian](kamus-rincian-rumah-rusak.csv). Total tetap dibedakan dari rincian; rincian yang tidak tersedia tidak dianggap nol. | [14.401 baris](rincian-rumah-rusak-harmonisasi.csv) menurut [K-008](../log-keputusan.csv) | [K-008](../log-keputusan.csv), [kamus rincian](kamus-rincian-rumah-rusak.csv) |
| Angka ekstrem dan perubahan tahunan | Ada [201 calon angka ekstrem](calon-anomali.csv). Tidak ditemukan salah input terbukti. Pada `rumah_rusak`, angka turun di 25 dari 33 provinsi (angka tengah turun ~22% < batas 50%) di [uji patahan](uji-patahan-seri.csv). | Angka ekstrem tetap disimpan. Angka tidak diperbaiki tanpa bukti dari sumber. | [201 calon](calon-anomali.csv); 0 angka diperbaiki; [0 patahan](uji-patahan-seri.csv) | [K-005](../log-keputusan.csv), [hasil profil](tahap-2-profil-anomali.md), [hasil uji patahan](uji-patahan-seri.csv) |
| Salinan dan revisi antarberkas | Dari [266 pasangan data 2024](audit-snapshot-2024.csv) yang dibandingkan, semuanya sama; tidak ada nilai berbeda. | Salinan sama hanya dihitung sekali. Jika ada nilai berbeda, keduanya harus ditelusuri sebelum memilih angka. | [228 salinan tidak dihitung ulang](audit-snapshot-2024.csv) | [K-004](../log-keputusan.csv), [audit snapshot](audit-snapshot-2024.csv) |
| Jumlah kabupaten/kota berbeda dari provinsi | Dari [1.456 pasangan](uji-agregasi-kabupaten-provinsi.csv), 1.294 cocok dan 162 berbeda. | Selisih dipertahankan dan tidak dikoreksi otomatis. | [162 pasangan berbeda](uji-agregasi-kabupaten-provinsi.csv) | [K-009](../log-keputusan.csv), [hasil uji agregasi](uji-agregasi-kabupaten-provinsi.csv) |
| Keterangan katalog belum tepat | Satuan dua seri luas belum tercatat; satuan WDI kosong; beberapa kode SDG ganda atau belum diisi. | Satuan luas ditetapkan sebagai hektar, WDI sebagai persen, dan kode SDG dibakukan di [katalog seri](../docs/seri.csv). Periode asli tetap di Silver; data diringkas per tahun di Gold. | 0 baris nilai diubah | [K-044–K-047](../log-keputusan.csv), [katalog seri](../docs/seri.csv) |

### Integrasi dan rekonsiliasi
Tiga pasangan sudah disiapkan di [pasangan-rekonsiliasi.md](pasangan-rekonsiliasi.md). Angka selisihnya akan diuji pada Sprint 2.

- P1: Rumah rusak akibat banjir pada baris Indonesia dibandingkan dengan jumlah 38 provinsi. Ada 16 tahun yang sama; nilainya diharapkan sama.
- P2: Rincian rumah rusak akibat banjir tahun 2025 dibandingkan dengan jumlah tingkat berat, sedang, dan ringan. Ada 1 tahun yang sama; jumlahnya diharapkan sama.
- P3: WDI tentang penduduk terdampak bencana dipakai sebagai konteks, bukan untuk menghitung selisih dengan jumlah rumah rusak. Tidak ada tahun yang sama.

Tabel nasional ada di [tabel-nasional.csv](tabel-nasional.csv).

### Validasi dan reproduksibilitas
Pemeriksaan skema Silver lolos: 18.187 baris, 15 seri, dan 39 wilayah. Metrik validasi mencatat 12 dari 12 aturan lolos dan 11 kolom terdokumentasi ([metrik validasi](../results/124450063/metrics.json)).

Silver juga dimuat ke SQLite, dengan 18.187 baris. Tim memilih SQLite karena mudah dijalankan secara lokal tanpa server. JSON mentah tetap disimpan sebagai sumber asli; SQLite lebih mudah dipakai untuk mencari data dengan kolom, tipe, dan kunci yang jelas. DDL, pemuat, dan alasan pilihan ada di [sqlite.py](../src/silver/sqlite.py) dan [dokumen penyimpanan](../docs/tahap-5-penyimpanan.md).

Catatan Sprint 1 menyebut langkah ekstraksi di `python pipeline.py` selesai dalam 1,5 detik. Waktu seluruh pipeline belum dicatat ([catatan Sprint 1](../sprint/sprint-1/124450071.md)).

### Pembagian kerja
Pembagian komponen mengikuti kesepakatan tim. Catatan pekerjaan Sprint 1 ada di [sprint/sprint-1/](../sprint/sprint-1), sedangkan metrik anggota ada di [results/](../results).
