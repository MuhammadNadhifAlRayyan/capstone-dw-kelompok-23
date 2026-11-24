# Data dictionary — Kasus 23 Kerusakan dan kerugian bencana

Ditulis ulang otomatis oleh `python pipeline.py` (`src/dokumen.py`). Tipe, rentang, dan jumlah kosong dihitung dari `data/silver/silver.parquet`.

## data/silver/silver.parquet (18,187 baris)

Satu baris = satu seri x wilayah x periode x rincian x berkas sumber. Kunci unik: sumber, seri_kode, wilayah_kode, periode, rincian, _berkas_raw.

| kolom | tipe | kosong | rentang_atau_nilai | asal | arti |
|---|---|---|---|---|---|
| sumber | str | 0 | bnpb, wdi | nama folder sumber di data/raw/ | lembaga penerbit: bps, wdi, who_gho, ilostat, bnpb |
| seri_kode | str | 0 | EN.CLC.MDAT.ZS, fasyankes_rusak, jembatan_rusak, kantor_rusak, kejadian, kios_toko_rusak, … (15 nilai) | kode seri di sumbernya (BPS: 'var' + var.val) | identitas seri; arti lengkap di docs/seri.csv |
| wilayah_kode | int64 | 0 | 1100 – 9999 | kamus src/wilayah.py; log K-001 | kode BPS dua digit x 100; 9999 = Indonesia |
| nama_wilayah | str | 0 | Aceh, Bali, Banten, Bengkulu, DI Yogyakarta, DKI Jakarta, … (39 nilai) | kamus src/wilayah.py | nama baku susunan 38 provinsi 2025, bukan label sumber |
| periode | str | 0 | 2009, 2010, 2011, 2012, 2013, 2014, … (17 nilai) | tahun/turtahun BPS, date WDI, DIM_TIME WHO | bentuk baku: 2019, 2019-S1, 2019-Q3, 2019-07 |
| jenis_periode | str | 0 | tahun | diturunkan dari periode | tahun, semester, triwulan, atau bulan |
| rincian | str | 0 | jenis_bencana=banjir, jenis_bencana=banjir;tingkat_kerusakan=berat, jenis_bencana=banjir;tingkat_kerusakan=ringan, jenis_bencana=banjir;tingkat_kerusakan=sedang, jenis_bencana=cuaca_ekstrem, jenis_bencana=cuaca_ekstrem;tingkat_kerusakan=berat, … (40 nilai) | turvar BPS; kolom DIM_* WHO yang bervariasi | 'total' atau 'dimensi=kode;...'; lihat kamus di bawah |
| nilai | float64 | 0 | 0 – 2.87265e+13 | datacontent BPS; value WDI; RATE_*_N WHO | angka sesuai satuan; baris tanpa angka tidak masuk Silver |
| satuan | str | 0 | hektar, kejadian, persen, rupiah, unit | src/konfigurasi.py, bukti di docs/seri.csv | satuan baku; satu satuan per seri |
| sdg_kode | str | 0 | 11.5.2, 11.5.2\|1.5.2, — | src/konfigurasi.py, bukti di docs/seri.csv | kode indikator SDG (kolom tambahan) |
| batas_bawah | float64 | 18187 | — | RATE_*_NL WHO | batas bawah ketidakpastian; kosong bila sumber tidak memberi |
| batas_atas | float64 | 18187 | — | RATE_*_NU WHO | batas atas ketidakpastian; kosong bila sumber tidak memberi |
| rujukan_tahun | Int64 | 18187 | — | var.note BPS; log | lebar jendela rujukan survei (tahun sebelum survei); kosong bila tidak berlaku |
| _berkas_raw | str | 0 | bnpb/2026-10-20/datastore/data-bencana-indonesia/03d7c28f-db2d-4fa3-a1e9-66109d7162d5.json, bnpb/2026-10-20/datastore/data-bencana-indonesia/1e489e0a-77a1-4ac5-9511-ce436aee0132.json, bnpb/2026-10-20/datastore/data-bencana-indonesia/21044ffd-c397-4b3c-acbd-5adaa03d79e3.json, bnpb/2026-10-20/datastore/data-bencana-indonesia/27bbeb6b-6f86-4490-840a-c1bc6393102b.json, bnpb/2026-10-20/datastore/data-bencana-indonesia/308f0499-7b3f-4733-8071-a7148bf65e50.json, bnpb/2026-10-20/datastore/data-bencana-indonesia/36ec22b9-27f6-4aa4-a3a8-595fca2fe5c1.json, … (54 nilai) | jalur berkas mentah relatif data/raw/ | lineage: berkas asal baris ini |
| _sha256_raw | str | 0 | 023ba025e25e18040f0291a542a95447efecf1bfd39c745a3887b39f5da40cd0, 0467ad3004914308c03472fe97fbd263ea99743e06c2b19c73c095108365e832, 1863865aec5781a59452ec66a6211c54441a206d686a3d1b9e31a5eace6e16b6, 1925a9ac1fe60238f0b068f15e349331ab92b27dcc16984bf0678a4b964afbe9, 2240e000c822a242501c0b8650c8757c1df17ec081b2fb9b10a2ec9c87558519, 23c28e0c04624a9e81d96d0966f3312e8c905ec70813d6dc649930e5368f5c16, … (52 nilai) | src.common.manifest.sha256_raw | lineage: sidik isi berkas asal, dicocokkan dengan MANIFEST.csv |

