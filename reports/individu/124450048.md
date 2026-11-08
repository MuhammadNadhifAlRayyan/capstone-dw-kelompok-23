# Laporan Perorangan — Nabila Nur Azizah (124450048), Komponen Transformasi dan Panel

**Kasus 23: Kerusakan dan Kerugian Akibat Bencana (Klaster G. Bencana BNPB; SDG 1, 11)**  
**Peran:** Koordinator Tim & Pemilik Komponen Transformasi dan Panel (Tahap 4)  
**Sprint:** Sprint 0 (Inisialisasi Lingkungan, Kontrak Tim, Verifikasi Berkas, dan Skema Panel Gold)

---

## 1. Komponen Saya
Saya memegang komponen **Transformasi dan Panel (Tahap 4)** sekaligus berperan sebagai **Koordinator Tim Kelompok 23**. Komponen ini bertanggung jawab merancang dan mengawal struktur data dari tabel panjang berstandar Silver menjadi tabel panel lebar Gold ($38 \text{ provinsi} \times \text{periode } 2010\text{–}2025 \times \text{indikator}$) yang siap dianalisis dan dimuat ke basis data SQL, serta memastikan koordinasi antar-anggota berjalan lancar untuk memenuhi kontrak tim dan jadwal sprint.

---

## 2. Keputusan Wrangling
Keputusan utama yang menjadi fondasi komponen ini pada Sprint 0 merujuk pada **K-001** di `log-keputusan.csv`:
- **Aturan Pemetaan Wilayah ke 38 Provinsi 2025:** Semua observasi wilayah dipetakan ke format kode BPS dua digit dikali 100 (`1100` Aceh hingga `9700` Papua Pegunungan), serta kode `9999` khusus untuk Indonesia (agregat nasional). Provinsi induk dibiarkan apa adanya, sehingga provinsi pemekaran baru (Kalimantan Utara sejak 2012; Papua Barat Daya, Papua Selatan, Papua Tengah, dan Papua Pegunungan sejak 2022) hanya memiliki observasi pada tahun sejak resmi terbentuk. Penggabungan antarberkas dilakukan berbasis kode numerik, bukan nama wilayah.
- **Alternatif yang Ditolak:** Menggabungkan paksa provinsi baru ke provinsi induk dengan pembobotan proporsi populasi historis.
- **Alasan:** Menjaga keaslian angka sumber data mentah tanpa manipulasi model pembobotan tambahan, menghindari inkonsistensi ejaan nama daerah antarsumber, serta menjamin kejelasan lineage data mentah ke Silver dan Gold (mengacu pada Langkah Kerja Bagian 5.1).
- **Keputusan Skala Moneter:** Untuk seri `nilai_kerugian` dan `nilai_kerusakan` yang bersatuan Rupiah dengan rentang nilai ekstrem (dari puluhan juta hingga ratusan triliun), disiapkan transformasi $\log(1 + x)$ (`np.log1p`) pada panel Gold tanpa menjumlahkan kedua nilai tersebut karena keduanya merupakan konsep ekonomi yang berbeda (kehilangan arus ekonomi vs kerusakan aset modal fisik).

---

## 3. Kegagalan dan Pelajaran
Pada tahap eksplorasi awal struktur berkas JSON CKAN Datastore dan tabel rekapitulasi XLSX BNPB (misalnya berkas kompilasi dampak 2024 dan 2025), ditemukan bahwa baris total `INDONESIA` tercampur dalam tabel provinsi dengan kolom `Kode Wilayah Provinsi` bernilai kosong (`None`). Apabila proses pembentukan panel dan agregasi dilakukan secara langsung tanpa pemilahan, baris nasional ini akan memicu duplikasi ganda (agregasi provinsi menjumlahkan angka nasional kembali) dan merusak integritas matriks wilayah. Pelajaran penting yang diperoleh adalah keharusan menyusun modul filter eksplisit (`pisahkan_nasional()`) di dalam `src/gold/panel.py` sejak perancangan kerangka awal agar agregat nasional tersimpan di tabel terpisah (`gold_nasional.parquet`) dan siap digunakan pada tahap rekonsiliasi.

---

## 4. Bukti
Pemeriksaan integritas berkas mentah dan pembentukan kerangka panel telah diuji dan menghasilkan angka yang dapat direproduksi:

| Ukuran / Indikator | Sebelum Sprint 0 | Sesudah Sprint 0 | Perintah Reproduksi |
|---|---|---|---|
| Berkas raw lolos sha256 | 0 berkas | 58 berkas cocok (0 salah) | `python -c "from src.common.manifest import periksa; print(periksa())"` |
| Verifikasi pipeline awal | Gagal (belum unduh) | Lolos verifikasi MANIFEST | `python pipeline.py` |
| Grid observasi panel master | Belum ada | 608 baris ($38 \times 16$ tahun) | `python -c "from src.gold.panel import buat_grid_provinsi_periode; print(len(buat_grid_provinsi_periode()))"` |
| Log keputusan tercatat | 0 | 1 keputusan (K-001) | `wc -l log-keputusan.csv` |
| Artefak metrik hasil | Belum ada | Tercatat di `results/124450048/` | `python -m src.common.hasil 124450048 berkas_diverifikasi=58 ...` |

---

## 5. Yang Akan Saya Ubah Jika Ada Satu Sprint Lagi
Pada sprint berikutnya (Sprint 1), saya akan memimpin koordinasi pembuatan parser ekstraksi multi-format (XLSX dengan multi-index header dan JSON CKAN datastore) serta menyusun standardisasi kamus rincian tingkat kerusakan rumah (`rumah_rusak`: rusak berat, rusak sedang, rusak ringan). Selain itu, saya akan mempersiapkan fungsi uji rekonsiliasi penjumlahan kabupaten/kota ke rekapitulasi tingkat provinsi agar saat data Silver selesai, pembentukan panel Gold 38 provinsi dapat langsung dieksekusi secara otomatis tanpa kendala ketidakcocokan skema.
