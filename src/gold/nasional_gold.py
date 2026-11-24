"""Persiapan tahap 6 — tabel nasional Gold: seri utama dan pembanding berdampingan per periode.

Satu baris = satu seri x rincian x periode tingkat Indonesia. Sumbernya:
- `baris_indonesia`: baris wilayah 9999 yang diterbitkan penerbit seri itu (BPS/BNPB/tabel statis);
- `pembanding`: seri nasional WDI/WHO/ILOSTAT;
- `agregat`: dihitung dari provinsi bila konfigurasi menetapkannya (GOLD_AGREGAT), dengan aturan tertulis.
Rincian yang masuk: `total` ditambah rincian yang disebut di pasangan rekonsiliasi. Bila satu sel punya
beberapa berkas, berkas dipilih dengan aturan yang sama dengan panel (URUTAN_BERKAS, lalu jalur terurut).

Keluaran: data/gold/nasional.parquet.
"""
import pandas as pd

from src import konfigurasi as K
from src import wilayah as W
from src.laporan import ROOT, catat
from src.silver import deret

KOLOM = ["seri_kode", "rincian", "sumber", "periode", "jenis_periode", "nilai", "satuan", "batas_bawah", "batas_atas",
         "rujukan_tahun", "asal", "_berkas_raw", "_sha256_raw"]


def rincian_dipakai():
    pakai = {}
    for p in K.PASANGAN:
        pakai.setdefault(p["utama"].split(",")[0].strip(), set()).update(
            p.get("rincian_utama_jumlah") or [p.get("rincian_utama", "total")])
        for s, r in p["pembanding"]:
            pakai.setdefault(s, set()).add(r)
    return pakai


def satu_per_sel(g):
    g = g.assign(_p=g["_berkas_raw"].map(deret.peringkat)).sort_values(["_p", "_berkas_raw"])
    return g.drop_duplicates(["seri_kode", "rincian", "periode"]).drop(columns="_p")


def agregat(silver):
    """GOLD_AGREGAT = {seri: dict(rincian=..., alasan=..., berkas_sama=bool)}: angka nasional = jumlah provinsi."""
    bagian = []
    for seri, a in getattr(K, "GOLD_AGREGAT", {}).items():
        r = a.get("rincian", "total")
        s = silver[(silver["seri_kode"] == seri) & (silver["rincian"] == r) & (silver["wilayah_kode"] != W.INDONESIA)]
        if a.get("berkas_sama"):
            # hanya baris provinsi dari berkas yang sama dengan baris INDONESIA-nya (satu tabel dibandingkan dengan
            # dirinya sendiri, bukan dengan berkas lain)
            ind = silver[(silver["seri_kode"] == seri) & (silver["rincian"] == r) & (silver["wilayah_kode"] == W.INDONESIA)]
            s = s[s.set_index(["periode", "_berkas_raw"]).index.isin(ind.set_index(["periode", "_berkas_raw"]).index)]
        s = s.assign(_p=s["_berkas_raw"].map(deret.peringkat)).sort_values(["_p", "_berkas_raw"]) \
            .drop_duplicates(["wilayah_kode", "periode"])
        g = s.groupby("periode", as_index=False).agg(
            nilai=("nilai", "sum"), jenis_periode=("jenis_periode", "first"), sumber=("sumber", "first"),
            satuan=("satuan", "first"), _berkas_raw=("_berkas_raw", lambda x: ";".join(sorted(set(x)))))
        g = g.assign(seri_kode=seri + " (agregat provinsi)", rincian=r, asal="agregat", _sha256_raw=None,
                     batas_bawah=None, batas_atas=None, rujukan_tahun=None)
        bagian.append(g)
    return bagian


def jalankan(silver):
    pakai = rincian_dipakai()
    nas = silver[silver["wilayah_kode"] == W.INDONESIA]
    nas = nas[[r in ({"total"} | pakai.get(s, set())) for s, r in zip(nas["seri_kode"], nas["rincian"])]]
    nas = satu_per_sel(nas.copy())
    tingkat = {k: s["tingkat"] for k, s in K.SERI.items()}
    nas["asal"] = nas["seri_kode"].map(lambda s: "baris_indonesia" if tingkat.get(s) == "provinsi" else "pembanding")
    t = pd.concat([nas, *agregat(silver)], ignore_index=True)
    for c in KOLOM:
        if c not in t:
            t[c] = None
    t = t[KOLOM].sort_values(["seri_kode", "rincian", "periode"]).reset_index(drop=True)
    for c in ("batas_bawah", "batas_atas", "rujukan_tahun"):
        # baris agregat membawa None, baris Silver Int64 <NA>: samakan dulu ke float
        t[c] = pd.to_numeric(t[c].astype(object).where(t[c].notna(), None), errors="coerce").astype("float64")
    (ROOT / "data" / "gold").mkdir(parents=True, exist_ok=True)
    t.to_parquet(ROOT / "data" / "gold" / "nasional.parquet", index=False)
    catat(baris_nasional_gold=len(t), seri_nasional_gold=int(t["seri_kode"].nunique()))
    return t
