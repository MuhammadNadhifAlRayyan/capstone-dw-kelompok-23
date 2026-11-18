"""Keputusan wrangling Kasus 23 — Kerusakan dan kerugian bencana.

Semua keputusan khas kasus ada di berkas ini supaya mudah ditinjau: identitas seri, satuan dan kode
SDG beserta buktinya, cara menulis rincian, berkas mana yang dipakai deret profil, sel yang dinyatakan
tidak terbit, ambang anomali, dan pasangan rekonsiliasi. Setiap keputusan juga tercatat di log-keputusan.csv.
Ini salah satu jawaban yang dapat dipertahankan, bukan satu-satunya.

Nama ukuran BNPB (judul resource dan kepala kolom -> seri) ada di src/kamus_bnpb.py karena sama untuk semua
kasus BNPB; di sini hanya dipilih seri mana yang masuk kasus ini.
"""

KASUS = 23
SLUG = "kerusakan-kerugian-bencana"
JUDUL = "Kerusakan dan kerugian bencana"

FORMAT_BPS = "json"     # tidak dipakai (tidak ada seri BPS)

_CKAN = "judul resource di ckan/package_search-pusdatinkom-01.json"
_U = dict(sumber="bnpb", tingkat="provinsi", satuan="unit", katalog_satuan="unit",
          bukti_satuan="baris satuan '(unit)' di bawah kepala 'Kerusakan' pada rekap 2021/2022 (XLSX tangan)")
_INFRA = dict(sdg="11.5.2", katalog_sdg="11.5.2",
              bukti_sdg="indikator global 11.5.2: kerugian ekonomi langsung, kerusakan infrastruktur kritis, dan gangguan "
                        "layanan dasar akibat bencana; seri ini komponennya")
_RUMAH = dict(sdg="11.5.2|1.5.2", katalog_sdg="11.5.2|1.5.2",
              bukti_sdg="indikator global 1.5.2 = 11.5.2 (kerugian ekonomi langsung akibat bencana); rumah dan aset "
                        "produktif yang rusak adalah komponen penilaiannya")
