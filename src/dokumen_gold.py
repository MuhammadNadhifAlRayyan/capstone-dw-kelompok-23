"""Bagian Gold di docs/data-dictionary.md (Sprint 2), ditulis sesudah bagian Silver oleh `python pipeline.py`.

Kolom Gold: panel, tabel nasional, rekonsiliasi. Asal setiap kolom ditulis (kolom Silver, grid, kategori
anomali, atau perhitungan Gold), lalu satu sel panel ditelusuri sampai berkas mentahnya.
"""
import pandas as pd

from src.dokumen import _rentang
from src.laporan import ROOT, catat, tabel_md

ARTI = {
    "indikator": ("label deret utama (src/silver/deret.py)", "kode seri, atau 'kode [rincian]' untuk deret berincian"),
    "status_sel": ("grid Sprint 1 (reports/grid-sel-kosong.csv)", "terisi, missing, tidak_diterbitkan, belum_ada, batas_lama"),
    "penanda": ("reports/anomali.csv", "kategori anomali Sprint 1 (outlier, patahan_seri, ...); nilai tidak diubah"),
    "asal": ("src/gold/nasional_gold.py; src/gold/rekonsiliasi.py",
             "nasional: baris_indonesia/pembanding/agregat; rekonsiliasi: keduanya/hanya_utama/hanya_pembanding"),
    "pasangan_id": ("PASANGAN di src/konfigurasi.py", "id pasangan rekonsiliasi (P1, P2, ...)"),
    "jenis": ("PASANGAN", "selisih (dihitung) atau konteks (ditampilkan berdampingan)"),
    "seri_utama": ("PASANGAN", "seri yang direkonsiliasi (BPS/BNPB, atau seri nasional untuk pasangan antarpembanding)"),
    "rincian_utama": ("PASANGAN", "rincian seri utama yang dibandingkan"),
    "seri_pembanding": ("PASANGAN", "seri pembanding; kosong bila pasangan tidak punya pembanding di paket"),
    "rincian_pembanding": ("PASANGAN", "rincian pembanding yang sebanding"),
    "nilai_utama": ("gold_nasional.nilai", "nilai seri utama pada periode itu"),
    "nilai_pembanding": ("gold_nasional.nilai x faktor GOLD_KONVERSI", "nilai pembanding dalam satuan seri utama"),
    "selisih": ("dihitung", "nilai_utama − nilai_pembanding; kosong bila tidak dibandingkan (lihat catatan)"),
    "selisih_relatif": ("dihitung", "100 × selisih / nilai_pembanding (persen)"),
    "kategori": ("PASANGAN (kategori_baku atau teks kategori)", "kategori baku penjelasan selisih"),
    "penjelasan": ("PASANGAN kategori", "alasan selisih dengan bukti dari Sprint 1"),
    "catatan": ("dihitung", "mengapa selisih tidak dihitung pada baris ini (proyeksi, konteks, satuan)"),
}


def _tabel(df, sumber_arti):
    from src.dokumen import ARTI as ARTI_SILVER
    baris = []
    for k in df.columns:
        asal, arti = ARTI.get(k) or ARTI_SILVER.get(k, ("", ""))
        baris.append({"kolom": k, "tipe": str(df[k].dtype), "kosong": int(df[k].isna().sum()),
                      "rentang_atau_nilai": _rentang(df[k]), "asal": asal, "arti": arti})
    return pd.DataFrame(baris)


def tulis_gold(gold):
    p, n, r = gold["panel"], gold["nasional"], gold["rekonsiliasi"]
    tp, tn, tr = _tabel(p, ARTI), _tabel(n, ARTI), _tabel(r, ARTI)
    kosong_arti = [t for t in (tp, tn, tr) if (t["arti"] == "").any()]
    catat(kolom_terdokumentasi=int(sum((t["arti"] != "").sum() for t in (tp, tn, tr))),
          kolom_gold=len(tp) + len(tn) + len(tr))
    if kosong_arti:
        raise SystemExit("data dictionary: ada kolom Gold tanpa arti: "
                         + ", ".join(k for t in kosong_arti for k in t.loc[t["arti"] == "", "kolom"]))
    contoh = p[p["status_sel"] == "terisi"].iloc[0]
    teks = [
        f"## data/gold/panel.parquet ({len(p):,} baris)",
        "Satu baris = satu indikator × provinsi × periode, termasuk sel kosong dari grid. Kunci unik: indikator, "
        "wilayah_kode, periode. Tampilan lebar (satu kolom per indikator, hanya sel terisi): "
        "`data/gold/panel_lebar.parquet`.",
        tabel_md(tp),
        "Satuan per indikator:",
        tabel_md(p.groupby("indikator")["satuan"].first().reset_index()),
        f"## data/gold/nasional.parquet ({len(n):,} baris)",
        "Satu baris = satu seri × rincian × periode tingkat Indonesia. Kunci unik: seri_kode, rincian, periode.",
        tabel_md(tn),
        f"## data/gold/rekonsiliasi.parquet ({len(r):,} baris)",
        "Satu baris = satu pasangan × pembanding × periode. Kunci unik: pasangan_id, seri_pembanding, "
        "rincian_pembanding, periode.",
        tabel_md(tr),
        "## Contoh penelusuran satu sel Gold",
        tabel_md(pd.DataFrame([contoh[["indikator", "wilayah_kode", "periode", "nilai", "_berkas_raw"]]])),
        f"1. Sel ini berasal dari baris Silver `{contoh['seri_kode']}` × {contoh['wilayah_kode']} × {contoh['periode']} "
        f"× rincian `{contoh['rincian']}` × berkas `{contoh['_berkas_raw']}` (aturan *gold: sel tertelusur ke Silver*).",
        "2. Baris Silver itu membawa `_sha256_raw` yang sama dengan `data/raw/MANIFEST.csv` (lihat penelusuran Silver di atas).",
    ]
    jalur = ROOT / "docs" / "data-dictionary.md"
    jalur.write_text(jalur.read_text(encoding="utf-8").rstrip() + "\n\n" + "\n\n".join(teks) + "\n", encoding="utf-8")
