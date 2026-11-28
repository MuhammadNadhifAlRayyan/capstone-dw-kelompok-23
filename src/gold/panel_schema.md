# Rancangan Struktur Panel Gold: Kasus 23 (Kerusakan dan Kerugian Akibat Bencana)

**Capstone Data Wrangling 2026/2027 — Kelompok 23 (Klaster G. Bencana BNPB; SDG 1, 11)**  
**Penanggung Jawab:** Nabila Nur Azizah (NIM: 124450048) — Koordinator / Fokus Transformasi dan Panel (Tahap 4)

---

## 1. Tujuan dan Ruang Lingkup
Menyusun arsitektur dan skema pembentukan tabel **Gold** dalam format panel terstruktur:
$$\text{Panel Gold: } 38 \text{ Provinsi} \times \text{Periode (2010–2025)} \times \text{Indikator Bencana}$$
yang siap untuk analisis statistik, pemodelan deret waktu/panel, serta rekonsiliasi terhadap indikator pembanding nasional (WDI `EN.CLC.MDAT.ZS`).

---

## 2. Dimensi dan Unit Observasi
- **Unit Observasi (Primary Key Panel):** Gabungan `(wilayah_kode, tahun)` yang unik per baris.
  - Setiap baris merepresentasikan 1 provinsi pada 1 tahun pengamatan.
- **Dimensi Wilayah:** 38 Provinsi di Indonesia sesuai standar BPS tahun 2025 (`wilayah_kode = kode_BPS \times 100`):
  - 1100: ACEH s.d. 9700: PAPUA PEGUNUNGAN.
  - Kode `9999`: INDONESIA (agregat nasional) dipisahkan ke tabel tersendiri (`gold_nasional.parquet`) untuk menjaga integritas panel provinsi.
- **Dimensi Waktu (Periode):** Tahunan (`jenis_periode = 'tahun'`) dengan rentang tahun kanonik 2010 hingga 2025 (16 tahun).
  - Total ukuran grid dasar: $38 \text{ provinsi} \times 16 \text{ tahun} = 608 \text{ baris observasi}$.

---

## 3. Matriks Ketersediaan Seri Utama (14 Seri BNPB)

| No | Kode Seri | Cakupan Tahun | Satuan Baku | Keterangan Granularitas |
|---|---|---|---|---|
| 1 | `kejadian` | 2010–2025 | kejadian | Total kejadian dan rincian per jenis bencana |
| 2 | `rumah_rusak` | 2010–2025 | unit | Rincian: total, rusak berat (RB), sedang (RS), ringan (RR) |
| 3 | `rumah_terendam` | 2021–2022 | unit | Seri temporal pendek |
| 4 | `fasyankes_rusak` | 2010–2025 | unit | Fasilitas pelayanan kesehatan rusak |
| 5 | `satuan_pendidikan_rusak` | 2021–2025 | unit | Gedung sekolah / institusi pendidikan rusak |
| 6 | `jembatan_rusak` | 2010–2025 | unit | Infrastruktur jembatan |
| 7 | `kantor_rusak` | 2010–2025 | unit | Gedung kantor pemerintahan/layanan |
| 8 | `rumah_ibadat_rusak` | 2010–2025 | unit | Fasilitas peribadatan |
| 9 | `kios_toko_rusak` | 2010–2024 | unit | Fasilitas perdagangan kecil/menengah |
| 10 | `pabrik_rusak` | 2024 | unit | Seri 1 tahun |
| 11 | `luas_sawah_rusak` | 2010–2024 | hektar | Lahan pertanian pangan |
| 12 | `luas_lahan_kebun_hutan_rusak` | 2010–2024 | hektar | Perkebunan dan kehutanan |
| 13 | `nilai_kerugian` | 2015–2024 | rupiah | Kerugian ekonomi arus barang/jasa |
| 14 | `nilai_kerusakan` | 2015–2024 | rupiah | Kerusakan aset fisik modal tetap |

*Catatan:* Sesuai arahan panduan Bagian 6, **nilai kerugian** dan **nilai kerusakan** adalah dua konsep ekonomi yang berbeda dan **tidak boleh dijumlahkan** menjadi satu angka tunggal tanpa justifikasi metodologis.

---

## 4. Struktur Kolom Panel Gold (`panel_provinsi_bencana.parquet`)

