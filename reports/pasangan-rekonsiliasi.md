# Tabel nasional dan pasangan rekonsiliasi

Dihasilkan `python pipeline.py` (`src/gold/nasional.py`) dari Silver dan `src/konfigurasi.py`. Perbandingan numerik hanya dilakukan pada tahun dan cakupan wilayah yang lengkap; nilai sumber dan selisih dipertahankan di `reports/hasil-rekonsiliasi.csv`.

Tabel nasional (periode x seri, rincian total, tampilan lebar): `reports/tabel-nasional.csv`. Kolom BPS hanya terisi pada tahun survei; itu bentuk datanya, tidak diisi.

## Ringkasan numerik

| id | periode | nilai_utama | nilai_pembanding | selisih_pembanding_minus_utama | status |
|---|---|---|---|---|---|
| P1 | 2024 | 32,664.00 | 32,664.00 | 0.00 | cocok |
| P1 | 2025 | 243,774.00 | 243,774.00 | 0.00 | cocok |
| P2 | 2025 | 243,774.00 | 243,774.00 | 0.00 | cocok |

## Ringkasan pasangan

| id | seri_utama | pembanding | jenis | periode_beririsan | tahun | dugaan_kategori |
|---|---|---|---|---|---|---|
| P1 | rumah_rusak | rumah_rusak [jenis_bencana=banjir] | selisih | 2 | 2024, 2025 | seharusnya sama: satu rumah tidak dihitung di dua provinsi (berbeda dengan kejadian) |
| P2 | rumah_rusak | rumah_rusak [jenis_bencana=banjir;tingkat_kerusakan=berat], rumah_rusak [jenis_bencana=banjir;tingkat_kerusakan=sedang], rumah_rusak [jenis_bencana=banjir;tingkat_kerusakan=ringan] | selisih | 1 | 2025 | seharusnya sama: dua tabel 2025 dari kompilasi yang sama |
| P3 | EN.CLC.MDAT.ZS | rumah_rusak [jenis_bencana=banjir] | konteks | 0 | — | periode dan konsep berbeda: WDI persen penduduk terdampak 1990–2009, BNPB unit rusak |

## Rincian per pasangan

### P1: Rumah rusak banjir: baris INDONESIA vs jumlah 38 provinsi
- Seri utama: `rumah_rusak` (rincian `jenis_bencana=banjir`)
- Pembanding: `rumah_rusak` (rincian `jenis_bencana=banjir`)
- Jenis: **selisih**; tahun yang dapat dibandingkan: 2024, 2025
- Kategori selisih: seharusnya sama: satu rumah tidak dihitung di dua provinsi (berbeda dengan kejadian)

Hasil rekonsiliasi numerik (selisih = pembanding − utama):
| periode | nilai_utama | nilai_pembanding | selisih_pembanding_minus_utama | persen_selisih_terhadap_utama | jumlah_provinsi | status |
|---|---|---|---|---|---|---|
| 2024 | 32,664.00 | 32,664.00 | 0.00 | 0.00 | 38.00 | cocok |
| 2025 | 243,774.00 | 243,774.00 | 0.00 | 0.00 | 38.00 | cocok |

Pertanyaan keterbandingan dan jawabannya:

1. **Bolehkah berbeda?** Untuk kejadian boleh (kejadian lintas provinsi dihitung sekali secara nasional); untuk rumah rusak tidak, karena setiap rumah berada di satu provinsi.
2. **Dari berkas mana?** Berkas tabel per jenis 2024 dan 2025 yang masing-masing memuat 38 provinsi dan baris INDONESIA.

### P2: Rumah rusak 2025: tabel per jenis vs rekap nasional (berat + sedang + ringan)
- Seri utama: `rumah_rusak` (rincian `jenis_bencana=banjir`)
- Pembanding: `rumah_rusak` (rincian `jenis_bencana=banjir;tingkat_kerusakan=berat`), `rumah_rusak` (rincian `jenis_bencana=banjir;tingkat_kerusakan=sedang`), `rumah_rusak` (rincian `jenis_bencana=banjir;tingkat_kerusakan=ringan`)
- Jenis: **selisih**; tahun yang dapat dibandingkan: 2025
- Kategori selisih: seharusnya sama: dua tabel 2025 dari kompilasi yang sama

Hasil rekonsiliasi numerik (selisih = pembanding − utama):
| periode | nilai_utama | nilai_pembanding | selisih_pembanding_minus_utama | persen_selisih_terhadap_utama | jumlah_provinsi | status |
|---|---|---|---|---|---|---|
| 2025 | 243,774.00 | 243,774.00 | 0.00 | 0.00 |  | cocok |

Pertanyaan keterbandingan dan jawabannya:

1. **Apakah tingkat kerusakan membagi habis?** Ya: rekap hanya punya tiga kolom rumah rusak (berat, sedang, ringan).
2. **Mengapa 2025 saja?** Rekap nasional per tingkat hanya ada untuk 2025.

### P3: Penduduk terdampak kekeringan, banjir, suhu ekstrem (WDI): konteks
- Seri utama: `EN.CLC.MDAT.ZS` (rincian `total`)
- Pembanding: `rumah_rusak` (rincian `jenis_bencana=banjir`)
- Jenis: **konteks**; tahun yang dapat dibandingkan: —
- Kategori selisih: periode dan konsep berbeda: WDI persen penduduk terdampak 1990–2009, BNPB unit rusak

Nilai WDI dipertahankan sebagai konteks, bukan dikurangkan: satu angka rata-rata 1990–2009 yang ditulis sebagai date 2009; mengukur penduduk terdampak, bukan kerusakan.
| periode | nilai | satuan | _berkas_raw |
|---|---|---|---|
| 2009 | 0.160589721908345 | persen | wdi/2026-10-20/data/kelompok-01-hal-01.json |

Pertanyaan keterbandingan dan jawabannya:

1. **Mengapa tidak dihitung selisihnya?** Konsep berbeda (penduduk vs rumah) dan tidak ada tahun yang sama.
