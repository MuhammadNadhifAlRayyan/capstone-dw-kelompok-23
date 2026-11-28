# Ekstraksi: jumlah baris per berkas

Dihasilkan `python pipeline.py`. Peran *data* berisi angka; *meta* berisi judul, definisi, atau catatan unduhan. Semua baris `data/raw/MANIFEST.csv` tertangani.

| berkas | pembaca | peran | baris | catatan |
|---|---|---|---|---|
| bnpb/2026-10-20/ckan/package_search-pusdatinkom-01.json | bnpb_ckan | meta | 355 | 78 dataset, 355 resource; judul resource = nama ukuran |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/03d7c28f-db2d-4fa3-a1e9-66109d7162d5.json | bnpb_sel | data | 4 | DataStore 2 record; tata nilai/kabkota; 0 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/1e489e0a-77a1-4ac5-9511-ce436aee0132.json | bnpb_sel | data | 124 | DataStore 9 record; tata tahun/nasional; 11 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/21044ffd-c397-4b3c-acbd-5adaa03d79e3.json | bnpb_sel | data | 7650 | DataStore 510 record; tata tahun/kabkota; 0 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/27bbeb6b-6f86-4490-840a-c1bc6393102b.json | bnpb_sel | data | 134 | DataStore 9 record; tata tahun/nasional; 1 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/308f0499-7b3f-4733-8071-a7148bf65e50.json | bnpb_sel | data | 351 | DataStore 39 record; tata jenis/provinsi; 0 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/36ec22b9-27f6-4aa4-a3a8-595fca2fe5c1.json | bnpb_sel | data | 4 | DataStore 2 record; tata nilai/kabkota; 0 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/471f71cb-27a4-4460-836f-416c0c35b4dc.json | bnpb_sel | data | 351 | DataStore 39 record; tata jenis/provinsi; 0 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/4dac65ee-a826-4ba7-8f97-63047b842cfd.json | bnpb_sel | data | 134 | DataStore 9 record; tata tahun/nasional; 1 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/520b34fd-a047-46a4-b595-e8b1d57faba1.json | bnpb_sel | data | 34 | DataStore 17 record; tata nilai/kabkota; 0 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/53f8dc76-8fac-49b1-8314-79948649a345.json | bnpb_sel | data | 96 | DataStore 48 record; tata nilai/kabkota; 0 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/5dfcae7e-acb3-4548-82b5-61d876ea478a.json | bnpb_sel | data | 570 | DataStore 38 record; tata tahun/provinsi; 0 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/69882257-7893-4eca-9f8a-c1391d4ed788.json | bnpb_sel | data | 134 | DataStore 9 record; tata tahun/nasional; 1 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/759ee230-c78c-48a1-bf0d-9596accb524c.json | bnpb_sel | data | 134 | DataStore 9 record; tata tahun/nasional; 1 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/9b41007e-c998-456b-8cbc-385b17986e46.json | bnpb_sel | data | 135 | DataStore 9 record; tata tahun/nasional; 0 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/a4daec53-1119-43ef-b05e-00ec3a4c42a4.json | bnpb_sel | data | 4059 | DataStore 451 record; tata jenis/kabkota; 0 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/a66a93b0-1773-4928-ba1e-7b9ffd43b439.json | bnpb_sel | data | 48 | DataStore 24 record; tata nilai/kabkota; 0 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/b1aa4eb5-d325-44f1-8598-7cdf44073173.json | bnpb_sel | data | 80 | DataStore 40 record; tata nilai/kabkota; 0 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/b2b878ac-988e-4ef3-8deb-c279b1097dac.json | bnpb_sel | data | 134 | DataStore 9 record; tata tahun/nasional; 1 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/bcf4f458-dcbc-4211-8bd2-db25e7aa45e6.json | bnpb_sel | data | 90 | DataStore 45 record; tata nilai/kabkota; 0 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/c013b8a0-4af3-416a-aec2-00feb6dd20a7.json | bnpb_sel | data | 68 | DataStore 34 record; tata nilai/kabkota; 0 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/cda5f236-01f8-4b1f-945d-192806480fac.json | bnpb_sel | data | 124 | DataStore 9 record; tata tahun/nasional; 11 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/cf6d0735-b669-4059-aacb-2d9f31350661.json | bnpb_sel | data | 76 | DataStore 38 record; tata nilai/kabkota; 0 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/e2c2ed75-c2c4-4f3b-90e3-3565b516c3f0.json | bnpb_sel | data | 122 | DataStore 61 record; tata nilai/kabkota; 0 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/f34f5637-b0e0-4920-b0cf-94792588d6ce.json | bnpb_sel | data | 134 | DataStore 9 record; tata tahun/nasional; 1 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/faeb2406-b800-4b8e-9e09-37d4b2aa5879.json | bnpb_sel | data | 351 | DataStore 39 record; tata jenis/provinsi; 0 sel kosong |
| bnpb/2026-10-20/datastore/data-bencana-indonesia/fefc94c0-5275-4d12-899e-1d517f6c8f7c.json | bnpb_sel | data | 620 | DataStore 310 record; tata nilai/kabkota; 0 sel kosong |
| bnpb/2026-10-20/datastore/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/26858365-9061-4ff7-9ccf-53480c6efb61.json | bnpb_sel | data | 351 | DataStore 39 record; tata jenis/provinsi; 0 sel kosong |
| bnpb/2026-10-20/datastore/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/353da3aa-9ada-42aa-a5c2-e653d52ffd9c.json | bnpb_sel | data | 4059 | DataStore 451 record; tata jenis/kabkota; 0 sel kosong |
| bnpb/2026-10-20/datastore/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/5c9f7ea9-f809-487c-b1f8-f05a6f3291b3.json | bnpb_sel | data | 4059 | DataStore 451 record; tata jenis/kabkota; 0 sel kosong |
| bnpb/2026-10-20/datastore/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/5f69273d-7755-4a5f-82f7-617303ba78ec.json | bnpb_sel | data | 351 | DataStore 39 record; tata jenis/provinsi; 0 sel kosong |
| bnpb/2026-10-20/datastore/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/5ff9f41f-8312-4b7c-aa18-fdbedac6ee7e.json | bnpb_sel | data | 4059 | DataStore 451 record; tata jenis/kabkota; 0 sel kosong |
| bnpb/2026-10-20/datastore/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/76c8231d-75e8-4e8e-bb9a-1b35ba6ed1f3.json | bnpb_sel | data | 351 | DataStore 39 record; tata jenis/provinsi; 0 sel kosong |
| bnpb/2026-10-20/datastore/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/8eea8adc-3c4d-4d0d-be9f-6d170127ff6c.json | bnpb_sel | data | 4059 | DataStore 451 record; tata jenis/kabkota; 0 sel kosong |
| bnpb/2026-10-20/datastore/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/ad86fca8-b15b-4fb6-b30c-259ab32e3113.json | bnpb_sel | data | 351 | DataStore 39 record; tata jenis/provinsi; 0 sel kosong |
| bnpb/2026-10-20/datastore/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/b5e3d843-cf11-4333-b8e3-233a2279b65a.json | bnpb_sel | data | 351 | DataStore 39 record; tata jenis/provinsi; 0 sel kosong |
| bnpb/2026-10-20/datastore/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/caefcb96-50a3-4a32-af0f-9ccc4bbcf487.json | bnpb_sel | data | 4059 | DataStore 451 record; tata jenis/kabkota; 0 sel kosong |
| bnpb/2026-10-20/datastore/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/d81153ed-d515-4d03-be64-6591c83b9539.json | bnpb_sel | data | 4059 | DataStore 451 record; tata jenis/kabkota; 0 sel kosong |
| bnpb/2026-10-20/datastore/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/f345ba43-99aa-428c-82d8-4b6a0bba380e.json | bnpb_sel | data | 351 | DataStore 39 record; tata jenis/provinsi; 0 sel kosong |
| bnpb/2026-10-20/tangan/data-bencana-indonesia/5f3bdd4d-b7e1-4249-9cb5-85636f1d1a49-jumlah-rumah-ibadat-yang-rusak-akibat-bencana-menurut-provinsi-2024.xlsx | bnpb_sel | data | 351 | XLSX 1 lembar data; tata jenis/provinsi; 0 sel kosong; lembar Keterangan 15 baris |
| bnpb/2026-10-20/tangan/data-bencana-indonesia/742bb9f9-3496-48d8-949f-0b86c5502799-jumlah-kantor-yang-rusak-akibat-bencana-menurut-provinsi-2024.xlsx | bnpb_sel | data | 351 | XLSX 1 lembar data; tata jenis/provinsi; 0 sel kosong; lembar Keterangan 15 baris |
| bnpb/2026-10-20/tangan/data-bencana/0c165adc-5be2-489d-8b1a-e90c6715e73e-tabel-jumlah-kejadian-korban-dan-kerusakan-akibat-bencana-tahun-2021-per-provinsi.xlsx | bnpb_sel | data | 2310 | XLSX 1 lembar data; tata rekap/provinsi; 0 sel kosong |
| bnpb/2026-10-20/tangan/data-bencana/692df9e1-a8f8-49b3-a78f-de5795fb6e79-tabel-jumlah-kejadian-korban-dan-kerusakan-akibat-bencana-tahun-2022-per-provinsi.xlsx | bnpb_sel | data | 1974 | XLSX 1 lembar data; tata rekap/provinsi; 0 sel kosong |
| bnpb/2026-10-20/tangan/data-bencana/6ec0418d-1590-45c3-b731-9fa1ab2af5c8-tabel-jumlah-kejadian-korban-dan-kerusakan-akibat-bencana-tahun-2021-per-kabupaten-kota.xlsx | bnpb_sel | data | 16170 | XLSX 1 lembar data; tata rekap/kabkota; 0 sel kosong |
| bnpb/2026-10-20/tangan/data-bencana/9170802b-7f71-4d8f-a326-8e478d0463e8-tabel-jumlah-kejadian-korban-dan-kerusakan-akibat-bencana-tahun-2022-per-kabupten-kota.xlsx | bnpb_sel | data | 12754 | XLSX 1 lembar data; tata rekap/kabkota; 0 sel kosong |
| bnpb/2026-10-20/tangan/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/091da066-4aca-4699-bd51-a2452f371778-jumlah-kantor-yang-rusak-akibat-bencana-menurut-provinsi-2024.xlsx | bnpb_sel | data | 351 | XLSX 1 lembar data; tata jenis/provinsi; 0 sel kosong; lembar Keterangan 15 baris |
| bnpb/2026-10-20/tangan/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/11ba1fdc-27cc-46e3-b75b-f4ec545dcf8f-jumlah-pabrik-rusak-akibat-bencana-menurut-kabupaten-2024.xlsx | bnpb_sel | data | 4059 | XLSX 1 lembar data; tata jenis/kabkota; 0 sel kosong; lembar Keterangan 15 baris |
| bnpb/2026-10-20/tangan/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/135f1962-4cb7-4634-a284-ff440a21a70c-jumlah-kios-yang-rusak-akibat-bencana-menurut-kabupaten-2024.xlsx | bnpb_sel | data | 4059 | XLSX 1 lembar data; tata jenis/kabkota; 0 sel kosong; lembar Keterangan 15 baris |
| bnpb/2026-10-20/tangan/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/200c487f-e0fc-4dd3-8cf0-b4222d460229-jumlah-rumah-ibadat-yang-rusak-akibat-bencana-menurut-provinsi-2024.xlsx | bnpb_sel | data | 351 | XLSX 1 lembar data; tata jenis/provinsi; 0 sel kosong; lembar Keterangan 15 baris |
| bnpb/2026-10-20/tangan/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/cbc56396-4cfa-4959-b9bd-38bf9d4a2d6c-jumlah-kios-yang-rusak-akibat-bencana-menurut-provinsi-2024.xlsx | bnpb_sel | data | 351 | XLSX 1 lembar data; tata jenis/provinsi; 0 sel kosong; lembar Keterangan 15 baris |
| bnpb/2026-10-20/tangan/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/fdebc70a-2305-4b25-9fa7-e876892b0f54-jumlah-jembatan-rusak-akibat-bencana-menurut-kabupaten-2024.xlsx | bnpb_sel | data | 4059 | XLSX 1 lembar data; tata jenis/kabkota; 0 sel kosong; lembar Keterangan 15 baris |
| bnpb/2026-10-20/tangan/kompilasi-data-kejadian-dan-dampak-bencana-2025/43b83e79-c8b6-4b9a-b2f0-d1cbd9cfa636-jumlah-rumah-rusak-akibat-bencana-menurut-provinsi-2025.xlsx | bnpb_sel | data | 351 | XLSX 1 lembar data; tata jenis/provinsi; 0 sel kosong; lembar Keterangan 15 baris |
| bnpb/2026-10-20/tangan/kompilasi-data-kejadian-dan-dampak-bencana-2025/6e947c9c-2404-4c02-b743-34dc5320f399-rekapitulasi-jumlah-kejadian-dan-dampak-bencana-menurut-provinsi-2025.xlsx | bnpb_sel | data | 140 | XLSX 1 lembar data; tata rekap_nasional/nasional; 0 sel kosong; lembar Keterangan 15 baris |
| bnpb/2026-10-20/tangan/kompilasi-data-kejadian-dan-dampak-bencana-2025/df39e8c3-117e-40fa-b518-ff1037743955-jumlah-kejadian-bencana-menurut-provinsi-2025.xlsx | bnpb_sel | data | 351 | XLSX 1 lembar data; tata jenis/provinsi; 0 sel kosong; lembar Keterangan 15 baris |
| wdi/2026-10-20/data/kelompok-01-hal-01.json | wdi_data | data | 66 | 3,960 baris di berkas, 1 seri kasus disaring |
| wdi/2026-10-20/metadata/sumber.json | wdi_sumber | meta | 71 |  |
| wdi/2026-10-20/metadata/sumber2_indikator.json | wdi_meta | meta | 1 | metadata seri kasus saja |
| wdi/2026-10-20/metadata/sumber46_indikator.json | wdi_meta | meta | 1 | metadata seri kasus saja |

Jumlah: 58 berkas dari 58 di MANIFEST, 90,269 baris mentah di berkas data.
