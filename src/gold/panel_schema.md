Rancangan Struktur Panel Gold

Capstone Data Wrangling Kelompok 23

1. Tujuan

Menyusun rancangan struktur data panel bencana Indonesia berdasarkan 38 provinsi dan periode pengamatan.

2. Unit Observasi

Satu baris merepresentasikan satu provinsi pada satu periode pengamatan.

3. Dimensi Panel

* Wilayah: 38 provinsi Indonesia.
* Periode: Tahun pengamatan sesuai ketersediaan sumber data.
* Identitas wilayah: Kode wilayah provinsi.
* Identitas waktu: Tahun.

4. Seri Bencana

Seri yang direncanakan:

1. Banjir
2. Cuaca ekstrem
3. Erupsi gunung api
4. Gelombang pasang dan abrasi
5. Gempa bumi
6. Kebakaran hutan dan lahan
7. Kekeringan
8. Tanah longsor
9. Tsunami

5. Rancangan Kolom Panel

Kolom	Keterangan
kode_provinsi	Kode unik provinsi
provinsi	Nama provinsi
tahun	Periode pengamatan
banjir	Jumlah kejadian banjir
cuaca_ekstrem	Jumlah kejadian cuaca ekstrem
erupsi_gunung_api	Jumlah kejadian erupsi
gelombang_pasang_abrasi	Jumlah kejadian
gempa_bumi	Jumlah kejadian gempa
kebakaran_hutan_lahan	Jumlah kejadian
kekeringan	Jumlah kejadian kekeringan
tanah_longsor	Jumlah kejadian tanah longsor
tsunami	Jumlah kejadian tsunami

6. Aturan Transformasi

1. Menggunakan kode provinsi sebagai identitas wilayah.
2. Menyeragamkan nama provinsi.
3. Memastikan satu observasi untuk setiap kombinasi provinsi dan tahun.
4. Mengeluarkan baris agregat nasional dari panel provinsi.
5. Tidak mencampurkan data kabupaten/kota dengan data provinsi tanpa agregasi yang tervalidasi.
6. Membedakan nilai nol dengan data yang tidak tersedia.
7. Mempertahankan sumber dan satuan setiap seri.

7. Sumber Data Awal

* Data jumlah kejadian bencana menurut provinsi tahun 2025.
* Data jumlah rumah rusak akibat bencana tahun 2025.
* Data kejadian dan dampak bencana tahun 2024.
* Data pendukung lainnya sesuai hasil pemeriksaan dataset.

8. Catatan Validasi

Struktur ini masih berupa rancangan awal. Ketersediaan periode, kesesuaian definisi seri, dan konsistensi antarfile harus diperiksa sebelum pembentukan panel final.

9. Penanggung Jawab

Nabila Nur Azizah
NIM: 124450048
Komponen: Transformasi dan Panel (Koordinator)