SERI = {
    "kejadian": dict(sumber="bnpb", tingkat="provinsi", nama="Jumlah kejadian bencana", satuan="kejadian",
                     katalog_satuan="kejadian",
                     bukti_satuan="Keterangan: 'Jumlah Kejadian: Jumlah Total Kejadian Bencana Menurut Klasifikasi Penyajian'",
                     sdg="—", katalog_sdg="—", bukti_sdg="tidak ada indikator global untuk jumlah kejadian",
                     cakupan="penyebut kerusakan per kejadian; satu kejadian satu jenis utama (Keterangan)"),
    "rumah_rusak": dict(**_U, **_RUMAH, nama="Jumlah rumah rusak akibat bencana",
                        cakupan="rekap 2021/2022 per tingkat (berat, sedang, ringan) x jenis; tabel 2024, 2025 per jenis "
                                "tanpa tingkat; rekap nasional 2025 per tingkat; nasional per jenis 2010–2024"),
    "rumah_terendam": dict(**_U, **_RUMAH, nama="Jumlah rumah terendam", cakupan="hanya rekap 2021/2022"),
    "fasyankes_rusak": dict(**_U, **_INFRA, nama="Jumlah fasilitas pelayanan kesehatan rusak",
                            cakupan="kepala rekap 2021/2022 'Sarana Kesehatan'; tabel 2024; rekap nasional 2025; nasional 2010–2024"),
    "satuan_pendidikan_rusak": dict(**_U, **_INFRA, nama="Jumlah satuan pendidikan rusak",
                                    cakupan="kepala rekap 2021/2022 'Sarana Pendidikan'; tabel 2024; rekap nasional 2025"),
    "jembatan_rusak": dict(**_U, **_INFRA, nama="Jumlah jembatan rusak",
                           cakupan="rekap 2021/2022; tabel 2024; rekap nasional 2025; nasional 2010–2024"),
    "kantor_rusak": dict(**_U, sdg="—", katalog_sdg="—", bukti_sdg="bukan komponen indikator global yang dinamai",
                         nama="Jumlah kantor rusak", cakupan="kepala rekap 2021/2022 'Perkantoran'; tabel 2024; nasional 2010–2024"),
    "rumah_ibadat_rusak": dict(**_U, sdg="—", katalog_sdg="—", bukti_sdg="bukan komponen indikator global yang dinamai",
                               nama="Jumlah rumah ibadat rusak",
                               cakupan="kepala rekap 2021/2022 'Sarana Peribadatan'; lembar 2024 'Jumlah Fasdah Rusak'"),
    "kios_toko_rusak": dict(**_U, **_RUMAH, nama="Jumlah kios/toko rusak", cakupan="tabel 2024; nasional 2010–2024"),
    "pabrik_rusak": dict(**_U, **_RUMAH, nama="Jumlah pabrik rusak", cakupan="hanya tabel 2024"),
    "luas_sawah_rusak": dict(
        sumber="bnpb", tingkat="nasional", nama="Luas sawah rusak akibat bencana", satuan="hektar", katalog_satuan="tidak_ada",
        bukti_satuan="tabel tidak menyatakan satuan; Keterangan memakai hektar untuk ambang kejadian ('1 hektar lahan "
                     "terdampak/rusak') dan angkanya berdesimal dua; dugaan, dipastikan dari Juklak Standar Data (katalog) di Sprint 2",
        sdg="11.5.2|1.5.2", katalog_sdg="11.5.2|1.5.2", bukti_sdg="kerugian pertanian adalah komponen 1.5.2",
        cakupan="hanya nasional per jenis 2010–2024", koreksi="tingkat provinsi -> nasional; satuan tidak_ada -> hektar (dugaan)"),
    "luas_lahan_kebun_hutan_rusak": dict(
        sumber="bnpb", tingkat="nasional", nama="Luas lahan, kebun, dan hutan rusak akibat bencana", satuan="hektar",
        katalog_satuan="tidak_ada", bukti_satuan="sama dengan luas_sawah_rusak",
        sdg="11.5.2|1.5.2", katalog_sdg="11.5.2|1.5.2", bukti_sdg="kerugian pertanian dan kehutanan adalah komponen 1.5.2",
        cakupan="hanya nasional per jenis 2010–2024", koreksi="tingkat provinsi -> nasional; satuan tidak_ada -> hektar (dugaan)"),
    "nilai_kerusakan": dict(
        sumber="bnpb", tingkat="provinsi", nama="Nilai kerusakan akibat bencana (usulan rehabilitasi dan rekonstruksi)",
        satuan="rupiah", katalog_satuan="rupiah", bukti_satuan=f"{_CKAN}: 'Nilai Kerusakan dan Kerugian ...'; angka sampai satuan rupiah",
        sdg="11.5.2|1.5.2", katalog_sdg="11.5.2|1.5.2", bukti_sdg="kerugian ekonomi langsung (1.5.2 = 11.5.2)",
        cakupan="per kab/kota yang mengajukan proposal rehabilitasi-rekonstruksi, bukan semua kejadian; dijumlah ke "
                "provinsi per Tahun Kejadian; usulan beberapa tahun kejadian tidak dipakai"),
    "nilai_kerugian": dict(
        sumber="bnpb", tingkat="provinsi", nama="Nilai kerugian akibat bencana (usulan rehabilitasi dan rekonstruksi)",
        satuan="rupiah", katalog_satuan="rupiah", bukti_satuan="sama dengan nilai_kerusakan",
        sdg="11.5.2|1.5.2", katalog_sdg="11.5.2|1.5.2", bukti_sdg="kerugian ekonomi langsung (1.5.2 = 11.5.2)",
        cakupan="sama dengan nilai_kerusakan"),
    "EN.CLC.MDAT.ZS": dict(
        sumber="wdi", tingkat="nasional", nama="Droughts, floods, extreme temperatures (% of population, average 1990-2009)",
        satuan="persen", katalog_satuan="—", bukti_satuan="name: '(% of population, average 1990-2009)'",
        sdg="—", katalog_sdg="—", bukti_sdg="tercantum di sumber46_indikator.json tanpa kode indikator SDG",
        cakupan="satu angka rata-rata 1990–2009 yang ditulis sebagai date 2009; mengukur penduduk terdampak, bukan kerusakan"),
}