## Kamus rincian

Aturan menulis rincian (log): dimensi yang bervariasi ditulis `nama=kode`, dipisah `;`, urut abjad; nilai total sumber dibuang; baris tanpa dimensi bervariasi ditulis `total`. Dimensi yang nilainya tetap di seluruh berkas dianggap bagian definisi seri dan dicatat di kolom `cakupan` docs/seri.csv.

Nama dimensi dan kode yang sah:

- `jenis_bencana`: `banjir`, `cuaca_ekstrem`, `erupsi_gunung_api`, `gelombang_pasang_dan_abrasi`, `gempabumi`, `kebakaran_hutan_dan_lahan`, `kekeringan`, `tanah_longsor`, `tsunami`
- `tingkat_kerusakan`: `berat`, `ringan`, `sedang`

| rincian | dipakai_seri |
|---|---|
| jenis_bencana=banjir | fasyankes_rusak, jembatan_rusak, kantor_rusak, kejadian, kios_toko_rusak, luas_lahan_kebun_hutan_rusak, luas_sawah_rusak, pabrik_rusak, rumah_ibadat_rusak, rumah_rusak, rumah_terendam, satuan_pendidikan_rusak |
| jenis_bencana=banjir;tingkat_kerusakan=berat | rumah_rusak |
| jenis_bencana=banjir;tingkat_kerusakan=ringan | rumah_rusak |
| jenis_bencana=banjir;tingkat_kerusakan=sedang | rumah_rusak |
| jenis_bencana=cuaca_ekstrem | fasyankes_rusak, jembatan_rusak, kantor_rusak, kejadian, kios_toko_rusak, luas_lahan_kebun_hutan_rusak, luas_sawah_rusak, pabrik_rusak, rumah_ibadat_rusak, rumah_rusak, rumah_terendam, satuan_pendidikan_rusak |
| jenis_bencana=cuaca_ekstrem;tingkat_kerusakan=berat | rumah_rusak |
| jenis_bencana=cuaca_ekstrem;tingkat_kerusakan=ringan | rumah_rusak |
| jenis_bencana=cuaca_ekstrem;tingkat_kerusakan=sedang | rumah_rusak |
| jenis_bencana=erupsi_gunung_api | fasyankes_rusak, jembatan_rusak, kantor_rusak, kejadian, kios_toko_rusak, luas_lahan_kebun_hutan_rusak, luas_sawah_rusak, pabrik_rusak, rumah_ibadat_rusak, rumah_rusak, rumah_terendam, satuan_pendidikan_rusak |
| jenis_bencana=erupsi_gunung_api;tingkat_kerusakan=berat | rumah_rusak |
| jenis_bencana=erupsi_gunung_api;tingkat_kerusakan=ringan | rumah_rusak |
| jenis_bencana=erupsi_gunung_api;tingkat_kerusakan=sedang | rumah_rusak |
| jenis_bencana=gelombang_pasang_dan_abrasi | fasyankes_rusak, jembatan_rusak, kantor_rusak, kejadian, kios_toko_rusak, luas_lahan_kebun_hutan_rusak, luas_sawah_rusak, pabrik_rusak, rumah_ibadat_rusak, rumah_rusak, rumah_terendam, satuan_pendidikan_rusak |
| jenis_bencana=gelombang_pasang_dan_abrasi;tingkat_kerusakan=berat | rumah_rusak |
| jenis_bencana=gelombang_pasang_dan_abrasi;tingkat_kerusakan=ringan | rumah_rusak |
| jenis_bencana=gelombang_pasang_dan_abrasi;tingkat_kerusakan=sedang | rumah_rusak |
| jenis_bencana=gempabumi | fasyankes_rusak, jembatan_rusak, kantor_rusak, kejadian, kios_toko_rusak, luas_lahan_kebun_hutan_rusak, luas_sawah_rusak, pabrik_rusak, rumah_ibadat_rusak, rumah_rusak, rumah_terendam, satuan_pendidikan_rusak |
| jenis_bencana=gempabumi;tingkat_kerusakan=berat | rumah_rusak |
| jenis_bencana=gempabumi;tingkat_kerusakan=ringan | rumah_rusak |
| jenis_bencana=gempabumi;tingkat_kerusakan=sedang | rumah_rusak |
| jenis_bencana=kebakaran_hutan_dan_lahan | fasyankes_rusak, jembatan_rusak, kantor_rusak, kejadian, kios_toko_rusak, luas_lahan_kebun_hutan_rusak, luas_sawah_rusak, pabrik_rusak, rumah_ibadat_rusak, rumah_rusak, rumah_terendam, satuan_pendidikan_rusak |
| jenis_bencana=kebakaran_hutan_dan_lahan;tingkat_kerusakan=berat | rumah_rusak |
| jenis_bencana=kebakaran_hutan_dan_lahan;tingkat_kerusakan=ringan | rumah_rusak |
| jenis_bencana=kebakaran_hutan_dan_lahan;tingkat_kerusakan=sedang | rumah_rusak |
| jenis_bencana=kekeringan | fasyankes_rusak, jembatan_rusak, kantor_rusak, kejadian, kios_toko_rusak, luas_lahan_kebun_hutan_rusak, luas_sawah_rusak, pabrik_rusak, rumah_ibadat_rusak, rumah_rusak, rumah_terendam, satuan_pendidikan_rusak |
| jenis_bencana=kekeringan;tingkat_kerusakan=berat | rumah_rusak |
| jenis_bencana=kekeringan;tingkat_kerusakan=ringan | rumah_rusak |
| jenis_bencana=kekeringan;tingkat_kerusakan=sedang | rumah_rusak |
| jenis_bencana=tanah_longsor | fasyankes_rusak, jembatan_rusak, kantor_rusak, kejadian, kios_toko_rusak, luas_lahan_kebun_hutan_rusak, luas_sawah_rusak, pabrik_rusak, rumah_ibadat_rusak, rumah_rusak, rumah_terendam, satuan_pendidikan_rusak |
| jenis_bencana=tanah_longsor;tingkat_kerusakan=berat | rumah_rusak |
| jenis_bencana=tanah_longsor;tingkat_kerusakan=ringan | rumah_rusak |
| jenis_bencana=tanah_longsor;tingkat_kerusakan=sedang | rumah_rusak |
| jenis_bencana=tsunami | fasyankes_rusak, jembatan_rusak, kantor_rusak, kejadian, kios_toko_rusak, luas_lahan_kebun_hutan_rusak, luas_sawah_rusak, pabrik_rusak, rumah_ibadat_rusak, rumah_rusak, satuan_pendidikan_rusak |
| jenis_bencana=tsunami;tingkat_kerusakan=berat | rumah_rusak |
| jenis_bencana=tsunami;tingkat_kerusakan=ringan | rumah_rusak |
| jenis_bencana=tsunami;tingkat_kerusakan=sedang | rumah_rusak |
| tingkat_kerusakan=berat | rumah_rusak |
| tingkat_kerusakan=ringan | rumah_rusak |
| tingkat_kerusakan=sedang | rumah_rusak |
| total | EN.CLC.MDAT.ZS, fasyankes_rusak, jembatan_rusak, kantor_rusak, kejadian, nilai_kerugian, nilai_kerusakan, rumah_ibadat_rusak, satuan_pendidikan_rusak |

