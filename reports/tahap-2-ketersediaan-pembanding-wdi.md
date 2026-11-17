# Tahap 2 — Ketersediaan seri pembanding WDI

## `EN.CLC.MDAT.ZS`

- **Nama:** Droughts, floods, extreme temperatures (% of population, average 1990-2009)
- **Periode yang dimaksud indikator:** 1990–2009 (rata-rata periode), bukan deret nilai tahunan.
- **Observasi Indonesia non-null:** 2009 (nilai 0.16059). Snapshot memuat 66 baris tahun API 1960–2025, tetapi hanya 1 nilai non-null.
- **Satuan:** % populasi menurut nama indikator; kolom `unit` API kosong.
- **Rincian tersedia:** Indonesia/agregat nasional. Tidak ada pemisahan provinsi, jenis kelamin, umur, atau kelompok urban/rural. Indikator menggabungkan dampak kekeringan, banjir, dan suhu ekstrem.

Metadata menjelaskan penduduk terdampak sebagai penduduk yang terluka, kehilangan tempat tinggal, atau membutuhkan bantuan segera. Persentase adalah rata-rata untuk periode yang tercantum, dihitung dari jumlah terdampak dibagi jumlah populasi tahunan selama periode tersebut.

## Ketersediaan dan keterbandingan dengan seri utama

