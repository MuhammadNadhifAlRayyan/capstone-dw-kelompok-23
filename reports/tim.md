# Laporan tim — Kelompok 23, Kasus 23: Kerusakan dan kerugian akibat bencana

Status: draf revisi Sprint 1. Setiap angka utama dilengkapi dengan tautan ke baris data, keputusan, metrik, atau query yang dapat diulang. Silver Parquet tidak memiliki nomor baris tetap; untuk angka Silver, query di bawah memberi cara pemeriksaan yang deterministik.

### Ringkasan

Kasus 23 memuat 14 seri BNPB dan 1 seri pembanding WDI ([seluruh 15 seri di katalog](../docs/seri.csv#L2-L16)). Dua seri luas lahan BNPB tersedia pada tingkat nasional, bukan provinsi ([katalog seri, baris 12–13](../docs/seri.csv#L12-L13)). Silver berisi 18.187 baris untuk 15 seri, 40 nilai rincian, dan 39 wilayah. Temuan Sprint 1 mencakup kekosongan pada sebagian sel panel, rincian rumah rusak yang berbeda antarsumber, nilai ekstrem yang tidak otomatis dihapus, serta selisih pada sebagian pemeriksaan agregasi kabupaten/kota dengan provinsi.

### Data, lineage, dan pemeriksaan Silver

Manifest berisi 58 berkas: 39 JSON BNPB, 15 XLSX BNPB, dan 4 JSON WDI ([daftar berkas](../data/raw/MANIFEST.csv#L2-L59)). Metrik ekstraksi mencatat 58 berkas dibaca dan 15.058 baris mentah ([metrics NIM 124450044](../results/124450044/metrics.json#L2-L7); [metrics NIM 124450071](../results/124450071/metrics.json#L2-L13)).

Untuk memeriksa ringkasan Silver dari akar repositori, jalankan query DuckDB berikut pada [data/silver/silver.parquet](../data/silver/silver.parquet):

```sql
SELECT COUNT(*) AS baris_silver,
       COUNT(DISTINCT seri_kode) AS seri,
       COUNT(DISTINCT rincian) AS rincian,
       COUNT(DISTINCT wilayah_kode) AS wilayah
FROM read_parquet('data/silver/silver.parquet');
```

Hasil yang terverifikasi: **18.187 baris, 15 seri, 40 rincian, dan 39 wilayah**. Skema menyimpan `_berkas_raw` dan `_sha256_raw` untuk lineage setiap observasi ([data dictionary—skema dan lineage](../docs/data-dictionary.md#L5-L25)).

### Masalah data dan penanganannya

| Masalah | Bukti dan cara membaca angkanya | Penanganan | Keputusan |
|---|---|---|---|
| Bentuk berkas berbeda | XLSX memiliki header bertingkat dan sel wilayah gabungan. Log K-003 mencatat metode pembacaan dan `dampak_baris=0` ([baris K-003](../log-keputusan.csv#L4)). | Header dibaca bertingkat dan identitas wilayah diteruskan ke baris terkait; nilai mentah tidak dikoreksi. | [K-003](../log-keputusan.csv#L4) |
| Grid panel dan sel kosong | Grid memiliki **8.512 baris data**: 14 seri × 16 tahun (2010–2025) × 38 provinsi ([seluruh baris grid](grid-provinsi-tahap-3.csv#L2-L8513); [K-006](../log-keputusan.csv#L7)). Untuk `fasyankes_rusak`, kolom `sel_kosong_grid` bernilai 1 pada 2021 dan 5 pada 2022 ([rekap 2021–2022](kelengkapan-panel-per-tahun.csv#L13-L14); [K-010–K-011](../log-keputusan.csv#L11-L12)). | Tahun tanpa sumber provinsi dibedakan dari nilai kosong; nilai kosong tidak diisi nol. | [K-006](../log-keputusan.csv#L7), [K-010–K-011](../log-keputusan.csv#L11-L12) |
| Provinsi belum terbentuk | Pada grid, filter `status=wilayah_belum_terbentuk` menghasilkan **514 baris**; dari baris itu, **62** memiliki `nilai_sumber_asli` terisi ([baris grid](grid-provinsi-tahap-3.csv#L2-L8513)). | Nilai historis tetap tersedia untuk audit, tetapi nilai analisis provinsi tidak dipakai sebelum wilayah terbentuk. | [K-001](../log-keputusan.csv#L2), [K-007](../log-keputusan.csv#L8) |
| Rincian rumah rusak berbeda | Tabel harmonisasi saat ini berisi **14.392 baris data** ([baris 2–14.393](rincian-rumah-rusak-harmonisasi.csv#L2-L14393)); jumlah itu dihasilkan oleh `build_house_detail()` dan ditulis ke laporan melalui `len(house_detail)` ([fungsi pembentuk](../src/panel_kelengkapan.py#L547), [penulisan laporan](../src/panel_kelengkapan.py#L949)). K-008 masih menyimpan angka lama 14.401; K-049 mencatat koreksinya ([K-008](../log-keputusan.csv#L9), [K-049](../log-keputusan.csv#L50)). | Alias jenis bencana disatukan. Total dibedakan dari tingkat berat/sedang/ringan; rincian yang tidak tersedia tidak dianggap nol. | [kamus rincian](kamus-rincian-rumah-rusak.csv), [K-008](../log-keputusan.csv#L9), [K-049](../log-keputusan.csv#L50) |
| Angka ekstrem dan perubahan tahunan | [Calon-anomali.csv baris 2–202](calon-anomali.csv#L2-L202) berisi **201 calon anomali**. Untuk `rumah_rusak` 2021–2022, [baris 37 uji patahan](uji-patahan-seri.csv#L37) mencatat 33 provinsi berpasangan, 25 turun, median 677 menjadi 530 (turun 21,7%); ambang 50% tidak terpenuhi. Kolom `ambang_patahan_terpenuhi` pada seluruh hasil uji bernilai False ([hasil uji](uji-patahan-seri.csv#L2-L40)). | Tidak ada nilai yang dinyatakan salah hanya karena ekstrem; tidak ada koreksi nilai tanpa bukti sumber. | [K-005](../log-keputusan.csv#L6) |
| Salinan dan revisi antarberkas | [Audit snapshot baris 2–267](audit-snapshot-2024.csv#L2-L267) berisi 266 pasangan 2024; seluruh statusnya “identik; satu nilai dipakai”. K-004 mencatat 228 salinan lintas snapshot tidak dihitung ulang ([baris K-004](../log-keputusan.csv#L5)). | Salinan identik dihitung sekali. Nilai berbeda harus ditelusuri sebelum diputuskan sebagai revisi. | [K-004](../log-keputusan.csv#L5) |
| Agregat kabupaten/kota dan provinsi berbeda | [Audit agregasi baris 2–1.457](uji-agregasi-kabupaten-provinsi.csv#L2-L1457) berisi 1.456 pasangan: 1.294 berstatus `cocok` dan 162 `berbeda` ([baris K-009](../log-keputusan.csv#L10)). | Selisih dipertahankan dan tidak dikoreksi otomatis. | [K-009](../log-keputusan.csv#L10) |
| Metadata satuan, SDG, dan periode | Keputusan K-044–K-047 masing-masing mendokumentasikan satuan luas, satuan WDI, kode SDG kanonik, dan integritas periode ([baris K-044–K-047](../log-keputusan.csv#L45-L48)); kolom `dampak_baris` pada keputusan tersebut bernilai 0. | Satuan dan kode ditetapkan berdasarkan metadata/bukti yang dicatat; periode asli tidak dirata-ratakan ke tahunan di Silver. | [K-044–K-047](../log-keputusan.csv#L45-L48) |

### Integrasi dan rekonsiliasi

Tiga pasangan disiapkan: P1 dan P2 untuk uji selisih; P3 untuk konteks WDI. Rujukan periode irisan adalah [ringkasan pasangan](pasangan-rekonsiliasi.md#ringkasan-pasangan) dan metrik NIM 124450071 (`irisan_p1=16`, `irisan_p2=1`, `irisan_p3=0`; [baris metrik](../results/124450071/metrics.json#L2-L9)).

- P1 membandingkan rumah rusak akibat banjir pada baris nasional dengan jumlah provinsi; 16 tahun beririsan.
- P2 membandingkan total rumah rusak banjir 2025 dengan jumlah tingkat berat, sedang, dan ringan; 1 tahun beririsan.
- P3 membandingkan konsep berbeda sebagai konteks, bukan sebagai selisih; tidak ada tahun beririsan.

Nilai selisihnya direncanakan untuk diuji pada Sprint 2. Tabel nasional tersedia di [tabel-nasional.csv](tabel-nasional.csv).

### Validasi dan reproduksibilitas

Validasi skema mencatat **12 dari 12 aturan lolos** dan **11 kolom terdokumentasi** ([metrics NIM 124450063](../results/124450063/metrics.json#L2-L7)). Jumlah baris, seri, dan wilayah Silver dapat diperiksa dengan query di atas. Pemuatan SQLite juga menghasilkan 18.187 baris ([hasil pemuatan](../docs/tahap-5-penyimpanan.md#L59-L65)); pilihan dan skemanya dijelaskan di [pemuat SQLite](../src/silver/sqlite.py).

Catatan Sprint 1 melaporkan langkah ekstraksi selesai dalam 1,5 detik; itu waktu langkah ekstraksi, bukan waktu seluruh pipeline ([catatan NIM 124450071](../sprint/sprint-1/124450071.md#L18)).

### Pembagian kerja

Catatan pekerjaan Sprint 1 tersedia di [folder sprint](../sprint/sprint-1/); metrik anggota tersedia di [folder results](../results/).