## Satuan, kode SDG, dan cakupan per seri

| seri_kode | satuan | sdg_kode | cakupan | bukti_satuan |
|---|---|---|---|---|
| kejadian | kejadian | — | penyebut kerusakan per kejadian; satu kejadian satu jenis utama (Keterangan) | Keterangan: 'Jumlah Kejadian: Jumlah Total Kejadian Bencana Menurut Klasifikasi Penyajian' |
| rumah_rusak | unit | 11.5.2\|1.5.2 | rekap 2021/2022 per tingkat (berat, sedang, ringan) x jenis; tabel 2024, 2025 per jenis tanpa tingkat; rekap nasional 2025 per tingkat; nasional per jenis 2010–2024 | baris satuan '(unit)' di bawah kepala 'Kerusakan' pada rekap 2021/2022 (XLSX tangan) |
| rumah_terendam | unit | 11.5.2\|1.5.2 | hanya rekap 2021/2022 | baris satuan '(unit)' di bawah kepala 'Kerusakan' pada rekap 2021/2022 (XLSX tangan) |
| fasyankes_rusak | unit | 11.5.2 | kepala rekap 2021/2022 'Sarana Kesehatan'; tabel 2024; rekap nasional 2025; nasional 2010–2024 | baris satuan '(unit)' di bawah kepala 'Kerusakan' pada rekap 2021/2022 (XLSX tangan) |
| satuan_pendidikan_rusak | unit | 11.5.2 | kepala rekap 2021/2022 'Sarana Pendidikan'; tabel 2024; rekap nasional 2025 | baris satuan '(unit)' di bawah kepala 'Kerusakan' pada rekap 2021/2022 (XLSX tangan) |
| jembatan_rusak | unit | 11.5.2 | rekap 2021/2022; tabel 2024; rekap nasional 2025; nasional 2010–2024 | baris satuan '(unit)' di bawah kepala 'Kerusakan' pada rekap 2021/2022 (XLSX tangan) |
| kantor_rusak | unit | — | kepala rekap 2021/2022 'Perkantoran'; tabel 2024; nasional 2010–2024 | baris satuan '(unit)' di bawah kepala 'Kerusakan' pada rekap 2021/2022 (XLSX tangan) |
| rumah_ibadat_rusak | unit | — | kepala rekap 2021/2022 'Sarana Peribadatan'; lembar 2024 'Jumlah Fasdah Rusak' | baris satuan '(unit)' di bawah kepala 'Kerusakan' pada rekap 2021/2022 (XLSX tangan) |
| kios_toko_rusak | unit | 11.5.2\|1.5.2 | tabel 2024; nasional 2010–2024 | baris satuan '(unit)' di bawah kepala 'Kerusakan' pada rekap 2021/2022 (XLSX tangan) |
| pabrik_rusak | unit | 11.5.2\|1.5.2 | hanya tabel 2024 | baris satuan '(unit)' di bawah kepala 'Kerusakan' pada rekap 2021/2022 (XLSX tangan) |
| luas_sawah_rusak | hektar | 11.5.2\|1.5.2 | hanya nasional per jenis 2010–2024 | tabel tidak menyatakan satuan; Keterangan memakai hektar untuk ambang kejadian ('1 hektar lahan terdampak/rusak') dan angkanya berdesimal dua; dugaan, dipastikan dari Juklak Standar Data (katalog) di Sprint 2 |
| luas_lahan_kebun_hutan_rusak | hektar | 11.5.2\|1.5.2 | hanya nasional per jenis 2010–2024 | sama dengan luas_sawah_rusak |
| nilai_kerusakan | rupiah | 11.5.2\|1.5.2 | per kab/kota yang mengajukan proposal rehabilitasi-rekonstruksi, bukan semua kejadian; dijumlah ke provinsi per Tahun Kejadian; usulan beberapa tahun kejadian tidak dipakai | judul resource di ckan/package_search-pusdatinkom-01.json: 'Nilai Kerusakan dan Kerugian ...'; angka sampai satuan rupiah |
| nilai_kerugian | rupiah | 11.5.2\|1.5.2 | sama dengan nilai_kerusakan | sama dengan nilai_kerusakan |
| EN.CLC.MDAT.ZS | persen | — | satu angka rata-rata 1990–2009 yang ditulis sebagai date 2009; mengukur penduduk terdampak, bukan kerusakan | name: '(% of population, average 1990-2009)' |

