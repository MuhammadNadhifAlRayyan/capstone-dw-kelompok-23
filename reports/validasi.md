# Hasil validasi Silver

Dihasilkan `python pipeline.py` (`src/validasi/`). Aturan keras menghentikan pipeline bila gagal; peringatan dilaporkan untuk diperiksa manusia. Aturan juga diuji dengan baris yang sengaja dirusak (`pytest`, berkas `tests/test_validasi.py`).

| aturan | jenis | keterangan | hasil |
|---|---|---|---|
| kolom dan tipe | keras (umum) | setiap kolom ada dengan tipe yang benar; nilai tidak kosong | LOLOS |
| rincian_dari_kamus | keras (umum) | rincian 'total' atau 'dimensi=kode' dengan dimensi/kode dari kamus konfigurasi | LOLOS |
| satu_satuan_per_seri | keras (umum) | satu seri hanya punya satu satuan | LOLOS |
| nilai_dalam_rentang_satuan | keras (umum) | nilai berada di rentang sah satuannya (persen 0–100, per 1.000 0–1.000, ...) | LOLOS |
| batas_bawah_le_nilai_le_batas_atas | keras (umum) | untuk baris yang punya batas: batas bawah ≤ nilai ≤ batas atas | LOLOS |
| kunci unik | keras (umum) | kombinasi sumber + seri_kode + wilayah_kode + periode + rincian + _berkas_raw tidak kembar | LOLOS |
| wilayah dan periode | keras (umum) | wilayah_kode dari kamus 38 provinsi + 9999; periode berbentuk baku | LOLOS |
| cacah_bilangan_bulat | keras (kasus) | kejadian dan unit rusak bilangan bulat | LOLOS |
| jenis_menjumlah_ke_total | keras (kasus) | jumlah per jenis = baris Total di berkas yang sama | LOLOS |
| rumah_rusak_tingkat_sama_tabel_jenis | keras (kasus) | 2025: berat + sedang + ringan = rumah rusak per jenis | LOLOS |
| kejadian_kabkota_tidak_kurang | peringatan (kasus) | kejadian jumlah kab/kota < provinsi (peringatan) | PERINGATAN (1 baris) |
| kerusakan_kabkota_sama_provinsi | peringatan (kasus) | unit rusak jumlah kab/kota ≠ provinsi (peringatan) | PERINGATAN (2 baris) |
| indonesia_sama_lintas_berkas | peringatan (kasus) | baris Indonesia berbeda antarberkas (peringatan) | PERINGATAN (1 baris) |
| nilai_rekap_sama_tabel_tahunan | peringatan (kasus) | nilai rekap 2015–2024 ≠ tabel per tahun (peringatan) | PERINGATAN (4 baris) |

## Kegagalan aturan umum

Tidak ada.

## Baris yang memicu aturan kasus

### kejadian_kabkota_tidak_kurang

| seri_kode | wilayah_kode | periode | rincian | nilai_kabkota | nilai_provinsi | selisih | _berkas_raw_kabkota | _berkas_raw_provinsi |
|---|---|---|---|---|---|---|---|---|
| kejadian | 3100 | 2024 | jenis_bencana=tanah_longsor | 0.00 | 1.00 | -1.00 | bnpb/2026-10-20/datastore/data-bencana-indonesia/a4daec53-1119-43ef-b05e-00ec3a4c42a4.json | bnpb/2026-10-20/datastore/data-bencana-indonesia/faeb2406-b800-4b8e-9e09-37d4b2aa5879.json |

### kerusakan_kabkota_sama_provinsi

| seri_kode | wilayah_kode | periode | rincian | nilai_kabkota | nilai_provinsi | selisih | _berkas_raw_kabkota | _berkas_raw_provinsi |
|---|---|---|---|---|---|---|---|---|
| rumah_rusak | 3100 | 2024 | jenis_bencana=tanah_longsor | 0.00 | 50.00 | -50.00 | bnpb/2026-10-20/datastore/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/5c9f7ea9-f809-487c-b1f8-f05a6f3291b3.json | bnpb/2026-10-20/datastore/data-bencana-indonesia/471f71cb-27a4-4460-836f-416c0c35b4dc.json |
| rumah_rusak | 3200 | 2024 | jenis_bencana=tanah_longsor | 4,662.00 | 4,612.00 | 50.00 | bnpb/2026-10-20/datastore/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/5c9f7ea9-f809-487c-b1f8-f05a6f3291b3.json | bnpb/2026-10-20/datastore/data-bencana-indonesia/471f71cb-27a4-4460-836f-416c0c35b4dc.json |

### indonesia_sama_lintas_berkas

| seri_kode | wilayah_kode | periode | rincian | nunique | min | max | size |
|---|---|---|---|---|---|---|---|
| kejadian | 9999 | 2024 | jenis_bencana=tanah_longsor | 2 | 27.00 | 207.00 | 3 |

### nilai_rekap_sama_tabel_tahunan

| seri_kode | wilayah_kode | periode | rincian | nilai_rekap | nilai_tahunan | _berkas_raw_tahunan |
|---|---|---|---|---|---|---|
| nilai_kerugian | 1600 | 2017 | total | 20,090,800,000.00 | 48,016,600,000.00 | bnpb/2026-10-20/datastore/data-bencana-indonesia/e2c2ed75-c2c4-4f3b-90e3-3565b516c3f0.json |
| nilai_kerugian | 7200 | 2017 | total | 19,903,020,000.00 | 23,871,573,000.00 | bnpb/2026-10-20/datastore/data-bencana-indonesia/e2c2ed75-c2c4-4f3b-90e3-3565b516c3f0.json |
| nilai_kerusakan | 1600 | 2017 | total | 40,380,000,000.00 | 80,760,000,000.00 | bnpb/2026-10-20/datastore/data-bencana-indonesia/e2c2ed75-c2c4-4f3b-90e3-3565b516c3f0.json |
| nilai_kerusakan | 7200 | 2017 | total | 215,219,850,000.00 | 400,717,483,157.00 | bnpb/2026-10-20/datastore/data-bencana-indonesia/e2c2ed75-c2c4-4f3b-90e3-3565b516c3f0.json |
