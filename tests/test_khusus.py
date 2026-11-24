"""Aturan khas Kasus 23 diuji dengan baris yang sengaja dirusak."""
from src.validasi import khusus


def test_aturan_keras_lolos_pada_silver_asli(silver_contoh):
    for nama, _, keras, fungsi in khusus.ATURAN:
        if keras:
            assert fungsi(silver_contoh).empty, nama


def test_pecahan_pada_cacah_tertangkap(silver_contoh):
    rusak = silver_contoh.copy()
    i = rusak.index[rusak["seri_kode"] == "rumah_rusak"][0]
    rusak.loc[i, "nilai"] = rusak.loc[i, "nilai"] + 0.5
    assert len(khusus.cacah_bilangan_bulat(rusak)) == 1


def test_tingkat_kerusakan_tidak_sama_tertangkap(silver_contoh):
    rusak = silver_contoh.copy()
    i = rusak.index[(rusak["seri_kode"] == "rumah_rusak") & (rusak["periode"] == "2025") & (rusak["wilayah_kode"] == 9999)
                    & (rusak["rincian"] == "jenis_bencana=banjir;tingkat_kerusakan=berat")][0]
    rusak.loc[i, "nilai"] += 10
    assert len(khusus.rumah_rusak_tingkat_sama_tabel_jenis(rusak)) == 1


def test_galat_input_luas_lahan_tidak_masuk_silver(silver_contoh):
    s = silver_contoh
    sel = s[(s["seri_kode"] == "luas_lahan_kebun_hutan_rusak") & (s["periode"] == "2012")
            & (s["rincian"] == "jenis_bencana=kebakaran_hutan_dan_lahan")]
    assert sel.empty
    assert s.loc[s["seri_kode"] == "luas_lahan_kebun_hutan_rusak", "nilai"].max() < 1_000_000


def test_peringatan_menemukan_kasus_nyata(silver_contoh):
    # rumah rusak 2024: 50 unit masuk DKI Jakarta di tabel provinsi, Jawa Barat di tabel kab/kota
    kab = khusus.kerusakan_kabkota_sama_provinsi(silver_contoh)
    assert set(kab["wilayah_kode"]) == {3100, 3200}
    # 2017: Ogan Ilir tercatat dua kali di tabel per tahun; Sulawesi Tengah Toli Toli (per tahun) vs Buol (rekapitulasi)
    nilai = khusus.nilai_rekap_sama_tabel_tahunan(silver_contoh)
    assert set(nilai["wilayah_kode"]) == {1600, 7200}
