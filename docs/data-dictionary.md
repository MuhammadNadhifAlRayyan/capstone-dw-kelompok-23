# Data Dictionary — Kelompok 23 (Kerusakan dan Kerugian Akibat Bencana)

Dokumen ini mendefinisikan kamus data resmi seluruh seri, kolom, tipe, satuan baku, dan pemetaan indikator SDG untuk Kasus 23 (Klaster G. Bencana - BNPB).

---

## 1. Kamus Master Seri (15 Seri Kasus 23)

Pemeriksaan menyeluruh terhadap 58 berkas mentah (39 JSON datastore/CKAN BNPB, 15 XLSX BNPB, dan 4 JSON WDI) menetapkan satu satuan resmi dan satu kode SDG kanonik per seri, serta menyelesaikan ketidaksesuaian pada katalog awal:

| No | Kode Seri | Sumber | Nama Resmi Seri Mentah | Kode SDG Awal | Kode SDG Kanonik | Satuan Awal | Satuan Baku Resmi | Periode | Tingkat Wilayah | Dasar Rujukan & Penetapan |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `kejadian` | BNPB | Jumlah Kejadian Bencana Menurut Provinsi / Kabupaten / Rekapitulasi | — | — | kejadian | `kejadian` | 2010–2025 | Provinsi, Kab/Kota, Nasional | Frekuensi kejadian bencana alam; dasar pemicu (event counter) pada Sendai Framework; tidak memiliki kode numerik SDG langsung. |
| 2 | `rumah_rusak` | BNPB | Jumlah Rumah Rusak Akibat Bencana Menurut Provinsi / Rekapitulasi Kerusakan | 11.5.2\|1.5.2 | `11.5.2` | unit | `unit` | 2010–2025 | Provinsi, Kab/Kota, Nasional | Kerusakan fisik fasilitas perumahan permukiman (Sendai Framework Indikator C-4 & UN SDG 11.5.2). Satuan terverifikasi pada header XLSX 2021/2022 `(unit)`. |
| 3 | `rumah_terendam` | BNPB | Kerusakan - Rumah Terendam | 11.5.2\|1.5.2 | `11.5.2` | unit | `unit` | 2021–2022 | Provinsi, Kab/Kota | Fasilitas tempat tinggal terendam banjir sementara (Sendai B-4 & UN SDG 11.5.2). Satuan terverifikasi pada baris unit XLSX 2021/2022. |
| 4 | `fasyankes_rusak` | BNPB | Jumlah Fasilitas Pelayanan Kesehatan yang Rusak Akibat Bencana | 11.5.2 | `11.5.2` | unit | `unit` | 2010–2025 | Provinsi, Kab/Kota | Kerusakan infrastruktur kritis fasilitas kesehatan (Sendai Framework Indikator D-2 & UN SDG 11.5.2). Satuan: `unit`. |
| 5 | `satuan_pendidikan_rusak` | BNPB | Jumlah Satuan Pendidikan Rusak Akibat Bencana | 11.5.2 | `11.5.2` | unit | `unit` | 2021–2025 | Provinsi, Kab/Kota | Kerusakan infrastruktur kritis fasilitas pendidikan (Sendai Framework Indikator D-3 & UN SDG 11.5.2). Satuan: `unit`. |
| 6 | `jembatan_rusak` | BNPB | Jumlah Jembatan Rusak Akibat Bencana | 11.5.2 | `11.5.2` | unit | `unit` | 2010–2025 | Provinsi, Kab/Kota | Kerusakan infrastruktur transportasi publik penting (Sendai Framework Indikator D-4 & UN SDG 11.5.2). Satuan: `unit`. |
| 7 | `kantor_rusak` | BNPB | Jumlah Kantor yang Rusak Akibat Bencana | — | `11.5.2` | unit | `unit` | 2010–2025 | Provinsi, Kab/Kota | Kerusakan fasilitas dan gedung administrasi pelayanan publik dasar (Sendai Framework Indikator D-4 & UN SDG 11.5.2). Ditetapkan mengisi kode kosong `—`. |
| 8 | `rumah_ibadat_rusak` | BNPB | Jumlah Rumah Ibadat yang Rusak Akibat Bencana | — | `11.5.2` | unit | `unit` | 2010–2025 | Provinsi, Kab/Kota | Kerusakan sarana fasilitas sosial keagamaan masyarakat (Sendai Framework Indikator D-4 & UN SDG 11.5.2). Ditetapkan mengisi kode kosong `—`. |
| 9 | `kios_toko_rusak` | BNPB | Jumlah Kios / Toko yang Rusak Akibat Bencana | 11.5.2\|1.5.2 | `11.5.2` | unit | `unit` | 2010–2024 | Provinsi, Kab/Kota | Kerusakan fisik sarana komersial mikro perkotaan/permukiman (Sendai Framework D-4 / C-5 & UN SDG 11.5.2). Satuan: `unit`. |
| 10 | `pabrik_rusak` | BNPB | Jumlah Pabrik Rusak Akibat Bencana | 11.5.2\|1.5.2 | `11.5.2` | unit | `unit` | 2024 | Provinsi, Kab/Kota | Kerusakan fisik fasilitas industri/manufaktur (Sendai Framework D-4 / C-5 & UN SDG 11.5.2). Satuan: `unit`. |
| 11 | `luas_sawah_rusak` | BNPB | Luas Sawah yang Rusak Akibat Bencana | 11.5.2\|1.5.2 | `1.5.2` | tidak_ada | `hektar` | 2010–2024 | Nasional | Kerusakan areal tanaman pangan/pertanian (Sendai Framework Indikator C-2: Direct agricultural loss & UN SDG 1.5.2). Satuan dikoreksi dari `tidak_ada` menjadi `hektar` (ha) sesuai standar pelaporan BNPB/Kementan/BPS. |
| 12 | `luas_lahan_kebun_hutan_rusak` | BNPB | Luas Lahan, Kebun, dan Hutan yang Rusak Akibat Bencana | 11.5.2\|1.5.2 | `1.5.2` | tidak_ada | `hektar` | 2010–2024 | Nasional | Kerusakan areal perkebunan dan kehutanan produktif (Sendai Framework Indikator C-2 / C-5 & UN SDG 1.5.2). Satuan dikoreksi dari `tidak_ada` menjadi `hektar` (ha) sesuai standar KLHK/BNPB. |
| 13 | `nilai_kerugian` | BNPB | Nilai Kerusakan dan Kerugian Akibat Bencana (Pengajuan RRRP) | 11.5.2\|1.5.2 | `1.5.2` | rupiah | `rupiah` | 2015–2024 | Provinsi, Kab/Kota | Aliran ekonomi yang hilang / disrupsi finansial (losses) akibat bencana (Sendai Framework Indikator C-1 & UN SDG 1.5.2). Besaran nilai nominal dalam mata uang rupiah. |
| 14 | `nilai_kerusakan` | BNPB | Nilai Kerusakan dan Kerugian Akibat Bencana (Pengajuan RRRP) | 11.5.2\|1.5.2 | `1.5.2` | rupiah | `rupiah` | 2015–2024 | Provinsi, Kab/Kota | Nilai biaya kerusakan aset fisik langsung (direct damage) akibat bencana (Sendai Framework Indikator C-1 & UN SDG 1.5.2). Besaran nilai nominal dalam mata uang rupiah. |
| 15 | `EN.CLC.MDAT.ZS` | WDI | Droughts, floods, extreme temperatures (% of population, average 1990-2009) | — | `1.5.1` | — | `persen` | 2009 | Nasional (IDN) | Persentase populasi yang terdampak oleh bencana iklim (banjir, kekeringan, suhu ekstrem). Sumber WDI Source ID 46: Sustainable Development Goals. Satuan ditetapkan `persen` (% of population). |