## Kode wilayah

9999 = Indonesia; provinsi = kode BPS dua digit x 100, susunan 38 provinsi 2025 (38 kode). WDI menulis Indonesia `ID`/`IDN`, WHO GHO menulis `360` (M49); keduanya dipetakan ke 9999 di `src/wilayah.py`.

## Contoh penelusuran satu baris

| sumber | seri_kode | wilayah_kode | periode | rincian | nilai | _berkas_raw | _sha256_raw |
|---|---|---|---|---|---|---|---|
| bnpb | fasyankes_rusak | 1100 | 2021 | jenis_bencana=banjir | 0.00 | bnpb/2026-10-20/tangan/data-bencana/0c165adc-5be2-489d-8b1a-e90c6715e73e-tabel-jumlah-kejadian-korban-dan-kerusakan-akibat-bencana-tahun-2021-per-provinsi.xlsx | e951a1427459df035aaacd3873ce49295422d64debd670b9df8595645db6f963 |

1. `_berkas_raw` menunjuk `data/raw/bnpb/2026-10-20/tangan/data-bencana/0c165adc-5be2-489d-8b1a-e90c6715e73e-tabel-jumlah-kejadian-korban-dan-kerusakan-akibat-bencana-tahun-2021-per-provinsi.xlsx`.

