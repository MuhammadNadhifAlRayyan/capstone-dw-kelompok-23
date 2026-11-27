# Naskah Demo Sprint 2 (±10 menit) — Kasus 23

Demo Sprint 2 memperlihatkan perjalanan satu angka dari Silver ke panel Gold, ke SQL, dan ke tabel
rekonsiliasi. Rekam layar terminal dan editor.

| Menit | Tunjukkan | Perintah atau berkas |
|---|---|---|
| 0–1 | Sprint Goal dan tiga butir DoD | `sprint/sprint-2/sprint-goal.md` |
| 1–3 | Satu perintah dari mentah sampai Gold, SQL, validasi | `python pipeline.py` (±8.7 detik) |
| 3–4 | Aturan satu nilai per sel dan panel Gold | `reports/panel-gold.md`; buka `data/gold/panel_lebar.parquet` |
| 4–5 | Sel kosong tetap tampil dengan kategorinya | kolom `status_sel` di `data/gold/panel.parquet` |
| 5–6 | Gold di DuckDB, kunci primer menolak sel ganda | `reports/basis-data.md`; kueri di bawah |
| 6–8 | Rekonsiliasi P1: Rumah rusak banjir: baris INDONESIA vs jumlah 38 provinsi | `reports/rekonsiliasi.md`; median 0.0% |
| 8–9 | Validasi Gold dan tes baris yang sengaja dirusak | `reports/validasi.md`, `python -m pytest -q tests/test_gold.py` |
| 9–10 | Satu sel Gold ditelusuri ke berkas mentah; rencana Sprint 3 | `docs/data-dictionary.md` bagian *Contoh penelusuran satu sel Gold* |

Kueri contoh di DuckDB:

```bash
python - <<'EOF'
import duckdb
con = duckdb.connect("data/gold/gudang.duckdb", read_only=True)
print(con.sql("SELECT pasangan_id, kategori, count(*) n, round(median(abs(selisih_relatif)), 1) median_persen "
              "FROM rekonsiliasi GROUP BY ALL ORDER BY pasangan_id"))
EOF
```

Uji reproduksi (tugas Reproduksi): klon repo ke folder baru, jalankan `unduh_data.py` dan `pipeline.py`, lalu
bandingkan ketiga berkas Gold dengan yang di-commit:

```bash
python - <<'EOF'
import pandas as pd
for f in ["silver/silver", "gold/panel", "gold/nasional", "gold/rekonsiliasi"]:
    a = pd.read_parquet(f"data/{f}.parquet")
    b = pd.read_parquet(f"/jalur/repo-asli/data/{f}.parquet")
    print(f, "sama" if a.equals(b) else "berbeda")
EOF
```

Catat waktu jalan di komentar tugas Reproduksi.
