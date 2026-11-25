# Kategori anomali dan duplikat

Dihasilkan `python pipeline.py` (`src/silver/anomali.py`). Nilai di Silver tidak diubah kecuali galat input yang koreksinya jelas.

## Galat input (semua baris Silver diperiksa terhadap rentang satuan): 0

Tidak ada nilai di luar rentang satuannya.

### Galat input yang diputuskan sebelum Silver (`GALAT_INPUT` di `src/konfigurasi.py`)

| seri_kode | wilayah_kode | periode | rincian | nilai_asli | tindakan | bukti |
|---|---|---|---|---|---|---|
| luas_lahan_kebun_hutan_rusak | 9999 | 2012 | jenis_bencana=kebakaran_hutan_dan_lahan | 44,041,216.50 | buang | 44.041.216,5 ha = lebih dari seperlima luas daratan Indonesia; tahun lain kebakaran 6–119.698 ha; tidak ada berkas lain untuk sel ini, jadi angka yang benar tidak bisa dipastikan |

Berkas sumber dan buktinya: `reports/galat-input.csv`.

## Uji patahan seri

| seri_kode | pergantian | provinsi | porsi_naik | porsi_turun | patahan | keterangan |
|---|---|---|---|---|---|---|
| kejadian [jumlah] | 2010→2011 | 36 | 0.31 | 0.33 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| kejadian [jumlah] | 2011→2012 | 36 | 0.44 | 0.28 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| kejadian [jumlah] | 2012→2013 | 38 | 0.42 | 0.26 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| kejadian [jumlah] | 2013→2014 | 37 | 0.22 | 0.46 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| kejadian [jumlah] | 2014→2015 | 37 | 0.38 | 0.38 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| kejadian [jumlah] | 2015→2016 | 38 | 0.58 | 0.21 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| kejadian [jumlah] | 2016→2017 | 37 | 0.57 | 0.27 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| kejadian [jumlah] | 2017→2018 | 38 | 0.45 | 0.26 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| kejadian [jumlah] | 2018→2019 | 38 | 0.42 | 0.32 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| kejadian [jumlah] | 2019→2020 | 38 | 0.55 | 0.16 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| kejadian [jumlah] | 2020→2021 | 38 | 0.55 | 0.16 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| kejadian [jumlah] | 2021→2022 | 37 | 0.08 | 0.68 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| kejadian [jumlah] | 2022→2023 | 38 | 0.63 | 0.13 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| kejadian [jumlah] | 2023→2024 | 38 | 0.34 | 0.58 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| kejadian [jumlah] | 2024→2025 | 38 | 0.63 | 0.16 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| rumah_rusak [jumlah] | 2021→2022 | 34 | 0.24 | 0.68 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| rumah_rusak [jumlah] | 2022→2024 | 34 | 0.50 | 0.38 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| rumah_rusak [jumlah] | 2024→2025 | 38 | 0.45 | 0.45 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| rumah_terendam [jumlah] | — | 0 |  |  | tidak dapat diuji | hanya 2 periode; pola serentak dari dua titik tidak bisa dibedakan dari perubahan sungguhan |
| fasyankes_rusak [jumlah] | 2021→2022 | 20 | 0.20 | 0.75 | ya | ambang lompat 20%, porsi serentak ≥ 70% |
| fasyankes_rusak [jumlah] | 2022→2024 | 14 | 0.57 | 0.43 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| satuan_pendidikan_rusak [jumlah] | 2021→2022 | 32 | 0.31 | 0.59 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| satuan_pendidikan_rusak [jumlah] | 2022→2024 | 29 | 0.45 | 0.48 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| jembatan_rusak [jumlah] | 2021→2022 | 31 | 0.32 | 0.58 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| jembatan_rusak [jumlah] | 2022→2024 | 30 | 0.40 | 0.47 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| kantor_rusak [jumlah] | 2021→2022 | 28 | 0.32 | 0.64 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| kantor_rusak [jumlah] | 2022→2024 | 19 | 0.32 | 0.68 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| rumah_ibadat_rusak [jumlah] | 2021→2022 | 31 | 0.26 | 0.71 | ya | ambang lompat 20%, porsi serentak ≥ 70% |
| rumah_ibadat_rusak [jumlah] | 2022→2024 | 29 | 0.48 | 0.48 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| kios_toko_rusak [jumlah] | — | 0 |  |  | tidak dapat diuji | hanya 1 periode; pola serentak dari dua titik tidak bisa dibedakan dari perubahan sungguhan |
| pabrik_rusak [jumlah] | — | 0 |  |  | tidak dapat diuji | hanya 1 periode; pola serentak dari dua titik tidak bisa dibedakan dari perubahan sungguhan |
| nilai_kerusakan [jumlah] | 2015→2016 | 0 |  |  | tidak dapat diuji | hanya 0 provinsi punya angka di kedua periode (minimal 10) |
| nilai_kerusakan [jumlah] | 2016→2017 | 6 |  |  | tidak dapat diuji | hanya 6 provinsi punya angka di kedua periode (minimal 10) |
| nilai_kerusakan [jumlah] | 2017→2018 | 15 | 0.60 | 0.40 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| nilai_kerusakan [jumlah] | 2018→2019 | 9 |  |  | tidak dapat diuji | hanya 9 provinsi punya angka di kedua periode (minimal 10) |
| nilai_kerusakan [jumlah] | 2019→2020 | 6 |  |  | tidak dapat diuji | hanya 6 provinsi punya angka di kedua periode (minimal 10) |
| nilai_kerusakan [jumlah] | 2020→2021 | 11 | 0.45 | 0.18 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| nilai_kerusakan [jumlah] | 2021→2022 | 13 | 0.31 | 0.69 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| nilai_kerusakan [jumlah] | 2022→2023 | 7 |  |  | tidak dapat diuji | hanya 7 provinsi punya angka di kedua periode (minimal 10) |
| nilai_kerusakan [jumlah] | 2023→2024 | 2 |  |  | tidak dapat diuji | hanya 2 provinsi punya angka di kedua periode (minimal 10) |
| nilai_kerugian [jumlah] | 2015→2016 | 0 |  |  | tidak dapat diuji | hanya 0 provinsi punya angka di kedua periode (minimal 10) |
| nilai_kerugian [jumlah] | 2016→2017 | 6 |  |  | tidak dapat diuji | hanya 6 provinsi punya angka di kedua periode (minimal 10) |
| nilai_kerugian [jumlah] | 2017→2018 | 15 | 0.67 | 0.27 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| nilai_kerugian [jumlah] | 2018→2019 | 9 |  |  | tidak dapat diuji | hanya 9 provinsi punya angka di kedua periode (minimal 10) |
| nilai_kerugian [jumlah] | 2019→2020 | 6 |  |  | tidak dapat diuji | hanya 6 provinsi punya angka di kedua periode (minimal 10) |
| nilai_kerugian [jumlah] | 2020→2021 | 11 | 0.45 | 0.45 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| nilai_kerugian [jumlah] | 2021→2022 | 13 | 0.38 | 0.46 | tidak | ambang lompat 20%, porsi serentak ≥ 70% |
| nilai_kerugian [jumlah] | 2022→2023 | 7 |  |  | tidak dapat diuji | hanya 7 provinsi punya angka di kedua periode (minimal 10) |
| nilai_kerugian [jumlah] | 2023→2024 | 2 |  |  | tidak dapat diuji | hanya 2 provinsi punya angka di kedua periode (minimal 10) |

