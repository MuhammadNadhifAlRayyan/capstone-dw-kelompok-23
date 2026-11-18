# Data Dictionary — Kelompok 23 (Kerusakan dan Kerugian Akibat Bencana)

Dokumen ini mendefinisikan kamus data untuk tabel keluaran pipeline Capstone Data Wrangling.
Setiap angka dan tipe mengacu pada aturan baku *Langkah Kerja Capstone Data Wrangling* dan *Panduan Kasus 23*.

---

## 1. Tabel Silver: `data/silver/silver.parquet`

Skema minimal tabel Silver memuat 11 kolom wajib. Tabel ini menyimpan seluruh observasi mentah yang telah dirapikan, diseragamkan tipe dan kodenya, tanpa baris kosong (missing value), serta mempertahankan provenans (*lineage*) data mentah.

| Kolom | Tipe | Satuan / Format | Boleh Kosong | Rentang atau Nilai Sah | Asal (Berkas / Aturan) | Keterangan |
|---|---|---|---|---|---|---|
| `sumber` | string | — | Tidak | `bnpb`, `wdi` | Jalur folder `data/raw/` | Identitas produsen data |
| `seri_kode` | string | — | Tidak | 14 seri BNPB + 1 seri WDI (lihat daftar seri di bawah) | Dokumen KASUS.md | Kode unik indikator |
| `wilayah_kode` | int64 | Kode BPS $\times 100$ | Tidak | `9999` (Nasional) atau `1100`–`9700` (Provinsi) | Keputusan K-001 | Standar 38 provinsi tahun 2025 |
| `nama_wilayah` | string | — | Tidak | Nama provinsi terstandarisasi huruf kapital (misal: `ACEH`, `SUMATERA UTARA`), atau `INDONESIA` | Standardisasi nama wilayah | Ejaan diseragamkan antarberkas |
| `periode` | string | `YYYY` | Tidak | Regex `^\d{4}$` (contoh: `2010` s.d. `2025`) | Berkas mentah | Periode tahunan observasi |
| `jenis_periode` | string | — | Tidak | `tahun` | Aturan baku Silver | Kasus 23 berbasis agregasi tahunan |
| `rincian` | string | snake_case | Tidak | Terdaftar di Kamus Kategori Rincian (lihat Bagian 2) | Header / dimensi data mentah | Sub-kategori atau `total` jika agregat |
| `nilai` | float64 | Sesuai kolom `satuan` | Tidak | $\ge 0$ (khusus unit: bilangan bulat $\ge 0$) | Kolom observasi data mentah | Angka metrik; tidak boleh ada nilai negatif atau NaN |
| `satuan` | string | — | Tidak | `kejadian`, `unit`, `hektare`, `rupiah`, `persen` | Standardisasi satuan kasus | Satuan metrik yang dibakukan |
| `_berkas_raw` | string | Jalur relatif | Tidak | Jalur relatif terhadap `data/raw/` (terdaftar di `MANIFEST.csv`) | Fungsi pembaca ekstraksi | Provenans berkas sumber |
| `_sha256_raw` | string | Heksadesimal 64-karakter | Tidak | Cocok persis dengan hash di `data/raw/MANIFEST.csv` | `src.common.manifest.sha256_raw` | Sidik integritas berkas sumber |

### Contoh Penelusuran Silsilah (Lineage) Satu Baris Silver ke Berkas Mentah

Sesuai prinsip Capstone Data Wrangling bahwa *"Setiap angka punya jejak"*, setiap baris di `data/silver/silver.parquet` dapat dilacak secara deterministik ke sel asalnya di berkas mentah.

#### Contoh 1: Data Kerusakan Rumah Akibat Banjir di Provinsi Aceh (Tahun 2025)

Baris pada tabel Silver:
```text
sumber        : bnpb
seri_kode     : rumah_rusak
wilayah_kode  : 1100
nama_wilayah  : ACEH
periode       : 2025
jenis_periode : tahun
rincian       : banjir
nilai         : 197638.0
satuan        : unit
_berkas_raw   : bnpb/2026-10-20/tangan/kompilasi-data-kejadian-dan-dampak-bencana-2025/43b83e79-c8b6-4b9a-b2f0-d1cbd9cfa636-jumlah-rumah-rusak-akibat-bencana-menurut-provinsi-2025.xlsx
_sha256_raw   : 7b953507dab9dc861030f8e1bd8feaf69cc6c7479c0efbe9643b4ac761357912
```