---

## 2. Aturan Standar Periode & Wilayah

1. **Integritas Periode pada Lapis Silver**:
   - Observasi mentah dengan resolusi semesteran (`YYYY-S#`), triwulanan (`YYYY-Q#`), atau bulanan (`YYYY-MM`) **dilarang dirata-ratakan ke tahunan di Silver**.
   - Kolom `jenis_periode` wajib diisi sesuai resolusi aslinya (`tahun`, `semester`, `triwulan`, `bulan`).
   - Agregasi waktu (misalnya jumlah total tahunan atau perataan terkontrol) hanya boleh dilakukan di lapis Gold dengan aturan terdokumentasi (Log Keputusan K-047).
2. **Standardisasi Wilayah**:
   - `wilayah_kode = 9999` untuk Agregat Nasional (Indonesia).
   - `wilayah_kode = kode_BPS * 100` untuk 38 provinsi acuan tahun 2025 (misal 1100 Aceh, 9400 Papua).
   - Pemekaran wilayah dipertahankan apa adanya sejak tahun berdiri (Kalimantan Utara aktif mulai 2012, 4 provinsi Papua baru aktif mulai 2022) tanpa penggabungan retrospektif dengan bobot fiktif (Log Keputusan K-001 & K-007).

---

## 3. Spesifikasi Skema Tabel Silver (`data/silver/silver.parquet`)