## Pergantian definisi yang dinyatakan penerbit

Tidak ada.

## Cakupan parsial yang dinyatakan penerbit

Tidak ada.

## Perubahan batas wilayah di tengah panel: 16

| seri_kode | induk | wilayah_kode | periode | anak | nilai_sebelum | nilai_sesudah |
|---|---|---|---|---|---|---|
| rumah_rusak [jumlah] | Papua Barat | 9100 | 2024 | Papua Barat Daya | 259.00 | 67.00 |
| rumah_rusak [jumlah] | Papua | 9400 | 2024 | Papua Selatan, Papua Tengah, Papua Pegunungan | 1,824.00 | 317.00 |
| fasyankes_rusak [jumlah] | Papua Barat | 9100 | 2024 | Papua Barat Daya | 0.00 | 0.00 |
| fasyankes_rusak [jumlah] | Papua | 9400 | 2024 | Papua Selatan, Papua Tengah, Papua Pegunungan | 0.00 | 0.00 |
| satuan_pendidikan_rusak [jumlah] | Papua Barat | 9100 | 2024 | Papua Barat Daya | 0.00 | 0.00 |
| satuan_pendidikan_rusak [jumlah] | Papua | 9400 | 2024 | Papua Selatan, Papua Tengah, Papua Pegunungan | 0.00 | 4.00 |
| jembatan_rusak [jumlah] | Papua Barat | 9100 | 2024 | Papua Barat Daya | 0.00 | 4.00 |
| jembatan_rusak [jumlah] | Papua | 9400 | 2024 | Papua Selatan, Papua Tengah, Papua Pegunungan | 0.00 | 0.00 |
| kantor_rusak [jumlah] | Papua Barat | 9100 | 2024 | Papua Barat Daya | 0.00 | 0.00 |
| kantor_rusak [jumlah] | Papua | 9400 | 2024 | Papua Selatan, Papua Tengah, Papua Pegunungan | 0.00 | 0.00 |
| rumah_ibadat_rusak [jumlah] | Papua Barat | 9100 | 2024 | Papua Barat Daya | 0.00 | 3.00 |
| rumah_ibadat_rusak [jumlah] | Papua | 9400 | 2024 | Papua Selatan, Papua Tengah, Papua Pegunungan | 1.00 | 7.00 |
| nilai_kerusakan [jumlah] | Sulawesi Selatan | 7300 | 2017 | Sulawesi Barat | 58,309,330,000.00 | 112,140,883,625.00 |
| nilai_kerusakan [jumlah] | Papua | 9400 | 2017 | Papua Barat | 65,532,582,620.00 | 32,666,430,000.00 |
| nilai_kerugian [jumlah] | Sulawesi Selatan | 7300 | 2017 | Sulawesi Barat | 8,612,000,000.00 | 32,445,613,900.00 |
| nilai_kerugian [jumlah] | Papua | 9400 | 2017 | Papua Barat | 812,850,000.00 | 76,000,000.00 |

