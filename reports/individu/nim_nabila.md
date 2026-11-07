Laporan Individu

Sprint 0 – Transformasi dan Panel

Nama: Nabila Nur Azizah
NIM: 124450048
Peran: Koordinator Transformasi dan Panel

1. Pekerjaan yang Dilakukan

* Berhasil mengunduh 58 berkas data kasus 23.
* Memeriksa struktur dataset bencana tahun 2024 dan 2025.
* Mengidentifikasi struktur data jumlah kejadian bencana menurut provinsi.
* Memeriksa struktur sheet dan dimensi beberapa file Excel.
* Menyiapkan draft struktur panel Gold untuk 38 provinsi dan periode pengamatan.

2. Output

* src/gold/panel_schema.md
* Draft rancangan struktur panel provinsi dan seri bencana.

3. Temuan

Data memiliki beberapa format dan tingkat agregasi, termasuk provinsi dan kabupaten/kota. Diperlukan validasi sebelum penggabungan menjadi panel.

4. Kendala

Tahap ekstraksi pipeline belum diimplementasikan sehingga pipeline masih menghasilkan NotImplementedError.

5. Rencana Berikutnya

* Memvalidasi kesesuaian data antarperiode.
* Menyusun aturan transformasi.
* Menyiapkan struktur tabel panel Gold.
* Melakukan koordinasi dengan anggota tim.