# Tahap 2 — Profil deskriptif dan calon anomali

Analisis menggunakan data mentah yang tersedia pada snapshot repo; belum menjalankan
pembersihan atau mengubah nilai. Hanya observasi berlabel provinsi yang dianalisis.
Data level Indonesia dan kabupaten/kota dikecualikan agar tidak tercampur dengan
observasi provinsi. Beberapa indikator hanya tersedia untuk sejumlah tahun pada sumber
yang ada; statistik bukan klaim bahwa rentang tahun tersebut lengkap.

Jalankan ulang dari akar repo dengan `python -m src.analisis_tahap2`.

## Metode

- Statistik mencakup n, provinsi/periode teramati, mean, median, simpangan baku, kuartil,
  minimum, dan maksimum. Pengamatan dengan beberapa baris jenis bencana/proposal
  dijumlahkan pada tingkat provinsi-periode untuk membentuk satu observasi.
- Calon anomali ditandai menggunakan pagar IQR per seri pada gabungan observasi
  provinsi-periode: di bawah Q1 − 1,5×IQR atau di atas Q3 + 1,5×IQR. Ini hanya
  penanda eksploratif; nilai tidak dihapus atau dianggap salah.
- Nilai kerugian/kerusakan diagregasi per provinsi dan tahun kejadian yang tercatat.
  Baris dengan rentang tahun kejadian, bukan satu tahun, tidak dialokasikan agar tidak
  membuat pembagian nilai yang tidak didukung sumber. Dataset berasal dari proposal
  RRRP, bukan pencatatan menyeluruh seluruh dampak ekonomi aktual.
  Sebanyak 41 baris dengan periode tidak tunggal/tidak terbaca dan 0 baris dengan tahun di luar 2015–2024 tidak dimasukkan.
- Seri luas sawah dan luas lahan/kebun/hutan hanya tersedia sebagai agregat nasional
  menurut jenis bencana pada snapshot ini, sehingga tidak dibuat statistik provinsi.
  Grafiknya tetap disimpan dan menandai keterbatasan tersebut.

## Ringkasan per seri

| Seri | n | Provinsi | Periode | Mean | Median | Min | Maks | Calon anomali | Grafik |
|---|---:|---:|---|---:|---:|---:|---:|---:|---|
| `kejadian` | 608 | 38 | 2010–2025 | 82.7 | 33 | 0 | 1.36e+03 | 68 | [Boxplot & deret waktu](gambar/kejadian.png) |
| `rumah_rusak` | 142 | 38 | 2021–2025 | 4.33e+03 | 562 | 0 | 1.98e+05 | 20 | [Boxplot & deret waktu](gambar/rumah_rusak.png) |
| `rumah_terendam` | 66 | 33 | 2021–2022 | 3.96e+04 | 8.47e+03 | 36 | 3.22e+05 | 7 | [Boxplot & deret waktu](gambar/rumah_terendam.png) |
| `fasyankes_rusak` | 104 | 38 | 2021–2024 | 6.11 | 0 | 0 | 177 | 15 | [Boxplot & deret waktu](gambar/fasyankes_rusak.png) |
| `satuan_pendidikan_rusak` | 104 | 38 | 2021–2024 | 34.6 | 2 | 0 | 741 | 13 | [Boxplot & deret waktu](gambar/satuan_pendidikan_rusak.png) |
| `jembatan_rusak` | 104 | 38 | 2021–2024 | 12.3 | 5 | 0 | 159 | 9 | [Boxplot & deret waktu](gambar/jembatan_rusak.png) |
| `kantor_rusak` | 104 | 38 | 2021–2024 | 8.8 | 0 | 0 | 219 | 16 | [Boxplot & deret waktu](gambar/kantor_rusak.png) |
| `rumah_ibadat_rusak` | 104 | 38 | 2021–2024 | 31.6 | 2 | 0 | 555 | 13 | [Boxplot & deret waktu](gambar/rumah_ibadat_rusak.png) |
| `kios_toko_rusak` | 38 | 38 | 2024–2024 | 5.92 | 0 | 0 | 87 | 7 | [Boxplot & deret waktu](gambar/kios_toko_rusak.png) |
| `pabrik_rusak` | 38 | 38 | 2024–2024 | 2.53 | 0 | 0 | 90 | 3 | [Boxplot & deret waktu](gambar/pabrik_rusak.png) |
| `luas_sawah_rusak` | 0 | 0 | — | — | — | — | — | 0 | [Boxplot & deret waktu](gambar/luas_sawah_rusak.png) |
| `luas_lahan_kebun_hutan_rusak` | 0 | 0 | — | — | — | — | — | 0 | [Boxplot & deret waktu](gambar/luas_lahan_kebun_hutan_rusak.png) |
| `nilai_kerugian` | 131 | 34 | 2015–2024 | 2.42e+11 | 2.18e+10 | 0 | 1.51e+13 | 16 | [Boxplot & deret waktu](gambar/nilai_kerugian.png) |
| `nilai_kerusakan` | 131 | 34 | 2015–2024 | 4.96e+11 | 9.93e+10 | 0 | 2.87e+13 | 14 | [Boxplot & deret waktu](gambar/nilai_kerusakan.png) |

Rincian statistik per seri tersimpan di [`profil-per-seri.csv`](profil-per-seri.csv),
dan statistik per seri-provinsi di [`profil-per-provinsi.csv`](profil-per-provinsi.csv).
Seluruh calon anomali tersedia di [`calon-anomali.csv`](calon-anomali.csv).

