"""Tahap 6 — tabel nasional dan rekonsiliasi pasangan yang sebanding."""
import pandas as pd

from src import konfigurasi as K
from src import wilayah as W
from src.laporan import ROOT, catat, tabel_md, tulis
from src.silver.deret import peringkat, satu_per_sel


def tabel_nasional(silver):
    nas = silver[silver["wilayah_kode"] == W.INDONESIA].copy()
    nas["kolom"] = nas["seri_kode"] + nas["rincian"].map(lambda r: "" if r == "total" else f" [{r}]")
    total = nas[nas["rincian"] == "total"]
    lebar = total.pivot_table(index="periode", columns="kolom", values="nilai").sort_index()
    return nas, lebar


def irisan(silver, utama, rinci_utama, pembanding, semester=None):
    def per(seri, rinci):
        s = silver[(silver["seri_kode"] == seri) & (silver["rincian"] == rinci) & (silver["wilayah_kode"] == W.INDONESIA)]
        return set(s["periode"]) - set(getattr(K, "PROYEKSI", {}).get(seri, set()))

    a = per(utama, rinci_utama)
    if semester:
        a = {p[:4] for p in a if len(p) == 4 or p.endswith(f"-{semester}")}
    return sorted(set.intersection(a, *[per(s, r) for s, r in pembanding])) if pembanding else []


def _hasil_banding(pasangan, periode, nilai_utama, nilai_pembanding, berkas_utama,
                   berkas_pembanding, jumlah_provinsi=None):
    nilai_utama = float(nilai_utama)
    selisih = float(nilai_pembanding) - nilai_utama
    return {
        "id": pasangan["id"],
        "periode": periode,
        "metode": pasangan["metode"],
        "nilai_utama": nilai_utama,
        "nilai_pembanding": float(nilai_pembanding),
        "selisih_pembanding_minus_utama": selisih,
        "persen_selisih_terhadap_utama": selisih / abs(nilai_utama) * 100 if nilai_utama else None,
        "jumlah_provinsi": jumlah_provinsi,
        "berkas_utama": berkas_utama,
        "berkas_pembanding": berkas_pembanding,
        "status": "cocok" if selisih == 0 else "berbeda",
    }


def _rekonsiliasi_jumlah_provinsi(silver, pasangan):
    """Bandingkan angka nasional dengan jumlah provinsi hanya pada berkas yang memuat keduanya."""
    provinsi = set(W.PROVINSI)
    seri = pasangan["utama"].split(",")[0].strip()
    rincian = pasangan.get("rincian_utama", "total")
    data = silver[(silver["seri_kode"] == seri) & (silver["rincian"] == rincian)]
    hasil = []

    for periode, per_tahun in data.groupby("periode", sort=True):
        kandidat = []
        for berkas, g in per_tahun.groupby("_berkas_raw", sort=True):
            nasional = g[g["wilayah_kode"] == W.INDONESIA]
            daerah = g[g["wilayah_kode"].isin(provinsi)]
            if (len(nasional) != 1 or len(daerah) != len(provinsi)
                    or set(daerah["wilayah_kode"]) != provinsi
                    or daerah["wilayah_kode"].duplicated().any()):
                continue
            kandidat.append({
                "berkas": berkas,
                "peringkat": peringkat(berkas),
                "nasional": float(nasional["nilai"].iloc[0]),
                "jumlah_provinsi": float(daerah["nilai"].sum()),
            })

        if not kandidat:
            continue
        kandidat.sort(key=lambda x: (x["peringkat"], x["berkas"]))
        varian = {}
        for sumber in kandidat:
            kunci_nilai = (sumber["nasional"], sumber["jumlah_provinsi"])
            varian.setdefault(kunci_nilai, sumber)
        for dipilih in varian.values():
            hasil.append(_hasil_banding(
                pasangan, periode, dipilih["nasional"], dipilih["jumlah_provinsi"],
                dipilih["berkas"], dipilih["berkas"], jumlah_provinsi=len(provinsi),
            ))
    return hasil