**Langkah Penelusuran Rekonstruksi (*Audit Trail*)**:
1. **Verifikasi Integritas Berkas Sumber**:
   Ambil jalur `_berkas_raw`. Buka `data/raw/MANIFEST.csv` baris ke-53:
   `bnpb/2026-10-20/tangan/kompilasi-data-kejadian-dan-dampak-bencana-2025/43b83e79-c8b6-4b9a-b2f0-d1cbd9cfa636-jumlah-rumah-rusak-akibat-bencana-menurut-provinsi-2025.xlsx,18955,7b953507dab9dc861030f8e1bd8feaf69cc6c7479c0efbe9643b4ac761357912`
   Nilai SHA-256 pada baris Silver cocok identik dengan sidik berkas mentah asli.
2. **Lokasi Sel pada Berkas Mentah**:
   Buka berkas XLSX tersebut pada sheet `Rumah Rusak 2025`:
   - Baris 2 (Header): Kolom F memiliki nama `BANJIR`.
   - Baris 3 (Data Baris ke-1): Kolom B (`Kode Wilayah Provinsi`) bernilai `11`, Kolom C (`Provinsi`) bernilai `ACEH`.
   - Sel F3 (`BANJIR` untuk `ACEH`): Nilai mentah adalah `197638`.
3. **Penerapan Aturan Wrangling**:
   - Nilai sel `197638` diekstrak menjadi float `197638.0` pada kolom `nilai`.
   - Nama header `BANJIR` distandarisasi ke snake_case menjadi `banjir` pada kolom `rincian` (terdaftar di kamus kategori rincian).
   - Kode provinsi `11` dikonversi mengikuti keputusan `K-001` menjadi `1100` ($11 \times 100$) pada kolom `wilayah_kode`.
   - Kolom `satuan` ditetapkan sebagai `unit` sesuai dokumen `KASUS.md`.

---

---

## 2. Kamus Kategori Rincian (*seri_kode = rumah_rusak*)

Untuk seri `rumah_rusak`, data mentah memiliki dua model pelaporan yang berbeda antartahun:
1. **Tahun 2021 & 2022**: Berdasarkan **tingkat keparahan kerusakan**.
2. **Tahun 2024 & 2025**: Berdasarkan **jenis bencana alam**.
3. **Agregat Keseluruhan**: Nilai total kerusakan rumah tanpa pemecahan.

Seluruh nilai pada kolom `rincian` untuk `seri_kode == 'rumah_rusak'` **wajib** terdaftar pada salah satu kategori sah di bawah ini:

| Nilai Baku `rincian` | Dimensi Asal di Data Mentah | Kategori Klasifikasi | Definisi / Keterangan |
|---|---|---|---|
| `total` | Total Keseluruhan | Agregat | Total seluruh rumah rusak pada wilayah dan periode terkait |
| `rusak_berat` | `Rumah Rusak Berat` | Tingkat Kerusakan | Rumah roboh atau rusak parah pada struktur utama sehingga tidak layak huni |
| `rusak_sedang` | `Rumah Rusak Sedang` | Tingkat Kerusakan | Kerusakan pada dinding pemikul atau atap, namun struktur utama masih kokoh |
| `rusak_ringan` | `Rumah Rusak Ringan` | Tingkat Kerusakan | Kerusakan non-struktural (penutup atap, plesteran, kaca jendela) |
| `banjir` | `BANJIR` | Jenis Bencana | Rumah rusak terendam atau terhantam arus banjir / genangan |
| `cuaca_ekstrem` | `CUACA EKSTREM` | Jenis Bencana | Rumah rusak akibat angin kencang / angin puting beliung |
| `gempa_bumi` | `GEMPABUMI` | Jenis Bencana | Rumah rusak akibat goncangan atau getaran gempa bumi |
| `tanah_longsor` | `TANAH LONGSOR` | Jenis Bencana | Rumah rusak tertimbun atau terseret material longsoran lereng/tebing |
| `kebakaran_hutan_lahan` | `KEBAKARAN HUTAN DAN LAHAN` | Jenis Bencana | Rumah terbakar akibat kobaran kebakaran hutan dan lahan |
| `erupsigunungapi` | `ERUPSI GUNUNG API` | Jenis Bencana | Rumah rusak tertimpa lontaran batu pijar, abu vulkanik, atau awan panas |
| `gelombang_pasang_abrasi` | `GELOMBANG PASANG DAN ABRASI` | Jenis Bencana | Rumah rusak terhantam ombak pasang laut atau terkikis abrasi pantai |
| `kekeringan` | `KEKERINGAN` | Jenis Bencana | Rumah terdampak krisis air / retak struktur tanah akibat kekeringan ekstrem |
| `tsunami` | `TSUNAMI` | Jenis Bencana | Rumah hancur terhempas gelombang pasang tsunami |

