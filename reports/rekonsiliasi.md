# Tabel rekonsiliasi seri utama vs pembanding nasional

Dihasilkan `python pipeline.py` (`src/gold/rekonsiliasi.py`) dari `data/gold/nasional.parquet`. Selisih = nilai utama − nilai pembanding; selisih relatif dalam persen terhadap pembanding. Periode tanpa pasangan tetap ditampilkan. Selisih tidak dihapus dan tidak dipaksa sama.

## Ringkasan per pasangan

| pasangan_id | seri_pembanding | jenis | periode | berpasangan | selisih_dihitung | median_selisih | median_selisih_relatif | kategori |
|---|---|---|---|---|---|---|---|---|
| P1 | rumah_rusak (agregat provinsi) | selisih | 16 | 2 | 2 | 0.00 | 0.00 | tanpa pasangan (14), tidak berselisih (2) |
| P2 | rumah_rusak berat + sedang + ringan | selisih | 16 | 1 | 1 | 0.00 | 0.00 | tanpa pasangan (15), tidak berselisih (1) |
| P3 | rumah_rusak | konteks | 1 | 0 | 0 |  |  | definisi berbeda (1) |

Median selisih relatif mutlak, pasangan yang seri utamanya seri provinsi (BPS/BNPB): 0.00% (3 baris); semua pasangan termasuk antarpembanding: 0.00% (3 baris).

Periode pembanding di luar rentang seri utama yang tidak ditulis: P3 16.

## Kategori

Kategori baku: *definisi berbeda*, *metode berbeda*, *vintage berbeda*, *cakupan berbeda*, *belum terjelaskan*, *tanpa pasangan*, *tidak berselisih*. Kategori pasangan ditetapkan dari bukti di pasangan rekonsiliasi Sprint 1 (`reports/pasangan-rekonsiliasi.md`); baris satu sisi menjadi *tanpa pasangan*, baris yang angkanya sama menjadi *tidak berselisih*.

## Rincian per pasangan

### P1: Rumah rusak banjir: baris INDONESIA vs jumlah 38 provinsi

Jenis **selisih**; kategori pasangan: **belum terjelaskan**. Seharusnya sama: satu rumah tidak dihitung di dua provinsi (berbeda dengan kejadian).

Rincian: baris INDONESIA di tabel per jenis dibandingkan dengan jumlah baris provinsi di berkas yang sama.

| seri_pembanding | periode | nilai_utama | nilai_pembanding | selisih | selisih_relatif | asal | kategori | catatan |
|---|---|---|---|---|---|---|---|---|
| rumah_rusak (agregat provinsi) | 2010 | 24,894.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak (agregat provinsi) | 2011 | 40,877.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak (agregat provinsi) | 2012 | 16,357.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak (agregat provinsi) | 2013 | 39,803.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak (agregat provinsi) | 2014 | 7,725.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak (agregat provinsi) | 2015 | 3,802.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak (agregat provinsi) | 2016 | 14,872.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak (agregat provinsi) | 2017 | 16,328.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak (agregat provinsi) | 2018 | 7,537.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak (agregat provinsi) | 2019 | 16,389.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak (agregat provinsi) | 2020 | 39,199.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak (agregat provinsi) | 2021 | 94,667.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak (agregat provinsi) | 2022 | 10,342.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak (agregat provinsi) | 2023 | 18,244.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak (agregat provinsi) | 2024 | 32,664.00 | 32,664.00 | 0.00 | 0.00 | keduanya | tidak berselisih | agregat provinsi (GOLD_AGREGAT) |
| rumah_rusak (agregat provinsi) | 2025 | 243,774.00 | 243,774.00 | 0.00 | 0.00 | keduanya | tidak berselisih | agregat provinsi (GOLD_AGREGAT) |

### P2: Rumah rusak 2025: tabel per jenis vs rekap nasional (berat + sedang + ringan)

Jenis **selisih**; kategori pasangan: **belum terjelaskan**. Seharusnya sama: dua tabel 2025 dari kompilasi yang sama.

Rincian: banjir: jenis dengan rumah rusak terbanyak; rekap nasional memecah per tingkat, tabel per jenis tidak.

| seri_pembanding | periode | nilai_utama | nilai_pembanding | selisih | selisih_relatif | asal | kategori | catatan |
|---|---|---|---|---|---|---|---|---|
| rumah_rusak berat + sedang + ringan | 2010 | 24,894.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak berat + sedang + ringan | 2011 | 40,877.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak berat + sedang + ringan | 2012 | 16,357.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak berat + sedang + ringan | 2013 | 39,803.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak berat + sedang + ringan | 2014 | 7,725.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak berat + sedang + ringan | 2015 | 3,802.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak berat + sedang + ringan | 2016 | 14,872.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak berat + sedang + ringan | 2017 | 16,328.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak berat + sedang + ringan | 2018 | 7,537.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak berat + sedang + ringan | 2019 | 16,389.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak berat + sedang + ringan | 2020 | 39,199.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak berat + sedang + ringan | 2021 | 94,667.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak berat + sedang + ringan | 2022 | 10,342.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak berat + sedang + ringan | 2023 | 18,244.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak berat + sedang + ringan | 2024 | 32,664.00 |  |  |  | hanya_utama | tanpa pasangan |  |
| rumah_rusak berat + sedang + ringan | 2025 | 243,774.00 | 243,774.00 | 0.00 | 0.00 | keduanya | tidak berselisih | pembanding = jumlah rumah rusak berat, sedang, ringan (rekap nasional) |

### P3: Penduduk terdampak kekeringan, banjir, suhu ekstrem (WDI): konteks

Jenis **konteks**; kategori pasangan: **definisi berbeda**. Periode dan konsep berbeda: WDI persen penduduk terdampak 1990–2009, BNPB unit rusak.

Rincian: WDI tanpa rincian; BNPB banjir sebagai contoh jenis yang tercakup.

| seri_pembanding | periode | nilai_utama | nilai_pembanding | selisih | selisih_relatif | asal | kategori | catatan |
|---|---|---|---|---|---|---|---|---|
| rumah_rusak | 2009 | 0.16 |  |  |  | hanya_utama | definisi berbeda |  |