def _baris_nasional(silver, seri, rincian, periode):
    data = silver[
        (silver["seri_kode"] == seri)
        & (silver["rincian"] == rincian)
        & (silver["periode"] == periode)
    ].copy()
    terpilih, _ = satu_per_sel(data)
    baris = terpilih[terpilih["wilayah_kode"] == W.INDONESIA]
    if len(baris) > 1:
        raise ValueError(f"{seri} [{rincian}] {periode}: lebih dari satu baris nasional terpilih")
    return None if baris.empty else baris.iloc[0]


def _rekonsiliasi_jumlah_rincian(silver, pasangan):
    """Bandingkan total nasional dengan penjumlahan rincian pembentuknya."""
    seri = pasangan["utama"].split(",")[0].strip()
    rincian_utama = pasangan.get("rincian_utama", "total")
    periode_utama = set(silver.loc[
        (silver["seri_kode"] == seri) & (silver["rincian"] == rincian_utama)
        & (silver["wilayah_kode"] == W.INDONESIA), "periode"
    ])
    periode_rinci = [
        set(silver.loc[
            (silver["seri_kode"] == s) & (silver["rincian"] == r)
            & (silver["wilayah_kode"] == W.INDONESIA), "periode"
        ])
        for s, r in pasangan["pembanding"]
    ]
    periode_bersama = set.intersection(periode_utama, *periode_rinci) if periode_rinci else set()
    hasil = []
    for periode in sorted(periode_bersama):
        utama = _baris_nasional(silver, seri, rincian_utama, periode)
        pembanding = [_baris_nasional(silver, s, r, periode) for s, r in pasangan["pembanding"]]
        if utama is None or any(baris is None for baris in pembanding):
            continue
        hasil.append(_hasil_banding(
            pasangan, periode, utama["nilai"],
            sum(float(baris["nilai"]) for baris in pembanding),
            utama["_berkas_raw"],
            "; ".join(f"{s} [{r}]: {baris['_berkas_raw']}"
                      for (s, r), baris in zip(pasangan["pembanding"], pembanding)),
        ))
    return hasil


def rekonsiliasi(silver):
    """Hasilkan perbandingan numerik yang didukung data; WDI yang tak sebanding tetap sebagai konteks."""
    hasil = []
    for pasangan in K.PASANGAN:
        if pasangan["metode"] == "jumlah_provinsi":
            hasil.extend(_rekonsiliasi_jumlah_provinsi(silver, pasangan))
        elif pasangan["metode"] == "jumlah_rincian":
            hasil.extend(_rekonsiliasi_jumlah_rincian(silver, pasangan))
    return pd.DataFrame(hasil, columns=[
        "id", "periode", "metode", "nilai_utama", "nilai_pembanding",
        "selisih_pembanding_minus_utama", "persen_selisih_terhadap_utama",
        "jumlah_provinsi", "berkas_utama", "berkas_pembanding", "status",
    ])


