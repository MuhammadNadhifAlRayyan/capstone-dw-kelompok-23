# Tahap 3 — Grid panel dan kelengkapan wilayah

## Aturan grid dan missing

- Grid berisi 8,512 sel (14 seri × 16 tahun × 38 provinsi); baris Indonesia disimpan terpisah di `observasi-nasional-tahap-3.csv`.
- Input provinsi berisi 1,674 observasi seri-provinsi-periode; ini adalah grain keluaran profil tahap 2, bukan klaim jumlah seluruh baris tabel Silver mentah.
- `terisi` hanya menyalin nilai dari sumber provinsi; `kosong_dalam_sumber` hanya dipakai jika sumber provinsi tersedia tetapi provinsinya tidak memiliki observasi.
- `tidak_ada_sumber_provinsi` tidak dihitung sebagai missing. Nilai sel kosong tidak diisi nol.
- `nilai_sumber_asli` dipertahankan untuk audit. Nilai provinsi pemekaran sebelum tahun pembentukan tidak dipakai pada `nilai` dan berstatus `wilayah_belum_terbentuk`.
- Denominator kelengkapan mengikuti jumlah provinsi yang sudah terbentuk pada tahun itu (33 pada 2010–2011; 34 pada 2012–2021; 38 mulai 2022).

## Kelengkapan pada tahun dengan sumber provinsi

| Seri | Tahun | Terisi | Kosong | Denominator aktif | Persen |
|---|---:|---:|---:|---:|---:|
| fasyankes_rusak | 2021 | 33 | 1 | 34 | 97.1% |
| fasyankes_rusak | 2022 | 33 | 5 | 38 | 86.8% |
| fasyankes_rusak | 2024 | 38 | 0 | 38 | 100.0% |
| jembatan_rusak | 2021 | 33 | 1 | 34 | 97.1% |
| jembatan_rusak | 2022 | 33 | 5 | 38 | 86.8% |
| jembatan_rusak | 2024 | 38 | 0 | 38 | 100.0% |
| kantor_rusak | 2021 | 33 | 1 | 34 | 97.1% |
| kantor_rusak | 2022 | 33 | 5 | 38 | 86.8% |
| kantor_rusak | 2024 | 38 | 0 | 38 | 100.0% |
| kejadian | 2010 | 33 | 0 | 33 | 100.0% |
| kejadian | 2011 | 33 | 0 | 33 | 100.0% |
| kejadian | 2012 | 34 | 0 | 34 | 100.0% |
| kejadian | 2013 | 34 | 0 | 34 | 100.0% |
| kejadian | 2014 | 34 | 0 | 34 | 100.0% |
| kejadian | 2015 | 34 | 0 | 34 | 100.0% |
| kejadian | 2016 | 34 | 0 | 34 | 100.0% |
| kejadian | 2017 | 34 | 0 | 34 | 100.0% |
| kejadian | 2018 | 34 | 0 | 34 | 100.0% |
| kejadian | 2019 | 34 | 0 | 34 | 100.0% |
| kejadian | 2020 | 34 | 0 | 34 | 100.0% |
| kejadian | 2021 | 34 | 0 | 34 | 100.0% |
| kejadian | 2022 | 38 | 0 | 38 | 100.0% |
| kejadian | 2023 | 38 | 0 | 38 | 100.0% |
| kejadian | 2024 | 38 | 0 | 38 | 100.0% |
| kejadian | 2025 | 38 | 0 | 38 | 100.0% |
| kios_toko_rusak | 2024 | 38 | 0 | 38 | 100.0% |
| nilai_kerugian | 2015 | 1 | 33 | 34 | 2.9% |
| nilai_kerugian | 2016 | 6 | 28 | 34 | 17.6% |
| nilai_kerugian | 2017 | 24 | 10 | 34 | 70.6% |
| nilai_kerugian | 2018 | 17 | 17 | 34 | 50.0% |
| nilai_kerugian | 2019 | 14 | 20 | 34 | 41.2% |
| nilai_kerugian | 2020 | 13 | 21 | 34 | 38.2% |
| nilai_kerugian | 2021 | 21 | 13 | 34 | 61.8% |
| nilai_kerugian | 2022 | 15 | 23 | 38 | 39.5% |
| nilai_kerugian | 2023 | 12 | 26 | 38 | 31.6% |
| nilai_kerugian | 2024 | 2 | 36 | 38 | 5.3% |
| nilai_kerusakan | 2015 | 1 | 33 | 34 | 2.9% |
| nilai_kerusakan | 2016 | 6 | 28 | 34 | 17.6% |
| nilai_kerusakan | 2017 | 24 | 10 | 34 | 70.6% |
| nilai_kerusakan | 2018 | 17 | 17 | 34 | 50.0% |
| nilai_kerusakan | 2019 | 14 | 20 | 34 | 41.2% |
| nilai_kerusakan | 2020 | 13 | 21 | 34 | 38.2% |
| nilai_kerusakan | 2021 | 21 | 13 | 34 | 61.8% |
| nilai_kerusakan | 2022 | 15 | 23 | 38 | 39.5% |
| nilai_kerusakan | 2023 | 12 | 26 | 38 | 31.6% |
| nilai_kerusakan | 2024 | 2 | 36 | 38 | 5.3% |
| pabrik_rusak | 2024 | 38 | 0 | 38 | 100.0% |
| rumah_ibadat_rusak | 2021 | 33 | 1 | 34 | 97.1% |
| rumah_ibadat_rusak | 2022 | 33 | 5 | 38 | 86.8% |
| rumah_ibadat_rusak | 2024 | 38 | 0 | 38 | 100.0% |
| rumah_rusak | 2021 | 33 | 1 | 34 | 97.1% |
| rumah_rusak | 2022 | 33 | 5 | 38 | 86.8% |
| rumah_rusak | 2024 | 38 | 0 | 38 | 100.0% |
| rumah_rusak | 2025 | 38 | 0 | 38 | 100.0% |
| rumah_terendam | 2021 | 33 | 1 | 34 | 97.1% |
| rumah_terendam | 2022 | 33 | 5 | 38 | 86.8% |
| satuan_pendidikan_rusak | 2021 | 33 | 1 | 34 | 97.1% |
| satuan_pendidikan_rusak | 2022 | 33 | 5 | 38 | 86.8% |
| satuan_pendidikan_rusak | 2024 | 38 | 0 | 38 | 100.0% |