2. Baris berkas itu di `data/raw/MANIFEST.csv` memuat sha256 `e951a1427459…`; nilainya sama dengan `_sha256_raw`, jadi berkas yang dibaca adalah berkas yang tercatat.

3. Di berkas mentah, angka ditemukan pada wilayah, periode, dan rincian yang sama (untuk JSON BPS: kunci `datacontent` = kode wilayah + var + turvar + kode tahun + turtahun).

## data/gold/panel.parquet (5,244 baris)

Satu baris = satu indikator × provinsi × periode, termasuk sel kosong dari grid. Kunci unik: indikator, wilayah_kode, periode. Tampilan lebar (satu kolom per indikator, hanya sel terisi): `data/gold/panel_lebar.parquet`.

| kolom | tipe | kosong | rentang_atau_nilai | asal | arti |
|---|---|---|---|---|---|
| indikator | str | 0 | fasyankes_rusak [jumlah], jembatan_rusak [jumlah], kantor_rusak [jumlah], kejadian [jumlah], kios_toko_rusak [jumlah], nilai_kerugian [jumlah], … (12 nilai) | label deret utama (src/silver/deret.py) | kode seri, atau 'kode [rincian]' untuk deret berincian |
| seri_kode | str | 0 | fasyankes_rusak, jembatan_rusak, kantor_rusak, kejadian, kios_toko_rusak, nilai_kerugian, … (12 nilai) | kode seri di sumbernya (BPS: 'var' + var.val) | identitas seri; arti lengkap di docs/seri.csv |
| rincian | str | 0 | jumlah | turvar BPS; kolom DIM_* WHO yang bervariasi | 'total' atau 'dimensi=kode;...'; lihat kamus di bawah |
| wilayah_kode | int64 | 0 | 1100 – 9700 | kamus src/wilayah.py; log K-001 | kode BPS dua digit x 100; 9999 = Indonesia |
| nama_wilayah | str | 0 | Aceh, Bali, Banten, Bengkulu, DI Yogyakarta, DKI Jakarta, … (38 nilai) | kamus src/wilayah.py | nama baku susunan 38 provinsi 2025, bukan label sumber |
| periode | str | 0 | 2010, 2011, 2012, 2013, 2014, 2015, … (16 nilai) | tahun/turtahun BPS, date WDI, DIM_TIME WHO | bentuk baku: 2019, 2019-S1, 2019-Q3, 2019-07 |
| jenis_periode | str | 0 | tahun | diturunkan dari periode | tahun, semester, triwulan, atau bulan |
| nilai | float64 | 3556 | 0 – 2.87265e+13 | datacontent BPS; value WDI; RATE_*_N WHO | angka sesuai satuan; baris tanpa angka tidak masuk Silver |
| satuan | str | 0 | kejadian, rupiah, unit | src/konfigurasi.py, bukti di docs/seri.csv | satuan baku; satu satuan per seri |
| status_sel | str | 0 | belum_ada, terisi, tidak_diterbitkan | grid Sprint 1 (reports/grid-sel-kosong.csv) | terisi, missing, tidak_diterbitkan, belum_ada, batas_lama |
| penanda | str | 5086 | outlier, patahan_seri, patahan_wilayah, perbedaan_struktural | reports/anomali.csv | kategori anomali Sprint 1 (outlier, patahan_seri, ...); nilai tidak diubah |
| rujukan_tahun | float64 | 5244 | — | var.note BPS; log | lebar jendela rujukan survei (tahun sebelum survei); kosong bila tidak berlaku |
| _berkas_raw | str | 3556 | bnpb/2026-10-20/datastore/data-bencana-indonesia/308f0499-7b3f-4733-8071-a7148bf65e50.json, bnpb/2026-10-20/datastore/data-bencana-indonesia/471f71cb-27a4-4460-836f-416c0c35b4dc.json, bnpb/2026-10-20/datastore/data-bencana-indonesia/5dfcae7e-acb3-4548-82b5-61d876ea478a.json, bnpb/2026-10-20/datastore/data-bencana-indonesia/fefc94c0-5275-4d12-899e-1d517f6c8f7c.json, bnpb/2026-10-20/datastore/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/26858365-9061-4ff7-9ccf-53480c6efb61.json, bnpb/2026-10-20/datastore/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/5f69273d-7755-4a5f-82f7-617303ba78ec.json, … (14 nilai) | jalur berkas mentah relatif data/raw/ | lineage: berkas asal baris ini |
| _sha256_raw | str | 3556 | 2e54e6c78fd3465c795c06de3236273a0de6a48f3b1cef742141776c09128b57, 3a003ae685cc2eb23ed45be7871d6960c13048d8bed12107ff48a28d30ddacc8, 5d6f131c857403cf28b2e8a5da84000017bd66dbc3a7bace8f1546370b990773, 7b953507dab9dc861030f8e1bd8feaf69cc6c7479c0efbe9643b4ac761357912, 808d9b5b2f944e4a672e580d2ecf35c656fd05d143ca9b10d6d94a98056445d8, 9d72a69ae665925ab476d3a17db37b61c66e3e2c4590258b42f576e495036554, … (14 nilai) | src.common.manifest.sha256_raw | lineage: sidik isi berkas asal, dicocokkan dengan MANIFEST.csv |