### 4.1 Identitas Wilayah & Waktu
| Nama Kolom | Tipe Data | Keterangan |
|---|---|---|
| `wilayah_kode` | `int64` | Kode standar BPS $\times 100$ (1100 s.d. 9700) |
| `nama_wilayah` | `string` | Nama provinsi kanonik (huruf kapital) |
| `tahun` | `int64` | Tahun observasi (2010–2025) |

### 4.2 Kejadian Bencana (Frekuensi Kejadian)
| Nama Kolom | Tipe Data | Keterangan |
|---|---|---|
| `kejadian_total` | `float64` / `int64` | Total seluruh kejadian bencana |
| `kejadian_banjir` | `float64` / `int64` | Kejadian banjir |
| `kejadian_cuaca_ekstrem` | `float64` / `int64` | Puting beliung / badai / cuaca ekstrem |
| `kejadian_erupsi` | `float64` / `int64` | Letusan gunung api |
| `kejadian_gelombang_abrasi` | `float64` / `int64` | Gelombang pasang dan abrasi pantai |
| `kejadian_gempa_bumi` | `float64` / `int64` | Aktivitas tektonik gempa bumi |
| `kejadian_karhutla` | `float64` / `int64` | Kebakaran hutan dan lahan |
| `kejadian_kekeringan` | `float64` / `int64` | Musim kemarau panjang / kekeringan hidrologis |
| `kejadian_tanah_longsor` | `float64` / `int64` | Longsor perbukitan/lereng |
| `kejadian_tsunami` | `float64` / `int64` | Gelombang tsunami |

### 4.3 Kerusakan Sektor Permukiman & Infrastruktur Sosial
| Nama Kolom | Tipe Data | Keterangan |
|---|---|---|
| `rumah_rusak_total` | `float64` | Total unit rumah rusak |
| `rumah_rusak_berat` | `float64` | Rusak Berat (RB) |
| `rumah_rusak_sedang` | `float64` | Rusak Sedang (RS) |
| `rumah_rusak_ringan` | `float64` | Rusak Ringan (RR) |
| `rumah_terendam` | `float64` | Rumah tergenang banjir (tersedia 2021–2022) |
| `fasyankes_rusak` | `float64` | Rumah sakit, puskesmas, klinik rusak |
| `satuan_pendidikan_rusak` | `float64` | Sekolah, madrasah, kampus rusak (2021–2025) |
| `rumah_ibadat_rusak` | `float64` | Masjid, gereja, pura, vihara rusak |

### 4.4 Kerusakan Sektor Ekonomi & Produktif
| Nama Kolom | Tipe Data | Keterangan |
|---|---|---|
| `jembatan_rusak` | `float64` | Jembatan rusak |
| `kantor_rusak` | `float64` | Gedung kantor pemerintah/swasta rusak |
| `kios_toko_rusak` | `float64` | Pasar, toko, kios rusak (2010–2024) |
| `pabrik_rusak` | `float64` | Pabrik / industri manufaktur rusak (2024) |
| `luas_sawah_rusak_ha` | `float64` | Luas sawah rusak (hektar) |
| `luas_kebun_hutan_rusak_ha` | `float64` | Luas perkebunan & hutan rusak (hektar) |

### 4.5 Dampak Finansial & Transformasi Skala
| Nama Kolom | Tipe Data | Keterangan |
|---|---|---|
| `nilai_kerugian` | `float64` | Nilai kerugian nominal dalam rupiah; tidak disesuaikan dengan inflasi |
| `nilai_kerusakan` | `float64` | Nilai kerusakan aset nominal dalam rupiah; tidak disesuaikan dengan inflasi |
| `log_nilai_kerugian` | `float64` | $\log(1 + \text{nilai\_kerugian})$ atas nilai nominal rupiah |
| `log_nilai_kerusakan` | `float64` | $\log(1 + \text{nilai\_kerusakan})$ atas nilai nominal rupiah |

Nilai kerusakan adalah kerusakan aset fisik; nilai kerugian adalah dampak ekonomi.
Keduanya disimpan sebagai indikator terpisah dan tidak dijumlahkan. Transformasi `log1p`
hanya menambah fitur berskala log untuk analisis; nilai rupiah asli tetap ada.
Tidak ada deflasi karena indeks harga dan tahun dasar yang sesuai belum ditetapkan.