# Rincian (K-006): jenis bencana memakai slug kolom tabel per jenis; ejaan lain di rekap disamakan
# (src/kamus_bnpb.py JENIS_SAMA). Tingkat kerusakan rumah dari kepala 'Rumah Rusak Berat/Sedang/Ringan'.
RINCIAN_TOTAL_BPS = set()
RINCIAN_TOTAL_WHO = set()
RINCIAN_DIMENSI = {"jenis_bencana": "jenis_bencana", "tingkat_kerusakan": "tingkat_kerusakan"}
RINCIAN_NILAI = {}
KODE_RINCIAN = {"jenis_bencana": {"banjir", "cuaca_ekstrem", "erupsi_gunung_api", "gelombang_pasang_dan_abrasi",
                                  "gempabumi", "kebakaran_hutan_dan_lahan", "kekeringan", "tanah_longsor", "tsunami"},
                "tingkat_kerusakan": {"berat", "sedang", "ringan"}}

RUJUKAN_TAHUN = {}

# Deret profil = jumlah semua rincian dalam satu berkas (K-005): jenis membagi habis kejadian, dan berat + sedang +
# ringan = semua rumah rusak.
DERET = {s: ["jumlah"] for s, c in SERI.items() if c["sumber"] == "bnpb" and c["tingkat"] == "provinsi"}

# Satu sel provinsi x tahun bisa punya angka dari beberapa berkas (K-007). Deret profil memakai satu berkas.
URUTAN_BERKAS = [
    ("*/5dfcae7e-*", "Jumlah Kejadian Bencana Menurut Provinsi Tahun 2010-2024: angka provinsi yang diterbitkan, satu tabel"),
    ("*/tangan/*per-provinsi*", "rekap provinsi 2021/2022"),
    ("*/tangan/*menurut-provinsi*", "tabel provinsi 2024, 2025 (XLSX)"),
    ("*/datastore/data-bencana-indonesia/fefc94c0-*", "rekapitulasi nilai kerusakan dan kerugian 2015–2024: satu tabel"),
    ("*/datastore/data-bencana-indonesia/*", "tabel provinsi 2024 dataset data-bencana-indonesia"),
    ("*/datastore/kompilasi-*/*", "salinan tabel 2024 dataset kompilasi"),
    ("*/tangan/*kabup*", "rekap kab/kota 2021/2022 yang dijumlahkan ke provinsi: cadangan"),
]

_TAUTAN = ("katalog CKAN (ckan/package_search-pusdatinkom-01.json): untuk tahun ini hanya ada resource tautan "
           "'Jumlah Kejadian Bencana Tahun {t}' tanpa format dan tanpa DataStore; angka provinsi tidak diterbitkan sebagai tabel")
_NASIONAL = ("katalog CKAN: tahun ini hanya terbit di tabel nasional per jenis '... Akibat Bencana Tahun 2010-2024'; "
             "tabel provinsi hanya 2021, 2022 (rekap), 2024, 2025")
_KERUSAKAN = ("rumah_rusak", "fasyankes_rusak", "jembatan_rusak", "kantor_rusak", "rumah_ibadat_rusak", "kios_toko_rusak")
TIDAK_TERBIT = {}
for _s in _KERUSAKAN:
    for _t in range(2010, 2021):
        TIDAK_TERBIT[(_s, "provinsi", str(_t))] = _NASIONAL
    TIDAK_TERBIT[(_s, "provinsi", "2023")] = _TAUTAN.format(t=2023)
for _t in ("2021", "2022"):
    TIDAK_TERBIT[("kios_toko_rusak", "provinsi", _t)] = "rekap 2021/2022 tidak punya kolom kios/toko"
for _s in ("fasyankes_rusak", "jembatan_rusak", "kantor_rusak", "rumah_ibadat_rusak", "satuan_pendidikan_rusak"):
    TIDAK_TERBIT[(_s, "provinsi", "2025")] = ("kompilasi 2025 di katalog hanya punya tabel provinsi kejadian, korban, dan rumah "
                                              "rusak; ukuran ini hanya di rekap nasional 2025")
# nilai kerusakan/kerugian: tabel usulan rehabilitasi-rekonstruksi hanya memuat kab/kota yang mengajukan (K-011)
for _s in ("nilai_kerusakan", "nilai_kerugian"):
    for _t in range(2015, 2025):
        TIDAK_TERBIT[(_s, "provinsi", str(_t))] = ("tabel usulan rehabilitasi-rekonstruksi hanya memuat kab/kota yang "
                                                   "mengajukan; provinsi tanpa baris = tidak ada usulan tahun itu")