Satuan per indikator:

| indikator | satuan |
|---|---|
| fasyankes_rusak [jumlah] | unit |
| jembatan_rusak [jumlah] | unit |
| kantor_rusak [jumlah] | unit |
| kejadian [jumlah] | kejadian |
| kios_toko_rusak [jumlah] | unit |
| nilai_kerugian [jumlah] | rupiah |
| nilai_kerusakan [jumlah] | rupiah |
| pabrik_rusak [jumlah] | unit |
| rumah_ibadat_rusak [jumlah] | unit |
| rumah_rusak [jumlah] | unit |
| rumah_terendam [jumlah] | unit |
| satuan_pendidikan_rusak [jumlah] | unit |

## data/gold/nasional.parquet (28 baris)

Satu baris = satu seri × rincian × periode tingkat Indonesia. Kunci unik: seri_kode, rincian, periode.

| kolom | tipe | kosong | rentang_atau_nilai | asal | arti |
|---|---|---|---|---|---|
| seri_kode | str | 0 | EN.CLC.MDAT.ZS, fasyankes_rusak, jembatan_rusak, kantor_rusak, kejadian, rumah_ibadat_rusak, … (9 nilai) | kode seri di sumbernya (BPS: 'var' + var.val) | identitas seri; arti lengkap di docs/seri.csv |
| rincian | str | 0 | jenis_bencana=banjir, jenis_bencana=banjir;tingkat_kerusakan=berat, jenis_bencana=banjir;tingkat_kerusakan=ringan, jenis_bencana=banjir;tingkat_kerusakan=sedang, total | turvar BPS; kolom DIM_* WHO yang bervariasi | 'total' atau 'dimensi=kode;...'; lihat kamus di bawah |
| sumber | str | 0 | bnpb, wdi | nama folder sumber di data/raw/ | lembaga penerbit: bps, wdi, who_gho, ilostat, bnpb |
| periode | str | 0 | 2009, 2010, 2011, 2012, 2013, 2014, … (17 nilai) | tahun/turtahun BPS, date WDI, DIM_TIME WHO | bentuk baku: 2019, 2019-S1, 2019-Q3, 2019-07 |
| jenis_periode | str | 0 | tahun | diturunkan dari periode | tahun, semester, triwulan, atau bulan |
| nilai | float64 | 0 | 0.16059 – 243774 | datacontent BPS; value WDI; RATE_*_N WHO | angka sesuai satuan; baris tanpa angka tidak masuk Silver |
| satuan | str | 0 | kejadian, persen, unit | src/konfigurasi.py, bukti di docs/seri.csv | satuan baku; satu satuan per seri |
| batas_bawah | float64 | 28 | — | RATE_*_NL WHO | batas bawah ketidakpastian; kosong bila sumber tidak memberi |
| batas_atas | float64 | 28 | — | RATE_*_NU WHO | batas atas ketidakpastian; kosong bila sumber tidak memberi |
| rujukan_tahun | float64 | 28 | — | var.note BPS; log | lebar jendela rujukan survei (tahun sebelum survei); kosong bila tidak berlaku |
| asal | str | 0 | agregat, baris_indonesia, pembanding | src/gold/nasional_gold.py; src/gold/rekonsiliasi.py | nasional: baris_indonesia/pembanding/agregat; rekonsiliasi: keduanya/hanya_utama/hanya_pembanding |
| _berkas_raw | str | 0 | bnpb/2026-10-20/datastore/data-bencana-indonesia/27bbeb6b-6f86-4490-840a-c1bc6393102b.json, bnpb/2026-10-20/datastore/data-bencana-indonesia/471f71cb-27a4-4460-836f-416c0c35b4dc.json, bnpb/2026-10-20/tangan/kompilasi-data-kejadian-dan-dampak-bencana-2025/43b83e79-c8b6-4b9a-b2f0-d1cbd9cfa636-jumlah-rumah-rusak-akibat-bencana-menurut-provinsi-2025.xlsx, bnpb/2026-10-20/tangan/kompilasi-data-kejadian-dan-dampak-bencana-2025/6e947c9c-2404-4c02-b743-34dc5320f399-rekapitulasi-jumlah-kejadian-dan-dampak-bencana-menurut-provinsi-2025.xlsx, wdi/2026-10-20/data/kelompok-01-hal-01.json | jalur berkas mentah relatif data/raw/ | lineage: berkas asal baris ini |
| _sha256_raw | object | 2 | 023ba025e25e18040f0291a542a95447efecf1bfd39c745a3887b39f5da40cd0, 382dfc323598fa2f36da91bfb2d05227a31b81abc86146067b2de754551d37e2, 7b953507dab9dc861030f8e1bd8feaf69cc6c7479c0efbe9643b4ac761357912, 8d2fae3a96415bd41299bf08abfc356d33448bdd6b66ff2f492aca4eb0e63226 | src.common.manifest.sha256_raw | lineage: sidik isi berkas asal, dicocokkan dengan MANIFEST.csv |

