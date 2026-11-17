# Tahap 3 — Klasifikasi anomali, patahan, dan galat input

Tahap ini mengelompokkan semua penanda IQR dari profil Tahap 2. Nilai tidak diubah:
outlier asli dan patahan seri ditandai, sedangkan perbaikan hanya dibenarkan untuk
galat input yang terbukti dari sumber. Kategori outlier di sini bersifat sementara;
validasi statistik tidak membuktikan penyebab kejadian.

## Ringkasan klasifikasi

- Calon anomali Tahap 2 yang diklasifikasikan: **201**.
- Outlier asli (sementara): **201**.
- Patahan seri berdasarkan uji serentak: **0**.
- Galat input yang terkonfirmasi di antara kandidat: **0**.
- Nilai negatif pada observasi: **0**; nilai pecahan pada seri hitungan: **0**.
- Tidak ada perbaikan angka dilakukan. Tidak ditemukan galat input yang terbukti; ini bukan jaminan bahwa sumber bebas dari semua kesalahan.

Rincian untuk setiap kandidat terdapat pada [`klasifikasi-anomali.csv`](klasifikasi-anomali.csv).

## Uji patahan seri

Uji hanya memakai pasangan provinsi yang memiliki nilai pada dua tahun berurutan.
Patahan serentak ditandai bila sedikitnya 20 provinsi berpasangan, sekurangnya 75%
bergerak searah, dan median lintas-provinsi berubah minimal 50% dari median tahun
sebelumnya. Ini adalah ambang penyaring eksploratif; konfirmasi perubahan definisi
tetap memerlukan dokumentasi sumber.

Pasangan tahun yang memenuhi kedua ambang: **0**. Tidak ada tahun yang ditetapkan sebagai patahan.
Perubahan 2021→2022 pada `rumah_rusak` menurun di 76% provinsi berpasangan, tetapi
median hanya turun sekitar 22%, sehingga tidak memenuhi ambang perubahan median.
Untuk `kejadian`, kenaikan 2020→2021 terjadi pada 74% provinsi; masih di bawah
ambang 75%. Tahun yang tidak berurutan atau memiliki terlalu sedikit pasangan tidak
dapat dinilai dengan uji ini.

Tabel seluruh transisi yang diuji: [`uji-patahan-seri.csv`](uji-patahan-seri.csv).

## Audit duplikasi lintas snapshot

Kunci pembandingan adalah seri, periode, dan provinsi setelah menjumlahkan rincian
jenis bencana dalam satu snapshot. Angka sama lintas snapshot dianggap salinan dari
observasi yang sama dan hanya dihitung sekali; angka berbeda dicatat sebagai revisi
berprovenans, bukan dijumlahkan atau otomatis disebut galat input.

Audit mencakup 266 perbandingan pasangan provinsi: 266 identik, 0 berbeda/revisi, dan 0 hanya tersedia pada satu snapshot. Salinan identik yang tidak dihitung ulang: 228.
Pada snapshot 2024 yang diperiksa, seluruh nilai yang berpasangan identik; tidak ada
revisi berbeda yang perlu dipilih. Rincian per provinsi dan berkas sumber ada pada
[`audit-snapshot-2024.csv`](audit-snapshot-2024.csv).

## Keputusan penanganan

- Outlier asli: pertahankan sebagai nilai sah yang ekstrem; tidak dihapus atau
  di-winsorize. Kasus dengan sebaran nol-dominan (misalnya kios/pabrik) memerlukan
  verifikasi konteks, sebab pagar IQR nol menandai nilai positif.
- Patahan seri: bila kelak terkonfirmasi dari metadata, pertahankan observasi dan
  analisis terpisah sebelum/sesudah perubahan; jangan menghaluskan atau mengganti nilai.
- Galat input: hanya koreksi setelah nilai pembetulan dapat dilacak ke sumber asli;
  catat nilai lama, nilai baru, alasan, dan jumlah baris di `log-keputusan.csv`.
- Aturan deduplikasi dan hasil audit dicatat di `log-keputusan.csv`; tidak ada koreksi
  input pada tahap ini.