Tahun di luar rentang katalog dan tahun tanpa sumber provinsi tetap tercantum di grid, tetapi tidak masuk denominator kelengkapan. Rincian setiap sel ada di `grid-provinsi-tahap-3.csv`; rekap semua seri-tahun ada di `kelengkapan-panel-per-tahun.csv`.

## Matriks tingkat wilayah

Matriks `ketersediaan-seri-wilayah-tahap-3.csv` membedakan sumber nasional, provinsi, dan kabupaten/kota untuk seluruh seri dan 2010–2025. Rekap proposal nilai kerusakan/kerugian memuat catatan tingkat kabupaten; agregat provinsi tahap 2 tidak diperlakukan sebagai tabel provinsi independen.

## Kamus rumah rusak

Kamus kategori mencakup 9 jenis bencana baku dan tingkat berat/sedang/ringan/total. Tabel rincian terharmonisasi memiliki 14,392 baris: 2021–2022 memuat tingkat kerusakan, sumber nasional historis dan tabel 2024 tidak memisahkan tingkat, sedangkan rekap nasional 2025 menyediakan tingkat per jenis bencana. Tsunami tidak muncul pada tabel XLSX provinsi/kabupaten 2021–2022.
Alias `Letusan Gunung Api` disatukan dengan `ERUPSI GUNUNG API`; `Gempa Bumi` dengan `GEMPABUMI`; dan variasi penulisan gelombang pasang disatukan. Kategori yang tidak tersedia dibiarkan tanpa nilai, bukan nol.