## data/gold/rekonsiliasi.parquet (33 baris)

Satu baris = satu pasangan × pembanding × periode. Kunci unik: pasangan_id, seri_pembanding, rincian_pembanding, periode.

| kolom | tipe | kosong | rentang_atau_nilai | asal | arti |
|---|---|---|---|---|---|
| pasangan_id | str | 0 | P1, P2, P3 | PASANGAN di src/konfigurasi.py | id pasangan rekonsiliasi (P1, P2, ...) |
| jenis | str | 0 | konteks, selisih | PASANGAN | selisih (dihitung) atau konteks (ditampilkan berdampingan) |
| seri_utama | str | 0 | EN.CLC.MDAT.ZS, rumah_rusak | PASANGAN | seri yang direkonsiliasi (BPS/BNPB, atau seri nasional untuk pasangan antarpembanding) |
| rincian_utama | str | 0 | jenis_bencana=banjir, total | PASANGAN | rincian seri utama yang dibandingkan |
| seri_pembanding | str | 0 | rumah_rusak, rumah_rusak (agregat provinsi), rumah_rusak berat + sedang + ringan | PASANGAN | seri pembanding; kosong bila pasangan tidak punya pembanding di paket |
| rincian_pembanding | str | 0 | hitung, jenis_bencana=banjir | PASANGAN | rincian pembanding yang sebanding |
| periode | str | 0 | 2009, 2010, 2011, 2012, 2013, 2014, … (17 nilai) | tahun/turtahun BPS, date WDI, DIM_TIME WHO | bentuk baku: 2019, 2019-S1, 2019-Q3, 2019-07 |
| nilai_utama | float64 | 0 | 0.16059 – 243774 | gold_nasional.nilai | nilai seri utama pada periode itu |
| nilai_pembanding | float64 | 30 | 32664 – 243774 | gold_nasional.nilai x faktor GOLD_KONVERSI | nilai pembanding dalam satuan seri utama |
| satuan | str | 0 | persen, unit | src/konfigurasi.py, bukti di docs/seri.csv | satuan baku; satu satuan per seri |
| selisih | float64 | 30 | 0 – 0 | dihitung | nilai_utama − nilai_pembanding; kosong bila tidak dibandingkan (lihat catatan) |
| selisih_relatif | float64 | 30 | 0 – 0 | dihitung | 100 × selisih / nilai_pembanding (persen) |
| asal | str | 0 | hanya_utama, keduanya | src/gold/nasional_gold.py; src/gold/rekonsiliasi.py | nasional: baris_indonesia/pembanding/agregat; rekonsiliasi: keduanya/hanya_utama/hanya_pembanding |
| kategori | str | 0 | definisi berbeda, tanpa pasangan, tidak berselisih | PASANGAN (kategori_baku atau teks kategori) | kategori baku penjelasan selisih |
| penjelasan | str | 0 | periode dan konsep berbeda: WDI persen penduduk terdampak 1990–2009, BNPB unit rusak, seharusnya sama: dua tabel 2025 dari kompilasi yang sama, seharusnya sama: satu rumah tidak dihitung di dua provinsi (berbeda dengan kejadian) | PASANGAN kategori | alasan selisih dengan bukti dari Sprint 1 |
| catatan | str | 30 | agregat provinsi (GOLD_AGREGAT), pembanding = jumlah rumah rusak berat, sedang, ringan (rekap nasional) | dihitung | mengapa selisih tidak dihitung pada baris ini (proyeksi, konteks, satuan) |

## Contoh penelusuran satu sel Gold

| indikator | wilayah_kode | periode | nilai | _berkas_raw |
|---|---|---|---|---|
| fasyankes_rusak [jumlah] | 1100 | 2021 | 0.00 | bnpb/2026-10-20/tangan/data-bencana/0c165adc-5be2-489d-8b1a-e90c6715e73e-tabel-jumlah-kejadian-korban-dan-kerusakan-akibat-bencana-tahun-2021-per-provinsi.xlsx |

1. Sel ini berasal dari baris Silver `fasyankes_rusak` × 1100 × 2021 × rincian `jumlah` × berkas `bnpb/2026-10-20/tangan/data-bencana/0c165adc-5be2-489d-8b1a-e90c6715e73e-tabel-jumlah-kejadian-korban-dan-kerusakan-akibat-bencana-tahun-2021-per-provinsi.xlsx` (aturan *gold: sel tertelusur ke Silver*).

2. Baris Silver itu membawa `_sha256_raw` yang sama dengan `data/raw/MANIFEST.csv` (lihat penelusuran Silver di atas).