def jalankan(silver):
    nas, lebar = tabel_nasional(silver)
    (ROOT / "reports").mkdir(exist_ok=True)
    lebar.to_csv(ROOT / "reports" / "tabel-nasional.csv")
    numerik = rekonsiliasi(silver)
    numerik.to_csv(ROOT / "reports" / "hasil-rekonsiliasi.csv", index=False)
    baris, bagian = [], []
    for p in K.PASANGAN:
        hasil_p = numerik[numerik["id"] == p["id"]]
        if p["metode"] == "konteks":
            utama = p["utama"].split(",")[0].strip()
            bersama = irisan(silver, utama, p.get("rincian_utama", "total"), p["pembanding"])
        else:
            bersama = sorted(hasil_p["periode"].unique())
        baris.append({"id": p["id"], "seri_utama": p["utama"], "pembanding": ", ".join(f"{s} [{r}]" for s, r in p["pembanding"]) or "—",
                      "jenis": p["jenis"], "periode_beririsan": len(bersama), "tahun": ", ".join(bersama) or "—",
                      "dugaan_kategori": p["kategori"]})
        teks = [f"### {p['id']}: {p['judul']}", f"- Seri utama: `{p['utama']}` (rincian `{p.get('rincian_utama', 'total')}`)",
                "- Pembanding: " + (", ".join(f"`{s}` (rincian `{r}`)" for s, r in p["pembanding"]) or "tidak ada di paket"),
                f"- Jenis: **{p['jenis']}**; tahun yang dapat dibandingkan: {', '.join(bersama) or '—'}",
                f"- Kategori selisih: {p['kategori']}"]
        if p["metode"] != "konteks":
            kolom = ["periode", "nilai_utama", "nilai_pembanding", "selisih_pembanding_minus_utama",
                     "persen_selisih_terhadap_utama", "jumlah_provinsi", "status"]
            teks += ["", "Hasil rekonsiliasi numerik (selisih = pembanding − utama):",
                     tabel_md(hasil_p[kolom]) if len(hasil_p) else "Tidak ada periode dengan cakupan lengkap."]
        else:
            wdi = silver[
                (silver["seri_kode"] == p["utama"])
                & (silver["wilayah_kode"] == W.INDONESIA)
                & silver["nilai"].notna()
            ][["periode", "nilai", "satuan", "_berkas_raw"]]
            wdi = wdi.assign(nilai=wdi["nilai"].map(lambda nilai: format(float(nilai), ".15g")))
            cakupan = K.SERI[p["utama"]].get("cakupan", "")
            teks += ["", f"Nilai WDI dipertahankan sebagai konteks, bukan dikurangkan: {cakupan}.",
                     tabel_md(wdi) if len(wdi) else "Tidak ada observasi WDI non-null."]
        teks += ["", "Pertanyaan keterbandingan dan jawabannya:", ""]
        teks += [f"{i}. **{q}** {a}" for i, (q, a) in enumerate(p["pertanyaan"], 1)]
        bagian.append("\n".join(teks))
    daftar = pd.DataFrame(baris)
    n_selisih = int((daftar["jenis"] == "selisih").sum())
    catat(pasangan_rekonsiliasi=n_selisih, pasangan_konteks=int((daftar["jenis"] != "selisih").sum()),
          periode_beririsan=len(numerik[["id", "periode"]].drop_duplicates()),
          rekonsiliasi_cocok=int((numerik["status"] == "cocok").sum()),
          rekonsiliasi_berbeda=int((numerik["status"] == "berbeda").sum()),
          **{f"irisan_{r.id.lower()}": r.periode_beririsan for r in daftar.itertuples()})
    tulis("pasangan-rekonsiliasi.md", "\n\n".join([
        "# Tabel nasional dan pasangan rekonsiliasi",
        "Dihasilkan `python pipeline.py` (`src/gold/nasional.py`) dari Silver dan `src/konfigurasi.py`. "
        "Perbandingan numerik hanya dilakukan pada tahun dan cakupan wilayah yang lengkap; nilai sumber dan selisih "
        "dipertahankan di `reports/hasil-rekonsiliasi.csv`.",
        "Tabel nasional (periode x seri, rincian total, tampilan lebar): `reports/tabel-nasional.csv`. "
        "Kolom BPS hanya terisi pada tahun survei; itu bentuk datanya, tidak diisi.",
        "## Ringkasan numerik",
        tabel_md(numerik[["id", "periode", "nilai_utama", "nilai_pembanding",
                          "selisih_pembanding_minus_utama", "status"]]) if len(numerik)
        else "Tidak ada pasangan numerik yang dapat dibandingkan.",
        "## Ringkasan pasangan", tabel_md(daftar),
        "## Rincian per pasangan", *bagian,
    ]))
    return {"nasional": nas, "pasangan": daftar, "rekonsiliasi": numerik}
