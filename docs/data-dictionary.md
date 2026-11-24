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
