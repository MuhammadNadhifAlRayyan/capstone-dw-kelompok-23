# Tahap 5 — Penyimpanan Silver

## Pilihan basis data

Silver disimpan di SQLite (`data/silver/silver.sqlite`). Data kasus ini berskala kecil untuk
pipeline tim dan prosesnya berjalan lokal; SQLite tidak membutuhkan server atau dependensi Python
tambahan, mudah direproduksi, dan menyediakan transaksi serta kunci primer. DuckDB lebih sesuai
untuk kueri analitik kolumnar pada data besar, sedangkan PostgreSQL lebih sesuai bila diperlukan
akses serentak oleh banyak pengguna atau layanan. Keduanya menambah kebutuhan instalasi/konfigurasi
yang belum diperlukan untuk tahap ini.

Respons JSON mentah tetap dipertahankan di Bronze sebagai dokumen sumber yang otoritatif. JSON
menjaga struktur dan atribut asli yang bisa berubah antar-endpoint, tetapi kueri lintas berkas,
penegakan tipe/kunci, dan pemeriksaan duplikasi lebih sulit daripada pada tabel relasional. Karena
itu JSON bukan pengganti Silver: Silver memuat observasi yang telah diseragamkan dan menyimpan
`_berkas_raw` serta `_sha256_raw` untuk lineage kembali ke dokumen asli.

## Perbandingan Penyimpanan: SQLite (Silver) vs JSON Mentah (Bronze)

Pemisahan antara lapisan Bronze (JSON mentah) dan Silver (SQLite & Parquet) mengikuti prinsip *Medallion Architecture*. Berikut adalah perbandingan komparatif antara penyimpanan SQLite pada Silver dengan penyimpanan JSON mentah pada Bronze:

| Dimensi Evaluasi | Penyimpanan JSON Mentah (Bronze) | Basis Data SQLite (Silver) |
|---|---|---|
| **Paradigma Skema** | *Schema-on-read*: struktur fleksibel mengikuti payload API/CKAN, tipe data tidak ditegakkan secara otomatis saat penyimpanan. | *Schema-on-write*: struktur tabular ketat (`TEXT`, `INTEGER`, `NUMERIC`) dengan validasi kontrak skema sebelum penulisan. |
| **Integritas & Kunci Primer** | Tidak memiliki mekanisme penegakan *Primary Key* bawaan; risiko observasi duplikat tinggi bila tidak difilter manual di kode. | Penegakan *Composite Primary Key* 6 kolom (`sumber`, `seri_kode`, `wilayah_kode`, `periode`, `rincian`, `_berkas_raw`) dengan indeks `WITHOUT ROWID`. |
| **Pencegahan Nilai Tidak Valid** | Nilai disimpan apa adanya (string, angka tercampur koma/titik, null tidak konsisten). | Menggunakan `CHECK (typeof(nilai) IN ('integer', 'real'))` dan verifikasi bahwa kolom teks tidak berisi tipe campuran. |
| **Kemudahan & Performa Kueri** | Sulit dikueri lintas seri/wilayah/tahun tanpa membaca dan mem-parsing puluhan berkas JSON secara berulang ke memori. | Kueri SQL standar instan (`SELECT`, `JOIN`, `GROUP BY`, `WHERE`) dengan pengindeksan b-tree efisien untuk analitik dan rekonsiliasi. |
| **Sifat Transaksi & Atomisitas** | Penulisan berkas bersifat file-by-file; jika proses gagal di tengah jalan, berkas parsial dapat menyebabkan inkonsistensi. | Transaksi ACID penuh (`with koneksi: ...`); penulisan ulang membersihkan dan memuat tabel secara atomik tanpa risiko data setengah terisi. |
| **Ukuran & Efisiensi Disk** | Format teks JSON menyimpan nama kunci secara repetitif pada setiap rekaman, memakan ruang disk lebih besar. | Representasi biner terpadu dalam satu berkas tunggal (`silver.sqlite`), ringkas dan mudah dipindahkan antar-lingkungan kerja. |
| **Fungsi dalam Pipeline** | *Immutable Raw Storage* / *Source of Truth* awal yang menjamin reproduktifitas data mentah dari penyedia (BNPB/WDI). | *Single Version of Truth* data bersih yang siap digunakan untuk agregasi Gold, validasi deret waktu, dan pelaporan nasional. |
| **Audit Trail & Lineage** | Membawa hash berkas asli melalui `MANIFEST.csv`. | Menyimpan kolom audit `_berkas_raw` dan `_sha256_raw` pada setiap baris untuk melacak asal muasal data langsung ke berkas Bronze. |

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

## Keluaran Pengujian dan Pemuatan (Test Execution Output)

### 1. Pemuatan Tabel Silver Pertama ke SQLite

Eksekusi skrip pemuat terhadap berkas `data/silver/silver.parquet` berhasil memvalidasi seluruh kontrak skema dan memuat sebanyak 18.187 baris ke tabel `silver`:

```text
$ python -m src.silver.sqlite data/silver/silver.parquet data/silver/silver.sqlite
SQLite: 18,187 baris dimuat ke data\silver\silver.sqlite (tabel silver)
```

### 2. Pengujian Unit Otomatis (`tests/test_silver_sqlite.py`)

Seluruh unit test suite pemuatan SQLite mencakup pengujian kunci primer, mekanisme muat ulang atomik (*replace*), dan penolakan kunci ganda (*duplicate key rejection*):

```text
$ python -m unittest -v tests.test_silver_sqlite
test_memuat_observasi_ke_tabel_dengan_kunci_primer (tests.test_silver_sqlite.MuatSilverSQLiteTests.test_memuat_observasi_ke_tabel_dengan_kunci_primer) ... ok
test_menolak_kunci_ganda_tanpa_mengubah_tabel (tests.test_silver_sqlite.MuatSilverSQLiteTests.test_menolak_kunci_ganda_tanpa_mengubah_tabel) ... ok
test_muat_ulang_mengganti_isi_tabel (tests.test_silver_sqlite.MuatSilverSQLiteTests.test_muat_ulang_mengganti_isi_tabel) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.099s

OK
```

### 3. Verifikasi Integritas Basis Data SQLite

Pengecekan integritas langsung pada berkas basis data `data/silver/silver.sqlite`:

```text
$ python -c "import sqlite3; conn = sqlite3.connect('data/silver/silver.sqlite'); print('Jumlah baris:', conn.execute('SELECT COUNT(*) FROM silver').fetchone()[0]); print('Kolom PK:', [c[1] for c in conn.execute('PRAGMA table_info(silver)').fetchall() if c[5] > 0])"
Jumlah baris: 18187
Kolom PK: ['sumber', 'seri_kode', 'wilayah_kode', 'periode', 'rincian', '_berkas_raw']
```