| Seri utama | Periode seri utama | Rincian seri utama | Satuan | Periode WDI | Tahun beririsan | Rincian WDI kandidat | Status dan alasan |
|---|---|---|---|---|---|---|---|
| `kejadian` | 2010-2025 | Provinsi; jumlah kejadian, tersedia rincian jenis bencana | kejadian | 1990-2009 (rata-rata) | Tidak ada | Total Indonesia; tidak terdisagregasi | Konteks saja; tidak sebanding langsung. Tidak ada irisan periode; WDI mengukur persentase penduduk terdampak, sedangkan seri BNPB mengukur kejadian pada rincian provinsi. |
| `rumah_rusak` | 2010-2025 | Provinsi; tingkat kerusakan dan jenis bencana | unit | 1990-2009 (rata-rata) | Tidak ada | Total Indonesia; tidak terdisagregasi | Konteks saja; tidak sebanding langsung. Tidak ada irisan periode; WDI mengukur persentase penduduk terdampak, sedangkan seri BNPB mengukur unit pada rincian provinsi. |
| `rumah_terendam` | 2021-2022 | Provinsi; jumlah rumah terendam | unit | 1990-2009 (rata-rata) | Tidak ada | Total Indonesia; tidak terdisagregasi | Konteks saja; tidak sebanding langsung. Tidak ada irisan periode; WDI mengukur persentase penduduk terdampak, sedangkan seri BNPB mengukur unit pada rincian provinsi. |
| `fasyankes_rusak` | 2010-2025 | Provinsi; fasilitas kesehatan rusak | unit | 1990-2009 (rata-rata) | Tidak ada | Total Indonesia; tidak terdisagregasi | Konteks saja; tidak sebanding langsung. Tidak ada irisan periode; WDI mengukur persentase penduduk terdampak, sedangkan seri BNPB mengukur unit pada rincian provinsi. |
| `satuan_pendidikan_rusak` | 2021-2025 | Provinsi; satuan pendidikan rusak | unit | 1990-2009 (rata-rata) | Tidak ada | Total Indonesia; tidak terdisagregasi | Konteks saja; tidak sebanding langsung. Tidak ada irisan periode; WDI mengukur persentase penduduk terdampak, sedangkan seri BNPB mengukur unit pada rincian provinsi. |
| `jembatan_rusak` | 2010-2025 | Provinsi; jembatan rusak | unit | 1990-2009 (rata-rata) | Tidak ada | Total Indonesia; tidak terdisagregasi | Konteks saja; tidak sebanding langsung. Tidak ada irisan periode; WDI mengukur persentase penduduk terdampak, sedangkan seri BNPB mengukur unit pada rincian provinsi. |
| `kantor_rusak` | 2010-2025 | Provinsi; kantor rusak | unit | 1990-2009 (rata-rata) | Tidak ada | Total Indonesia; tidak terdisagregasi | Konteks saja; tidak sebanding langsung. Tidak ada irisan periode; WDI mengukur persentase penduduk terdampak, sedangkan seri BNPB mengukur unit pada rincian provinsi. |
| `rumah_ibadat_rusak` | 2010-2025 | Provinsi; rumah ibadat rusak | unit | 1990-2009 (rata-rata) | Tidak ada | Total Indonesia; tidak terdisagregasi | Konteks saja; tidak sebanding langsung. Tidak ada irisan periode; WDI mengukur persentase penduduk terdampak, sedangkan seri BNPB mengukur unit pada rincian provinsi. |
| `kios_toko_rusak` | 2010-2024 | Provinsi; kios/toko rusak | unit | 1990-2009 (rata-rata) | Tidak ada | Total Indonesia; tidak terdisagregasi | Konteks saja; tidak sebanding langsung. Tidak ada irisan periode; WDI mengukur persentase penduduk terdampak, sedangkan seri BNPB mengukur unit pada rincian provinsi. |
| `pabrik_rusak` | 2024-2024 | Provinsi; pabrik rusak | unit | 1990-2009 (rata-rata) | Tidak ada | Total Indonesia; tidak terdisagregasi | Konteks saja; tidak sebanding langsung. Tidak ada irisan periode; WDI mengukur persentase penduduk terdampak, sedangkan seri BNPB mengukur unit pada rincian provinsi. |
| `luas_sawah_rusak` | 2010-2024 | Provinsi pada definisi seri; hektare rusak | hektar | 1990-2009 (rata-rata) | Tidak ada | Total Indonesia; tidak terdisagregasi | Konteks saja; tidak sebanding langsung. Tidak ada irisan periode; WDI mengukur persentase penduduk terdampak, sedangkan seri BNPB mengukur hektar pada rincian provinsi. |
| `luas_lahan_kebun_hutan_rusak` | 2010-2024 | Provinsi pada definisi seri; hektare rusak | hektar | 1990-2009 (rata-rata) | Tidak ada | Total Indonesia; tidak terdisagregasi | Konteks saja; tidak sebanding langsung. Tidak ada irisan periode; WDI mengukur persentase penduduk terdampak, sedangkan seri BNPB mengukur hektar pada rincian provinsi. |
| `nilai_kerugian` | 2015-2024 | Provinsi; nilai kerugian | rupiah | 1990-2009 (rata-rata) | Tidak ada | Total Indonesia; tidak terdisagregasi | Konteks saja; tidak sebanding langsung. Tidak ada irisan periode; WDI mengukur persentase penduduk terdampak, sedangkan seri BNPB mengukur rupiah pada rincian provinsi. |
| `nilai_kerusakan` | 2015-2024 | Provinsi; nilai kerusakan | rupiah | 1990-2009 (rata-rata) | Tidak ada | Total Indonesia; tidak terdisagregasi | Konteks saja; tidak sebanding langsung. Tidak ada irisan periode; WDI mengukur persentase penduduk terdampak, sedangkan seri BNPB mengukur rupiah pada rincian provinsi. |

Untuk semua seri utama, irisan tahun adalah **tidak ada**: periode BNPB dimulai pada 2010 atau sesudahnya, sedangkan indikator WDI merangkum 1990–2009. Label API `2009` menandai satu nilai ringkasan itu dan tidak menjadikannya pengamatan tahunan 2009 yang sebanding.

## Rekomendasi untuk Tahap 6

Rincian WDI yang tersedia hanya **total nasional Indonesia**. Rincian ini dapat dipertahankan sebagai konteks, tetapi tidak ada rincian yang sebanding untuk rekonsiliasi numerik dengan 14 seri utama: konsep, satuan/granularitas, dan periode tidak cocok. Jangan menghitung selisih atau menggabungkannya ke panel provinsi.

Tabel terstruktur: [`ketersediaan-wdi-en-clc-mdat-zs.csv`](ketersediaan-wdi-en-clc-mdat-zs.csv) dan [`irisan-wdi-seri-utama.csv`](irisan-wdi-seri-utama.csv).

## Sumber

Data observasi WDI `kelompok-01-hal-01.json`; metadata indikator dari `sumber2_indikator.json` dan `sumber46_indikator.json` pada snapshot 2026-10-20. Kedua metadata menyajikan definisi indikator yang sama.