Nilai induk sebelum periode ini mencakup wilayah provinsi pemekaran; sesudahnya tidak. Perubahannya bukan tren dan tidak diratakan.

## Calon anomali dan kategorinya (158)

| seri_kode | nama_wilayah | periode | nilai | arah | kategori | tindakan |
|---|---|---|---|---|---|---|
| fasyankes_rusak [jumlah] | Nusa Tenggara Timur | 2021 | 177.00 | ke bawah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun |
| fasyankes_rusak [jumlah] | Kalimantan Selatan | 2021 | 127.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| fasyankes_rusak [jumlah] | Aceh | 2022 | 3.00 | ke bawah | patahan_seri | tandai; cari catatan metode |
| fasyankes_rusak [jumlah] | Sumatera Barat | 2022 | 30.00 | ke bawah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun |
| fasyankes_rusak [jumlah] | Jawa Barat | 2022 | 25.00 | ke bawah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun |
| fasyankes_rusak [jumlah] | Banten | 2022 | 31.00 | ke bawah + perubahan | patahan_seri | tandai; cari catatan metode |
| fasyankes_rusak [jumlah] | Nusa Tenggara Timur | 2022 | 3.00 | ke bawah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun |
| fasyankes_rusak [jumlah] | Kalimantan Selatan | 2022 | 0.00 | perubahan | patahan_seri | tandai; cari catatan metode |
| fasyankes_rusak [jumlah] | Sulawesi Selatan | 2022 | 1.00 | ke bawah | patahan_seri | tandai; cari catatan metode |
| fasyankes_rusak [jumlah] | Sulawesi Barat | 2022 | 0.00 | perubahan | patahan_seri | tandai; cari catatan metode |
| fasyankes_rusak [jumlah] | Maluku Utara | 2022 | 2.00 | ke bawah | patahan_seri | tandai; cari catatan metode |
| fasyankes_rusak [jumlah] | Aceh | 2024 | 0.00 | perubahan | outlier | tandai, nilai tidak diubah |
| fasyankes_rusak [jumlah] | Sumatera Barat | 2024 | 5.00 | ke bawah + perubahan | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun |
| fasyankes_rusak [jumlah] | Riau | 2024 | 16.00 | ke bawah + perubahan | outlier | tandai, nilai tidak diubah |
| fasyankes_rusak [jumlah] | Lampung | 2024 | 1.00 | perubahan | outlier | tandai, nilai tidak diubah |
| fasyankes_rusak [jumlah] | Jawa Barat | 2024 | 10.00 | ke bawah + perubahan | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun |
| fasyankes_rusak [jumlah] | Jawa Tengah | 2024 | 2.00 | perubahan | outlier | tandai, nilai tidak diubah |
| fasyankes_rusak [jumlah] | DI Yogyakarta | 2024 | 2.00 | perubahan | outlier | tandai, nilai tidak diubah |
| fasyankes_rusak [jumlah] | Jawa Timur | 2024 | 8.00 | ke bawah + perubahan | outlier | tandai, nilai tidak diubah |
| fasyankes_rusak [jumlah] | Banten | 2024 | 0.00 | perubahan | outlier | tandai, nilai tidak diubah |
| fasyankes_rusak [jumlah] | Nusa Tenggara Barat | 2024 | 1.00 | perubahan | outlier | tandai, nilai tidak diubah |
| fasyankes_rusak [jumlah] | Nusa Tenggara Timur | 2024 | 29.00 | ke bawah + perubahan | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun |
| fasyankes_rusak [jumlah] | Sulawesi Tengah | 2024 | 3.00 | perubahan | outlier | tandai, nilai tidak diubah |
| fasyankes_rusak [jumlah] | Sulawesi Selatan | 2024 | 0.00 | perubahan | outlier | tandai, nilai tidak diubah |
| fasyankes_rusak [jumlah] | Maluku Utara | 2024 | 0.00 | perubahan | outlier | tandai, nilai tidak diubah |
| fasyankes_rusak [jumlah] | Papua Pegunungan | 2024 | 5.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| jembatan_rusak [jumlah] | Sumatera Barat | 2024 | 159.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kantor_rusak [jumlah] | Nusa Tenggara Timur | 2021 | 219.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kantor_rusak [jumlah] | Kalimantan Selatan | 2021 | 197.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kantor_rusak [jumlah] | Sumatera Barat | 2022 | 46.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kantor_rusak [jumlah] | Jawa Barat | 2022 | 44.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kantor_rusak [jumlah] | Nusa Tenggara Timur | 2022 | 0.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kantor_rusak [jumlah] | Jawa Timur | 2024 | 46.00 | ke bawah + perubahan | outlier | tandai, nilai tidak diubah |
| kantor_rusak [jumlah] | Banten | 2024 | 0.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kantor_rusak [jumlah] | Nusa Tenggara Timur | 2024 | 11.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kantor_rusak [jumlah] | Sulawesi Selatan | 2024 | 4.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Kepulauan Bangka Belitung | 2010 | 0.00 | ke samping | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Kepulauan Riau | 2011 | 4.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Jawa Tengah | 2011 | 467.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Jawa Timur | 2011 | 278.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Kalimantan Utara | 2011 | 0.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Sulawesi Tenggara | 2011 | 13.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Papua Selatan | 2011 | 0.00 | ke bawah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun |
| kejadian [jumlah] | Papua Pegunungan | 2011 | 0.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Kepulauan Bangka Belitung | 2012 | 0.00 | ke samping | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Sulawesi Tenggara | 2012 | 99.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Kepulauan Bangka Belitung | 2013 | 15.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Sulawesi Tenggara | 2013 | 29.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Papua Barat Daya | 2013 | 0.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Kalimantan Selatan | 2014 | 13.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Kepulauan Riau | 2015 | 5.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Bali | 2015 | 6.00 | ke samping | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | DKI Jakarta | 2016 | 43.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Jawa Barat | 2016 | 306.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Jawa Tengah | 2016 | 600.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Jawa Timur | 2016 | 406.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Maluku | 2016 | 5.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Papua | 2016 | 1.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Papua Selatan | 2016 | 0.00 | ke bawah + perubahan | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun |
| kejadian [jumlah] | Lampung | 2017 | 9.00 | ke samping | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Jawa Tengah | 2017 | 1,071.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Kalimantan Utara | 2017 | 2.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Papua Selatan | 2017 | 0.00 | ke bawah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun |
| kejadian [jumlah] | Kepulauan Bangka Belitung | 2018 | 117.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Nusa Tenggara Timur | 2018 | 185.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Papua Tengah | 2018 | 0.00 | ke samping | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Kepulauan Bangka Belitung | 2019 | 22.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | DKI Jakarta | 2019 | 6.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Jawa Barat | 2019 | 699.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Jawa Tengah | 2019 | 926.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Jawa Timur | 2019 | 622.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Nusa Tenggara Timur | 2019 | 38.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Kalimantan Utara | 2019 | 21.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Papua Barat Daya | 2019 | 1.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Papua Selatan | 2019 | 0.00 | ke bawah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun |
| kejadian [jumlah] | Papua Pegunungan | 2019 | 5.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Papua Pegunungan | 2020 | 0.00 | ke bawah + perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Jawa Barat | 2021 | 1,358.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Papua Barat Daya | 2021 | 0.00 | ke bawah + perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Papua Selatan | 2021 | 0.00 | ke bawah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun |
| kejadian [jumlah] | Papua Tengah | 2021 | 4.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Papua Pegunungan | 2021 | 3.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Jambi | 2022 | 9.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Kepulauan Riau | 2022 | 11.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Jawa Barat | 2022 | 825.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Papua Barat Daya | 2022 | 8.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Papua Selatan | 2022 | 0.00 | ke bawah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun |
| kejadian [jumlah] | Papua Tengah | 2022 | 0.00 | ke bawah + ke samping | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Papua Pegunungan | 2022 | 1.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Papua Selatan | 2023 | 2.00 | ke bawah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun |
| kejadian [jumlah] | Papua Tengah | 2023 | 1.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Papua Pegunungan | 2023 | 2.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Sumatera Selatan | 2024 | 271.00 | ke samping | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Kalimantan Selatan | 2024 | 26.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Riau | 2025 | 396.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Kalimantan Selatan | 2025 | 276.00 | perubahan | outlier | tandai, nilai tidak diubah |
| kejadian [jumlah] | Papua Selatan | 2025 | 1.00 | ke bawah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun |
| kejadian [jumlah] | Papua Tengah | 2025 | 4.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kios_toko_rusak [jumlah] | Sumatera Barat | 2024 | 50.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kios_toko_rusak [jumlah] | Jawa Tengah | 2024 | 14.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kios_toko_rusak [jumlah] | DI Yogyakarta | 2024 | 40.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| kios_toko_rusak [jumlah] | Jawa Timur | 2024 | 87.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| nilai_kerugian [jumlah] | Sulawesi Selatan | 2015 | 8,612,000,000.00 | ke samping | outlier | tandai, nilai tidak diubah |
| nilai_kerugian [jumlah] | Jawa Barat | 2017 | 0.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| nilai_kerugian [jumlah] | DI Yogyakarta | 2017 | 759,394,860,108.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| nilai_kerugian [jumlah] | Gorontalo | 2017 | 0.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| nilai_kerugian [jumlah] | Papua | 2017 | 76,000,000.00 | ke bawah | patahan_wilayah | tandai; jangan bandingkan induk sebelum dan sesudah pemekaran |
| nilai_kerugian [jumlah] | Sumatera Utara | 2018 | 172,500,000.00 | ke bawah + ke samping | outlier | tandai, nilai tidak diubah |
| nilai_kerugian [jumlah] | Sulawesi Tengah | 2018 | 15,147,663,526,706.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| nilai_kerugian [jumlah] | Gorontalo | 2018 | 4,454,625,000.00 | perubahan | outlier | tandai, nilai tidak diubah |
| nilai_kerugian [jumlah] | Sumatera Utara | 2019 | 52,130,593,545.00 | perubahan | outlier | tandai, nilai tidak diubah |
| nilai_kerugian [jumlah] | Sulawesi Tengah | 2019 | 17,236,296,000.00 | perubahan | outlier | tandai, nilai tidak diubah |
| nilai_kerugian [jumlah] | Maluku | 2019 | 382,844,000.00 | ke bawah + ke samping | outlier | tandai, nilai tidak diubah |
| nilai_kerugian [jumlah] | Maluku Utara | 2020 | 824,836,000.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| nilai_kerugian [jumlah] | Sumatera Utara | 2021 | 596,077,008,006.00 | perubahan + ke samping | outlier | tandai, nilai tidak diubah |
| nilai_kerugian [jumlah] | Jawa Barat | 2021 | 596,500,000.00 | perubahan | outlier | tandai, nilai tidak diubah |
| nilai_kerugian [jumlah] | Jawa Timur | 2021 | 1,678,500,000.00 | perubahan | outlier | tandai, nilai tidak diubah |
| nilai_kerugian [jumlah] | Nusa Tenggara Barat | 2022 | 6,895,375.00 | ke bawah + perubahan | outlier | tandai, nilai tidak diubah |
| nilai_kerugian [jumlah] | Sulawesi Selatan | 2022 | 1,109,622,134,176.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| nilai_kerugian [jumlah] | Nusa Tenggara Timur | 2023 | 0.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| nilai_kerusakan [jumlah] | Sumatera Barat | 2017 | 255,925,081,497.00 | ke samping | outlier | tandai, nilai tidak diubah |
| nilai_kerusakan [jumlah] | Jawa Barat | 2017 | 0.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| nilai_kerusakan [jumlah] | Sulawesi Tengah | 2018 | 28,726,512,029,305.00 | ke bawah + perubahan | outlier | tandai, nilai tidak diubah |
| nilai_kerusakan [jumlah] | Sulawesi Tengah | 2019 | 59,569,700,000.00 | perubahan | outlier | tandai, nilai tidak diubah |
| nilai_kerusakan [jumlah] | Papua Barat | 2019 | 77,441,750,000.00 | perubahan | outlier | tandai, nilai tidak diubah |
| nilai_kerusakan [jumlah] | Papua | 2019 | 1,381,438,807,300.00 | perubahan | outlier | tandai, nilai tidak diubah |
| nilai_kerusakan [jumlah] | Sulawesi Tenggara | 2020 | 21,957,420,800.00 | ke samping | outlier | tandai, nilai tidak diubah |
| nilai_kerusakan [jumlah] | Aceh | 2021 | 82,601,914,286.00 | perubahan | outlier | tandai, nilai tidak diubah |
| nilai_kerusakan [jumlah] | Jawa Barat | 2021 | 157,543,943.71 | ke bawah + perubahan | outlier | tandai, nilai tidak diubah |
| nilai_kerusakan [jumlah] | Sulawesi Tenggara | 2021 | 170,032,845,713.00 | perubahan | outlier | tandai, nilai tidak diubah |
| nilai_kerusakan [jumlah] | Papua Pegunungan | 2021 | 954,308,571.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| nilai_kerusakan [jumlah] | Jawa Barat | 2022 | 93,176,009,550.00 | perubahan | outlier | tandai, nilai tidak diubah |
| nilai_kerusakan [jumlah] | Nusa Tenggara Barat | 2022 | 27,272,900.00 | ke bawah + perubahan | outlier | tandai, nilai tidak diubah |
| nilai_kerusakan [jumlah] | Nusa Tenggara Timur | 2023 | 0.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| pabrik_rusak [jumlah] | Jawa Timur | 2024 | 2.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| pabrik_rusak [jumlah] | Nusa Tenggara Barat | 2024 | 90.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| pabrik_rusak [jumlah] | Kalimantan Timur | 2024 | 4.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| rumah_ibadat_rusak [jumlah] | Bali | 2021 | 555.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| rumah_ibadat_rusak [jumlah] | Jawa Barat | 2022 | 339.00 | ke bawah | patahan_seri | tandai; cari catatan metode |
| rumah_ibadat_rusak [jumlah] | Banten | 2022 | 55.00 | perubahan | patahan_seri | tandai; cari catatan metode |
| rumah_ibadat_rusak [jumlah] | Nusa Tenggara Timur | 2022 | 3.00 | perubahan | patahan_seri | tandai; cari catatan metode |
| rumah_ibadat_rusak [jumlah] | Kalimantan Selatan | 2022 | 0.00 | perubahan | patahan_seri | tandai; cari catatan metode |
| rumah_ibadat_rusak [jumlah] | Jawa Timur | 2024 | 220.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| rumah_rusak [jumlah] | Jambi | 2024 | 561.00 | perubahan | outlier | tandai, nilai tidak diubah |
| rumah_rusak [jumlah] | Jawa Barat | 2024 | 30,228.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| rumah_rusak [jumlah] | Kalimantan Tengah | 2024 | 0.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| rumah_rusak [jumlah] | Papua Tengah | 2024 | 0.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| rumah_rusak [jumlah] | Aceh | 2025 | 198,082.00 | ke bawah + perubahan | outlier | tandai, nilai tidak diubah |
| rumah_rusak [jumlah] | Papua Barat Daya | 2025 | 0.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| rumah_rusak [jumlah] | Papua Selatan | 2025 | 0.00 | ke bawah + perubahan | outlier | tandai, nilai tidak diubah |
| rumah_terendam [jumlah] | Kepulauan Bangka Belitung | 2022 | 111.00 | ke bawah + perubahan | outlier | tandai, nilai tidak diubah |
| rumah_terendam [jumlah] | Bali | 2022 | 4,192.00 | perubahan | outlier | tandai, nilai tidak diubah |
| satuan_pendidikan_rusak [jumlah] | Sumatera Barat | 2022 | 248.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| satuan_pendidikan_rusak [jumlah] | Jawa Barat | 2022 | 741.00 | ke bawah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun |
| satuan_pendidikan_rusak [jumlah] | Kalimantan Selatan | 2022 | 0.00 | perubahan | outlier | tandai, nilai tidak diubah |
| satuan_pendidikan_rusak [jumlah] | Jawa Barat | 2024 | 91.00 | ke bawah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun |
| satuan_pendidikan_rusak [jumlah] | Jawa Tengah | 2024 | 229.00 | ke bawah | outlier | tandai, nilai tidak diubah |
| satuan_pendidikan_rusak [jumlah] | Jawa Timur | 2024 | 134.00 | ke bawah | outlier | tandai, nilai tidak diubah |

Outlier di sini adalah outlier statistik. Menyebutnya *outlier asli* butuh penjelasan dunia nyata (kebijakan, bencana, cakupan survei); kolom itu diisi tim saat Sprint 2 bila buktinya ditemukan.

## Duplikat dua format BPS (CSV vs JSON)

Tidak ada seri BPS dua format.

## Kunci Silver kembar: 0
