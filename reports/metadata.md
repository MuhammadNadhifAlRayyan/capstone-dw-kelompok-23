# Metadata seri: nama, satuan, kode SDG

Dihasilkan `python pipeline.py` dari berkas mentah dan `src/konfigurasi.py`. Tabel lengkap ada di `docs/seri.csv`. Bila katalog dan berkas mentah berbeda, berkas mentah yang dipakai dan koreksinya dicatat di `log-keputusan.csv`.

## Nama di berkas mentah dan nama baku

| seri_kode | nama_di_berkas | nama_baku |
|---|---|---|
| kejadian | Jumlah Kejadian Bencana Menurut Kabupaten Tahun 2010-2024 | Jumlah kejadian bencana |
| rumah_rusak | Jumlah Rumah Rusak Akibat Bencana Tahun 2010-2024 | Jumlah rumah rusak akibat bencana |
| rumah_terendam | kolom 'Rumah Terendam' di Rekapitulasi Jumlah Kejadian, Korban dan Kerusakan Akibat Bencana Tahun 2021 per Provinsi | Jumlah rumah terendam |
| fasyankes_rusak | Jumlah Fasilitas Pelayanan Kesehatan yang Rusak Akibat Bencana Tahun 2010-2024 | Jumlah fasilitas pelayanan kesehatan rusak |
| satuan_pendidikan_rusak | Jumlah Satuan Pendidikan Rusak Akibat Bencana Menurut Provinsi 2024.xlsx | Jumlah satuan pendidikan rusak |
| jembatan_rusak | Jumlah Jembatan Rusak Akibat Bencana Menurut Provinsi, 2024 | Jumlah jembatan rusak |
| kantor_rusak | Jumlah Kantor yang Rusak Akibat Bencana Tahun 2010-2024 | Jumlah kantor rusak |
| rumah_ibadat_rusak | Jumlah Rumah Ibadat yang Rusak Akibat Bencana Tahun 2010-2024 | Jumlah rumah ibadat rusak |
| kios_toko_rusak | Jumlah Kios / Toko Rusak Akibat Bencana Tahun 2010-2024.xlsx | Jumlah kios/toko rusak |
| pabrik_rusak | Jumlah Pabrik Rusak Akibat Bencana Menurut Provinsi 2024.xlsx | Jumlah pabrik rusak |
| luas_sawah_rusak | Luas Sawah yang Rusak Akibat Bencana Tahun 2010-2024 | Luas sawah rusak akibat bencana |
| luas_lahan_kebun_hutan_rusak | Luas Lahan, Kebun, dan Hutan yang Rusak Akibat Bencana Tahun 2010-2024.xlsx | Luas lahan, kebun, dan hutan rusak akibat bencana |
| nilai_kerusakan |  | Nilai kerusakan akibat bencana (usulan rehabilitasi dan rekonstruksi) |
| nilai_kerugian |  | Nilai kerugian akibat bencana (usulan rehabilitasi dan rekonstruksi) |
| EN.CLC.MDAT.ZS | Droughts, floods, extreme temperatures (% of population, average 1990-2009) | Droughts, floods, extreme temperatures (% of population, average 1990-2009) |

## Satuan dan kode SDG

| seri_kode | katalog_satuan | satuan | bukti_satuan | katalog_sdg | sdg_kode |
|---|---|---|---|---|---|
| kejadian | kejadian | kejadian | Keterangan: 'Jumlah Kejadian: Jumlah Total Kejadian Bencana Menurut Klasifikasi Penyajian' | — | — |
| rumah_rusak | unit | unit | baris satuan '(unit)' di bawah kepala 'Kerusakan' pada rekap 2021/2022 (XLSX tangan) | 11.5.2\|1.5.2 | 11.5.2\|1.5.2 |
| rumah_terendam | unit | unit | baris satuan '(unit)' di bawah kepala 'Kerusakan' pada rekap 2021/2022 (XLSX tangan) | 11.5.2\|1.5.2 | 11.5.2\|1.5.2 |
| fasyankes_rusak | unit | unit | baris satuan '(unit)' di bawah kepala 'Kerusakan' pada rekap 2021/2022 (XLSX tangan) | 11.5.2 | 11.5.2 |
| satuan_pendidikan_rusak | unit | unit | baris satuan '(unit)' di bawah kepala 'Kerusakan' pada rekap 2021/2022 (XLSX tangan) | 11.5.2 | 11.5.2 |
| jembatan_rusak | unit | unit | baris satuan '(unit)' di bawah kepala 'Kerusakan' pada rekap 2021/2022 (XLSX tangan) | 11.5.2 | 11.5.2 |
| kantor_rusak | unit | unit | baris satuan '(unit)' di bawah kepala 'Kerusakan' pada rekap 2021/2022 (XLSX tangan) | — | — |
| rumah_ibadat_rusak | unit | unit | baris satuan '(unit)' di bawah kepala 'Kerusakan' pada rekap 2021/2022 (XLSX tangan) | — | — |
| kios_toko_rusak | unit | unit | baris satuan '(unit)' di bawah kepala 'Kerusakan' pada rekap 2021/2022 (XLSX tangan) | 11.5.2\|1.5.2 | 11.5.2\|1.5.2 |
| pabrik_rusak | unit | unit | baris satuan '(unit)' di bawah kepala 'Kerusakan' pada rekap 2021/2022 (XLSX tangan) | 11.5.2\|1.5.2 | 11.5.2\|1.5.2 |
| luas_sawah_rusak | tidak_ada | hektar | tabel tidak menyatakan satuan; Keterangan memakai hektar untuk ambang kejadian ('1 hektar lahan terdampak/rusak') dan angkanya berdesimal dua; dugaan, dipastikan dari Juklak Standar Data (katalog) di Sprint 2 | 11.5.2\|1.5.2 | 11.5.2\|1.5.2 |
| luas_lahan_kebun_hutan_rusak | tidak_ada | hektar | sama dengan luas_sawah_rusak | 11.5.2\|1.5.2 | 11.5.2\|1.5.2 |
| nilai_kerusakan | rupiah | rupiah | judul resource di ckan/package_search-pusdatinkom-01.json: 'Nilai Kerusakan dan Kerugian ...'; angka sampai satuan rupiah | 11.5.2\|1.5.2 | 11.5.2\|1.5.2 |
| nilai_kerugian | rupiah | rupiah | sama dengan nilai_kerusakan | 11.5.2\|1.5.2 | 11.5.2\|1.5.2 |
| EN.CLC.MDAT.ZS | — | persen | name: '(% of population, average 1990-2009)' | — | — |

## Koreksi katalog

| seri_kode | koreksi_katalog |
|---|---|
| luas_sawah_rusak | tingkat provinsi -> nasional; satuan tidak_ada -> hektar (dugaan) |
| luas_lahan_kebun_hutan_rusak | tingkat provinsi -> nasional; satuan tidak_ada -> hektar (dugaan) |

## Catatan BPS (var.note)

Tidak ada seri BPS.

## Metadata WDI yang muncul di lebih dari satu berkas

| seri | jumlah_entri | berkas | isi_sama |
|---|---|---|---|
| EN.CLC.MDAT.ZS | 2 | sumber2_indikator.json, sumber46_indikator.json | ya |

## Judul dengan spasi di awal/akhir

Tidak ada.