## Calon anomali

Daftar berikut menampilkan sampai lima observasi dengan nilai tertinggi per seri;
CSV memuat seluruh observasi yang melampaui pagar IQR.

### `kejadian`

| Provinsi | Periode | Nilai | Alasan |
|---|---:|---:|---|
| JAWA BARAT | 2021 | 1,358 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| JAWA TENGAH | 2017 | 1,071 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| JAWA TENGAH | 2020 | 1,021 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| JAWA BARAT | 2020 | 942 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| JAWA TENGAH | 2019 | 926 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |

### `rumah_rusak`

| Provinsi | Periode | Nilai | Alasan |
|---|---:|---:|---|
| ACEH | 2025 | 198,082 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| JAWA BARAT | 2022 | 64,978 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| NUSA TENGGARA TIMUR | 2021 | 57,008 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| JAWA BARAT | 2024 | 30,228 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| JAWA TIMUR | 2021 | 22,043 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |

### `rumah_terendam`

| Provinsi | Periode | Nilai | Alasan |
|---|---:|---:|---|
| JAWA BARAT | 2021 | 321,650 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| KALIMANTAN SELATAN | 2021 | 253,000 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| JAWA TENGAH | 2022 | 222,949 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| KALIMANTAN BARAT | 2021 | 157,881 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| SUMATERA UTARA | 2021 | 146,731 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |

### `fasyankes_rusak`

| Provinsi | Periode | Nilai | Alasan |
|---|---:|---:|---|
| NUSA TENGGARA TIMUR | 2021 | 177 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| KALIMANTAN SELATAN | 2021 | 127 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| SULAWESI BARAT | 2021 | 48 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| JAWA TIMUR | 2021 | 32 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| BANTEN | 2022 | 31 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |

### `satuan_pendidikan_rusak`

| Provinsi | Periode | Nilai | Alasan |
|---|---:|---:|---|
| JAWA BARAT | 2022 | 741 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| KALIMANTAN SELATAN | 2021 | 564 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| NUSA TENGGARA TIMUR | 2021 | 317 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| SUMATERA BARAT | 2022 | 248 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| SULAWESI BARAT | 2021 | 231 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |

### `jembatan_rusak`

| Provinsi | Periode | Nilai | Alasan |
|---|---:|---:|---|
| SUMATERA BARAT | 2024 | 159 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| NUSA TENGGARA TIMUR | 2021 | 106 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| KALIMANTAN BARAT | 2022 | 102 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| KALIMANTAN SELATAN | 2021 | 53 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| NUSA TENGGARA BARAT | 2021 | 40 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |

### `kantor_rusak`

| Provinsi | Periode | Nilai | Alasan |
|---|---:|---:|---|
| NUSA TENGGARA TIMUR | 2021 | 219 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| KALIMANTAN SELATAN | 2021 | 197 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| SULAWESI BARAT | 2021 | 81 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| JAWA TIMUR | 2021 | 69 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| JAWA TIMUR | 2024 | 46 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |

### `rumah_ibadat_rusak`

| Provinsi | Periode | Nilai | Alasan |
|---|---:|---:|---|
| BALI | 2021 | 555 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| KALIMANTAN SELATAN | 2021 | 531 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| NUSA TENGGARA TIMUR | 2021 | 429 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| JAWA BARAT | 2022 | 339 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| JAWA TIMUR | 2021 | 277 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |

### `kios_toko_rusak`

| Provinsi | Periode | Nilai | Alasan |
|---|---:|---:|---|
| JAWA TIMUR | 2024 | 87 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| SUMATERA BARAT | 2024 | 50 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| DAERAH ISTIMEWA YOGYAKARTA | 2024 | 40 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| JAWA TENGAH | 2024 | 14 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| NUSA TENGGARA BARAT | 2024 | 10 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |

### `pabrik_rusak`

| Provinsi | Periode | Nilai | Alasan |
|---|---:|---:|---|
| NUSA TENGGARA BARAT | 2024 | 90 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| KALIMANTAN TIMUR | 2024 | 4 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| JAWA TIMUR | 2024 | 2 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |

### `luas_sawah_rusak`
Tidak ada observasi tingkat provinsi; calon anomali tidak dapat dinilai dari sumber yang tersedia.

### `luas_lahan_kebun_hutan_rusak`
Tidak ada observasi tingkat provinsi; calon anomali tidak dapat dinilai dari sumber yang tersedia.

### `nilai_kerugian`

| Provinsi | Periode | Nilai | Alasan |
|---|---:|---:|---|
| SULAWESI TENGAH | 2018 | 1.51477e+13 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| JAWA TENGAH | 2018 | 3.96466e+12 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| SULAWESI SELATAN | 2021 | 1.22239e+12 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| SULAWESI SELATAN | 2022 | 1.10962e+12 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| JAWA BARAT | 2023 | 8.74009e+11 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |

### `nilai_kerusakan`

| Provinsi | Periode | Nilai | Alasan |
|---|---:|---:|---|
| SULAWESI TENGAH | 2018 | 2.87265e+13 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| JAWA TENGAH | 2018 | 7.14425e+12 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| ACEH | 2016 | 2.42562e+12 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| JAWA BARAT | 2020 | 1.70996e+12 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
| PAPUA | 2019 | 1.38144e+12 | nilai di atas pagar atas IQR (Q3 + 1,5 x IQR) |