TAHUN_TERBIT = {}

# Galat input (K-014): nilai mustahil yang koreksinya tidak jelas tidak masuk Silver; Silver lain dari berkas yang
# sama tetap dipakai.
GALAT_INPUT = {
    ("luas_lahan_kebun_hutan_rusak", 9999, "2012", "jenis_bencana=kebakaran_hutan_dan_lahan"): dict(
        tindakan="buang", berkas="*/1e489e0a-*",
        bukti="44.041.216,5 ha = lebih dari seperlima luas daratan Indonesia; tahun lain kebakaran 6–119.698 ha; "
              "tidak ada berkas lain untuk sel ini, jadi angka yang benar tidak bisa dipastikan"),
}

RENTANG = {"kejadian": (0, 100_000), "unit": (0, 10_000_000), "hektar": (0, 10_000_000),
           "rupiah": (0, 1e15), "persen": (0, 100)}

# Ambang anomali (K-004). Kerusakan dan nilai rupiah sangat menceng: IQR pada log(1 + nilai). Uji patahan butuh
# >= 10 provinsi yang punya angka di kedua periode (nilai usulan sering hanya beberapa provinsi).
ANOMALI = {"k_iqr": 1.5, "min_titik_samping": 6, "lompat_relatif": 0.20, "porsi_patahan": 0.70, "skala": "log1p",
           "min_provinsi_patahan": 10}

PASANGAN = [
    dict(id="P1", judul="Rumah rusak banjir: baris INDONESIA vs jumlah 38 provinsi",
         utama="rumah_rusak", rincian_utama="jenis_bencana=banjir", pembanding=[("rumah_rusak", "jenis_bencana=banjir")],
         jenis="selisih", kategori="seharusnya sama: satu rumah tidak dihitung di dua provinsi (berbeda dengan kejadian)",
         alasan_rincian="baris INDONESIA di tabel per jenis dibandingkan dengan jumlah baris provinsi di berkas yang sama",
         pertanyaan=[
             ("Bolehkah berbeda?", "Untuk kejadian boleh (kejadian lintas provinsi dihitung sekali secara nasional); untuk "
                                  "rumah rusak tidak, karena setiap rumah berada di satu provinsi."),
             ("Dari berkas mana?", "Tabel per jenis 2024 dan 2025 (baris provinsi dan INDONESIA) dan tabel nasional 2010–2024."),
         ]),
    dict(id="P2", judul="Rumah rusak 2025: tabel per jenis vs rekap nasional (berat + sedang + ringan)",
         utama="rumah_rusak", rincian_utama="jenis_bencana=banjir",
         pembanding=[("rumah_rusak", "jenis_bencana=banjir;tingkat_kerusakan=berat"),
                     ("rumah_rusak", "jenis_bencana=banjir;tingkat_kerusakan=sedang"),
                     ("rumah_rusak", "jenis_bencana=banjir;tingkat_kerusakan=ringan")],
         jenis="selisih", kategori="seharusnya sama: dua tabel 2025 dari kompilasi yang sama",
         alasan_rincian="banjir: jenis dengan rumah rusak terbanyak; rekap nasional memecah per tingkat, tabel per jenis tidak",
         pertanyaan=[
             ("Apakah tingkat kerusakan membagi habis?", "Ya: rekap hanya punya tiga kolom rumah rusak (berat, sedang, ringan)."),
             ("Mengapa 2025 saja?", "Rekap nasional per tingkat hanya ada untuk 2025."),
         ]),
    dict(id="P3", judul="Penduduk terdampak kekeringan, banjir, suhu ekstrem (WDI): konteks",
         utama="EN.CLC.MDAT.ZS", rincian_utama="total", pembanding=[("rumah_rusak", "jenis_bencana=banjir")],
         jenis="konteks", kategori="periode dan konsep berbeda: WDI persen penduduk terdampak 1990–2009, BNPB unit rusak",
         alasan_rincian="WDI tanpa rincian; BNPB banjir sebagai contoh jenis yang tercakup",
         pertanyaan=[("Mengapa tidak dihitung selisihnya?", "Konsep berbeda (penduduk vs rumah) dan tidak ada tahun yang sama.")]),
]
