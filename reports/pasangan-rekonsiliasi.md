# Tabel nasional dan pasangan rekonsiliasi

Dihasilkan `python pipeline.py` (`src/gold/nasional.py`) dari Silver dan `src/konfigurasi.py`. Selisih dihitung di Sprint 2; Sprint 1 memastikan setiap pasangan memang sebanding dan mencatat tahun yang beririsan.

Tabel nasional (periode x seri, rincian total, tampilan lebar): `reports/tabel-nasional.csv`. Kolom BPS hanya terisi pada tahun survei; itu bentuk datanya, tidak diisi.

## Ringkasan pasangan

| id | seri_utama | pembanding | jenis | periode_beririsan | tahun | dugaan_kategori |
|---|---|---|---|---|---|---|
| P1 | rumah_rusak | rumah_rusak [jenis_bencana=banjir] | selisih | 16 | 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025 | seharusnya sama: satu rumah tidak dihitung di dua provinsi (berbeda dengan kejadian) |
| P2 | rumah_rusak | rumah_rusak [jenis_bencana=banjir;tingkat_kerusakan=berat], rumah_rusak [jenis_bencana=banjir;tingkat_kerusakan=sedang], rumah_rusak [jenis_bencana=banjir;tingkat_kerusakan=ringan] | selisih | 1 | 2025 | seharusnya sama: dua tabel 2025 dari kompilasi yang sama |
| P3 | EN.CLC.MDAT.ZS | rumah_rusak [jenis_bencana=banjir] | konteks | 0 | — | periode dan konsep berbeda: WDI persen penduduk terdampak 1990–2009, BNPB unit rusak |

## Rincian per pasangan

### P1: Rumah rusak banjir: baris INDONESIA vs jumlah 38 provinsi
- Seri utama: `rumah_rusak` (rincian `jenis_bencana=banjir`)
- Pembanding: `rumah_rusak` (rincian `jenis_bencana=banjir`)
- Jenis: **selisih**; tahun beririsan: 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025
- Dugaan kategori selisih (diuji di Sprint 2): seharusnya sama: satu rumah tidak dihitung di dua provinsi (berbeda dengan kejadian)

Pertanyaan keterbandingan dan jawabannya:

1. **Bolehkah berbeda?** Untuk kejadian boleh (kejadian lintas provinsi dihitung sekali secara nasional); untuk rumah rusak tidak, karena setiap rumah berada di satu provinsi.
2. **Dari berkas mana?** Tabel per jenis 2024 dan 2025 (baris provinsi dan INDONESIA) dan tabel nasional 2010–2024.

### P2: Rumah rusak 2025: tabel per jenis vs rekap nasional (berat + sedang + ringan)
- Seri utama: `rumah_rusak` (rincian `jenis_bencana=banjir`)
- Pembanding: `rumah_rusak` (rincian `jenis_bencana=banjir;tingkat_kerusakan=berat`), `rumah_rusak` (rincian `jenis_bencana=banjir;tingkat_kerusakan=sedang`), `rumah_rusak` (rincian `jenis_bencana=banjir;tingkat_kerusakan=ringan`)
- Jenis: **selisih**; tahun beririsan: 2025
- Dugaan kategori selisih (diuji di Sprint 2): seharusnya sama: dua tabel 2025 dari kompilasi yang sama

Pertanyaan keterbandingan dan jawabannya:

1. **Apakah tingkat kerusakan membagi habis?** Ya: rekap hanya punya tiga kolom rumah rusak (berat, sedang, ringan).
2. **Mengapa 2025 saja?** Rekap nasional per tingkat hanya ada untuk 2025.

### P3: Penduduk terdampak kekeringan, banjir, suhu ekstrem (WDI): konteks
- Seri utama: `EN.CLC.MDAT.ZS` (rincian `total`)
- Pembanding: `rumah_rusak` (rincian `jenis_bencana=banjir`)
- Jenis: **konteks**; tahun beririsan: —
- Dugaan kategori selisih (diuji di Sprint 2): periode dan konsep berbeda: WDI persen penduduk terdampak 1990–2009, BNPB unit rusak

Pertanyaan keterbandingan dan jawabannya:

1. **Mengapa tidak dihitung selisihnya?** Konsep berbeda (penduduk vs rumah) dan tidak ada tahun yang sama.
