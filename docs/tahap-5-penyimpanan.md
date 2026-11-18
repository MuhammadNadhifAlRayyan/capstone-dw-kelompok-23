# Tahap 5 — Penyimpanan Silver

## Pilihan basis data

Silver disimpan di SQLite (`data/silver/silver.sqlite`). Data kasus ini berskala kecil untuk
pipeline tim dan prosesnya berjalan lokal; SQLite tidak membutuhkan server atau dependensi Python
tambahan, mudah direproduksi, dan menyediakan transaksi serta kunci primer. DuckDB lebih sesuai
untuk kueri analitik kolumnar pada data besar, sedangkan PostgreSQL lebih sesuai bila diperlukan
akses serentak oleh banyak pengguna atau layanan. Keduanya menambah kebutuhan instalasi/konfigurasi
yang belum diperlukan untuk tahap ini.

Respons JSON mentah tetap dipertahankan di Bronze sebagai dokumen sumber yang otoritatif. JSON
menjaga struktur dan atribut asli yang bisa berubah antar-endpoint, tetapi query lintas berkas,
penegakan tipe/kunci, dan pemeriksaan duplikasi lebih sulit daripada pada tabel relasional. Karena
itu JSON bukan pengganti Silver: Silver memuat observasi yang telah diseragamkan dan menyimpan
`_berkas_raw` serta `_sha256_raw` untuk lineage kembali ke dokumen asli.

## Skema dan pemuatan

`src/silver/sqlite.py` membuat tabel `silver` menggunakan tipe `TEXT`, `INTEGER`, dan `NUMERIC`.
Kunci primer komposit mengikuti kunci unik Silver baku: sumber, seri, wilayah, periode, rincian,
dan berkas sumber. Sebelum menulis, pemuat memeriksa skema, duplikasi, tipe/periode, dan kecocokan
SHA-256 dengan `data/raw/MANIFEST.csv`. Pemuatan ulang mengganti isi tabel dalam transaksi agar
hasil tidak terduplikasi; kegagalan validasi/penulisan dilaporkan, bukan diabaikan.

Setelah pipeline tahap 2–4 menghasilkan `data/silver/silver.parquet`, jalankan dari root repo:

```bash
python -m src.silver.sqlite
```

Jalur input dan database dapat diberikan secara eksplisit:

```bash
python -m src.silver.sqlite data/silver/silver.parquet data/silver/silver.sqlite
```

Output tahap 5 adalah tabel SQLite `silver`, bukan berkas JSON baru.