Tabel Silver memuat 11 kolom wajib standar dengan kunci unik kombinasi: `['sumber', 'seri_kode', 'wilayah_kode', 'periode', 'rincian', '_berkas_raw']`.

| Kolom | Tipe Data | Format / Satuan | Boleh Kosong | Rentang / Nilai Sah | Rujukan Aturan | Deskripsi & Peran |
|---|---|---|---|---|---|---|
| `sumber` | string | teks kode | Tidak | `bnpb`, `wdi` | Struktur folder raw | Identitas produsen data primer. |
| `seri_kode` | string | snake_case | Tidak | 15 kode seri sah di Bagian 1 | Katalog Kasus 23 | Kode unik indikator bencana/pembanding. |
| `wilayah_kode` | int64 | numerik | Tidak | 9999, 1100–9700 | Log K-001, K-007 | Kode wilayah acuan susunan 38 provinsi BPS × 100 dan 9999 untuk nasional. |
| `nama_wilayah` | string | UPPERCASE | Tidak | Nama 38 provinsi baku / `INDONESIA` | Log K-001 | Nama kanonik wilayah administrasi. |
| `periode` | string | regex waktu | Tidak | `^\d{4}$` atau `^\d{4}-(0[1-9]\|1[0-2])$` | Log K-047, Skema Silver | Waktu observasi sesuai resolusi asli (tahun/bulan/semester). |
| `jenis_periode` | string | string | Tidak | `tahun`, `semester`, `triwulan`, `bulan` | Skema Silver | Dimensi temporal granularitas observasi. |
| `rincian` | string | string | Tidak | `total`, nama bencana (`BANJIR`, dll.), tingkat kerusakan (`berat`, dll.) | Log K-008 | Dimensi disagregasi kejadian/kerusakan. |
| `nilai` | float64 | numerik | Tidak | $\ge 0$ | Log K-002 | Besaran kuantitatif observasi (tidak menyimpan missing). |
| `satuan` | string | string | Tidak | `kejadian`, `unit`, `hektar`, `rupiah`, `persen` | Log K-044, K-045 | Satuan ukuran resmi terstandardisasi. |
| `_berkas_raw` | string | relative path | Tidak | Tercantum di `MANIFEST.csv` | Lineage Bronze | Jalur relatif berkas mentah asal observasi. |
| `_sha256_raw` | string | hex sha256 | Tidak | 64 karakter hex | `MANIFEST.csv` | Sidik integritas kriptografis berkas mentah. |

---

## 4. Spesifikasi Skema Panel Gold

1. **Panel Provinsi (`data/gold/panel_provinsi_bencana.parquet`)**:
   - Dimensi grid: 38 Provinsi × 16 Tahun (2010–2025) = 608 observasi per seri level provinsi.
   - Kolom: `wilayah_kode`, `nama_wilayah`, `tahun`, diikuti 10 kolom indikator tingkat provinsi (`kejadian`, `rumah_rusak`, `rumah_terendam`, `fasyankes_rusak`, `satuan_pendidikan_rusak`, `jembatan_rusak`, `kantor_rusak`, `rumah_ibadat_rusak`, `kios_toko_rusak`, `pabrik_rusak`, `nilai_kerugian`, `nilai_kerusakan`).
   - Transformasi moneter: Nilai rupiah tetap disimpan dalam nilai nominal asli (`rupiah`), serta kolom turunan terstandarisasi $\log(1 + x)$ untuk analisis ekonometrika rentang lebar.
2. **Tabel Seri Nasional (`data/gold/nasional_bencana.parquet`)**:
   - Memuat seri yang hanya tersedia pada agregat nasional (`luas_sawah_rusak`, `luas_lahan_kebun_hutan_rusak`, dan pembanding WDI `EN.CLC.MDAT.ZS`).
   - Menghindari percampuran seri nasional dan provinsi dalam satu panel tanpa kode wilayah yang benar.