---

## 5. Prinsip Transformasi dan Kebijakan Missing Value (Tahap 4)
1. **Grid Lengkap vs Missing Jujur:**
   - Panel dibentuk dengan melakukan *left join* antara grid master $38 \times 16$ dengan tabel observasi Silver.
   - Observasi tahun di mana suatu seri belum dikumpulkan oleh BNPB dibiarkan bernilai `NaN` (bukan diimputasi $0$), agar kelengkapan panel per seri dapat dihitung dan dilaporkan secara jujur.
   - Kejadian bencana yang tervalidasi nihil dicatat sebagai $0$.
2. **Pemekaran Provinsi (Aturan Baku 5.1 & Log K-001):**
   - Provinsi induk dibiarkan apa adanya sesuai catatan sumber data.
   - Provinsi baru (Kalimantan Utara sejak 2012; Papua Barat Daya, Papua Selatan, Papua Tengah, Papua Pegunungan sejak 2022) hanya memiliki data sejak resmi berdiri.
   - Tidak dilakukan penggabungan paksa berbasis bobot penduduk agar tidak mengubah keaslian data mentah.
3. **Pemisahan Jalur Nasional:**
   - Baris dengan `wilayah_kode = 9999` (Indonesia) dialokasikan ke `gold_nasional.parquet` dan digunakan pada Tahap 6 untuk rekonsiliasi agregat provinsi vs angka nasional.

## 6. Aturan Seleksi Observasi Gold

Fungsi `pilih_observasi_gold` di `src/gold/aturan.py` dipanggil saat `python pipeline.py`
membangun Gold. Kunci Gold adalah provinsi × tahun × indikator; tabel nasional memakai
wilayah × periode asli × indikator. Aturan dan hitungan baris Silver yang tidak terpilih
ditulis/diperbarui pada `log-keputusan.csv` (K-101–K-105). Dampak nol berarti aturan
tersebut tidak mengecualikan baris Silver. Hitungan yang sama dikembalikan oleh
`bentuk_panel_gold` dan tersedia di hasil `gold.jalankan(silver)` sebagai
`gold_selection_counts`; `pipeline.py` mencetaknya setelah tahap Gold selesai.

1. **Snapshot dan revisi:** untuk indikator, wilayah, periode, dan rincian yang sama,
   snapshot dengan tanggal pada jalur sumber terbaru dipilih. Jika tanggal sama, kompilasi
   BNPB terbaru diprioritaskan; `_berkas_raw` leksikografis menjadi pemutus seri deterministik.
   Nilai yang tidak dipilih tidak dijumlahkan. Baris terpilih tetap membawa `_berkas_raw`
   dan `_sha256_raw`; baris Silver sumber tidak dihapus.
2. **Rincian:** panel provinsi menggunakan rincian `total` sumber bila tersedia. Jika sumber
   hanya memiliki `jenis_bencana=...`, nilai kategori dijumlahkan satu kali untuk total seri;
   rincian jenis bencana tetap berada di Silver. Untuk `rumah_rusak`, `berat`, `sedang`, dan
   `ringan` menjadi indikator terpisah saat tersedia. Total rumah rusak berasal dari total
   sumber, atau dijumlahkan dari rincian jenis bencana, atau diturunkan dari tiga tingkat
   kerusakan hanya bila ketiganya tersedia. Total tidak dijumlahkan lagi dengan rinciannya.
   Ketersediaan tingkat kerusakan tidak diisi dengan nol. Nilai kerusakan dan kerugian tidak
   saling ditambahkan.
3. **Frekuensi:** panel provinsi tahap ini hanya memuat periode tahunan 2010–2025.
   Periode semester/bulan tidak dijumlahkan atau disebarkan menjadi data tahunan; observasinya
   tetap di Silver sampai aturan agregasi dan kelengkapan periode dapat dibuktikan. Tabel
   nasional mempertahankan label periode sumber.
4. **Tanda Sprint 1:** tanda outlier dan patahan dari `reports/klasifikasi-anomali.csv` dan
   `reports/uji-patahan-seri.csv` diteruskan ke kolom flag per indikator; observasi dan nilainya
   tidak dihapus atau diubah karena tanda tersebut.