Lihat `kamus-rincian-rumah-rusak.csv` dan `rincian-rumah-rusak-harmonisasi.csv`.

## Audit jumlah kabupaten/kota ke provinsi

| Seri | Tahun | Pasangan wilayah | Cocok | Berbeda | Tanpa pasangan |
|---|---:|---:|---:|---:|---:|
| fasyankes_rusak | 2021 | 34 | 34 | 0 | 0 |
| fasyankes_rusak | 2022 | 34 | 34 | 0 | 0 |
| fasyankes_rusak | 2024 | 38 | 38 | 0 | 0 |
| jembatan_rusak | 2021 | 34 | 34 | 0 | 0 |
| jembatan_rusak | 2022 | 34 | 34 | 0 | 0 |
| jembatan_rusak | 2024 | 38 | 38 | 0 | 0 |
| kantor_rusak | 2021 | 34 | 34 | 0 | 0 |
| kantor_rusak | 2022 | 34 | 34 | 0 | 0 |
| kantor_rusak | 2024 | 38 | 38 | 0 | 0 |
| kejadian | 2010 | 38 | 24 | 14 | 0 |
| kejadian | 2011 | 38 | 30 | 8 | 0 |
| kejadian | 2012 | 38 | 33 | 5 | 0 |
| kejadian | 2013 | 38 | 26 | 12 | 0 |
| kejadian | 2014 | 38 | 31 | 7 | 0 |
| kejadian | 2015 | 38 | 36 | 2 | 0 |
| kejadian | 2016 | 38 | 34 | 4 | 0 |
| kejadian | 2017 | 38 | 32 | 6 | 0 |
| kejadian | 2018 | 38 | 28 | 10 | 0 |
| kejadian | 2019 | 38 | 28 | 10 | 0 |
| kejadian | 2020 | 38 | 30 | 8 | 0 |
| kejadian | 2021 | 38 | 28 | 10 | 0 |
| kejadian | 2021 | 34 | 24 | 10 | 0 |
| kejadian | 2022 | 38 | 28 | 10 | 0 |
| kejadian | 2022 | 34 | 24 | 10 | 0 |
| kejadian | 2023 | 38 | 18 | 20 | 0 |
| kejadian | 2024 | 38 | 31 | 7 | 0 |
| kejadian | 2024 | 38 | 31 | 7 | 0 |
| kios_toko_rusak | 2024 | 38 | 38 | 0 | 0 |
| pabrik_rusak | 2024 | 38 | 38 | 0 | 0 |
| rumah_ibadat_rusak | 2021 | 34 | 34 | 0 | 0 |
| rumah_ibadat_rusak | 2022 | 34 | 34 | 0 | 0 |
| rumah_ibadat_rusak | 2024 | 38 | 38 | 0 | 0 |
| rumah_rusak | 2021 | 34 | 34 | 0 | 0 |
| rumah_rusak | 2022 | 34 | 34 | 0 | 0 |
| rumah_rusak | 2024 | 38 | 36 | 2 | 0 |
| rumah_terendam | 2021 | 34 | 34 | 0 | 0 |
| rumah_terendam | 2022 | 34 | 34 | 0 | 0 |
| satuan_pendidikan_rusak | 2021 | 34 | 34 | 0 | 0 |
| satuan_pendidikan_rusak | 2022 | 34 | 34 | 0 | 0 |
| satuan_pendidikan_rusak | 2024 | 38 | 38 | 0 | 0 |

Audit memakai sumber kabupaten dan provinsi yang tersedia secara berpasangan; nilai tidak disesuaikan. Untuk kejadian historis, perbandingan mencakup 2010–2024; untuk dampak 2021–2022 memakai XLSX rekap; dan untuk 2024 memakai tabel kompilasi provinsi/kabupaten. Proposal nilai kerusakan/kerugian tidak dibandingkan karena agregat provinsinya dibentuk dari catatan proposal yang sama, bukan pembanding independen.

Jumlah calon anomali yang tetap ditandai: 201. Tidak ada outlier yang dihapus atau diperbaiki pada tahap ini.