> [!NOTE]
> Untuk seri di luar `rumah_rusak` (misalnya `fasyankes_rusak`, `jembatan_rusak`, `kantor_rusak`), nilai baku kolom `rincian` default adalah `total`, kecuali berkas mentah menyajikan breakdown jenis bencana tertentu.

---

## 3. Daftar Seri dan Satuan Baku

| Sumber | Kode Seri (`seri_kode`) | Satuan Baku (`satuan`) | Kode SDG | Periode Data | Granularitas Mentah |
|---|---|---|---|---|---|
| `bnpb` | `kejadian` | `kejadian` | — | 2010–2025 | Nasional, Provinsi, Kab/Kota |
| `bnpb` | `rumah_rusak` | `unit` | 1.5.2, 11.5.2 | 2010–2025 | Nasional, Provinsi, Kab/Kota |
| `bnpb` | `rumah_terendam` | `unit` | 1.5.2, 11.5.2 | 2021–2022 | Provinsi, Kab/Kota |
| `bnpb` | `fasyankes_rusak` | `unit` | 11.5.2 | 2010–2025 | Provinsi, Kab/Kota |
| `bnpb` | `satuan_pendidikan_rusak` | `unit` | 11.5.2 | 2021–2025 | Provinsi, Kab/Kota |
| `bnpb` | `jembatan_rusak` | `unit` | 11.5.2 | 2010–2025 | Provinsi, Kab/Kota |
| `bnpb` | `kantor_rusak` | `unit` | — | 2010–2025 | Provinsi |
| `bnpb` | `rumah_ibadat_rusak` | `unit` | — | 2010–2025 | Provinsi |
| `bnpb` | `kios_toko_rusak` | `unit` | 1.5.2, 11.5.2 | 2010–2024 | Provinsi, Kab/Kota |
| `bnpb` | `pabrik_rusak` | `unit` | 1.5.2, 11.5.2 | 2024 | Kab/Kota |
| `bnpb` | `luas_sawah_rusak` | `hektare` | 1.5.2, 11.5.2 | 2010–2024 | Nasional, Provinsi |
| `bnpb` | `luas_lahan_kebun_hutan_rusak` | `hektare` | 1.5.2, 11.5.2 | 2010–2024 | Nasional, Provinsi |
| `bnpb` | `nilai_kerugian` | `rupiah` | 1.5.2, 11.5.2 | 2015–2024 | Kab/Kota, Provinsi |
| `bnpb` | `nilai_kerusakan` | `rupiah` | 1.5.2, 11.5.2 | 2015–2024 | Kab/Kota, Provinsi |
| `wdi` | `EN.CLC.MDAT.ZS` | `persen` | — | 2009 | Nasional |

---

## 4. Tabel Gold: `data/gold/gold_panel.parquet` (Direncanakan Sprint 2)

| Kolom | Tipe | Satuan / Format | Boleh Kosong | Rentang atau Nilai Sah | Keterangan |
|---|---|---|---|---|---|
| `wilayah_kode` | int64 | Kode BPS $\times 100$ | Tidak | `1100`–`9600` | 38 Provinsi tahun 2025 |
| `nama_wilayah` | string | — | Tidak | Nama provinsi kapital | Ejaan kanonik |
| `periode` | string | `YYYY` | Tidak | 2010–2025 | Rentang analisis |
| `kejadian` | float64 | kejadian | Ya | $\ge 0$ | Total kejadian bencana |
| `rumah_rusak_total` | float64 | unit | Ya | $\ge 0$ | Total rumah rusak gabungan |
| `rumah_rusak_berat` | float64 | unit | Ya | $\ge 0$ | Rumah rusak berat |
| `rumah_rusak_sedang` | float64 | unit | Ya | $\ge 0$ | Rumah rusak sedang |
| `rumah_rusak_ringan` | float64 | unit | Ya | $\ge 0$ | Rumah rusak ringan |
| `fasyankes_rusak` | float64 | unit | Ya | $\ge 0$ | Fasilitas kesehatan rusak |
| `satuan_pendidikan_rusak`| float64 | unit | Ya | $\ge 0$ | Sekolah / pendidikan rusak |
| `jembatan_rusak` | float64 | unit | Ya | $\ge 0$ | Jembatan rusak |
| `kantor_rusak` | float64 | unit | Ya | $\ge 0$ | Perkantoran rusak |
| `rumah_ibadat_rusak` | float64 | unit | Ya | $\ge 0$ | Sarana ibadah rusak |
| `nilai_kerusakan` | float64 | rupiah | Ya | $\ge 0$ | Nilai kerusakan aset fisik |
| `nilai_kerugian` | float64 | rupiah | Ya | $\ge 0$ | Nilai kerugian arus ekonomi |
