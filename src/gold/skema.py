"""Definisi skema, kamus wilayah 38 provinsi, dan seri utama Gold Kasus 23.

Bagian dari Tahap 4 (Transformasi dan Panel)
Penanggung Jawab: Nabila Nur Azizah (NIM: 124450048)
"""

# Daftar 38 Provinsi Acuan BPS 2025 (wilayah_kode = BPS * 100)
# Plus 9999 untuk Agregat Nasional (Indonesia)
PROVINSI_38_2025 = {
    1100: "ACEH",
    1200: "SUMATERA UTARA",
    1300: "SUMATERA BARAT",
    1400: "RIAU",
    1500: "JAMBI",
    1600: "SUMATERA SELATAN",
    1700: "BENGKULU",
    1800: "LAMPUNG",
    1900: "KEPULAUAN BANGKA BELITUNG",
    2100: "KEPULAUAN RIAU",
    3100: "DKI JAKARTA",
    3200: "JAWA BARAT",
    3300: "JAWA TENGAH",
    3400: "DAERAH ISTIMEWA YOGYAKARTA",
    3500: "JAWA TIMUR",
    3600: "BANTEN",
    5100: "BALI",
    5200: "NUSA TENGGARA BARAT",
    5300: "NUSA TENGGARA TIMUR",
    6100: "KALIMANTAN BARAT",
    6200: "KALIMANTAN TENGAH",
    6300: "KALIMANTAN SELATAN",
    6400: "KALIMANTAN TIMUR",
    6500: "KALIMANTAN UTARA",
    7100: "SULAWESI UTARA",
    7200: "SULAWESI TENGAH",
    7300: "SULAWESI SELATAN",
    7400: "SULAWESI TENGGARA",
    7500: "GORONTALO",
    7600: "SULAWESI BARAT",
    8100: "MALUKU",
    8200: "MALUKU UTARA",
    9100: "PAPUA BARAT",
    9200: "PAPUA BARAT DAYA",
    9400: "PAPUA",
    9500: "PAPUA SELATAN",
    9600: "PAPUA TENGAH",
    9700: "PAPUA PEGUNUNGAN",
}

KODE_NASIONAL = 9999
NAMA_NASIONAL = "INDONESIA"

# Rentang Waktu Kanonik Analisis Panel
TAHUN_AWAL = 2010
TAHUN_AKHIR = 2025

# 14 Seri Utama Kasus 23
SERI_UTAMA_K23 = {
    "kejadian": {"rentang": (2010, 2025), "satuan": "kejadian"},
    "rumah_rusak": {"rentang": (2010, 2025), "satuan": "unit"},
    "rumah_terendam": {"rentang": (2021, 2022), "satuan": "unit"},
    "fasyankes_rusak": {"rentang": (2010, 2025), "satuan": "unit"},
    "satuan_pendidikan_rusak": {"rentang": (2021, 2025), "satuan": "unit"},
    "jembatan_rusak": {"rentang": (2010, 2025), "satuan": "unit"},
    "kantor_rusak": {"rentang": (2010, 2025), "satuan": "unit"},
    "rumah_ibadat_rusak": {"rentang": (2010, 2025), "satuan": "unit"},
    "kios_toko_rusak": {"rentang": (2010, 2024), "satuan": "unit"},
    "pabrik_rusak": {"rentang": (2024, 2024), "satuan": "unit"},
    "luas_sawah_rusak": {"rentang": (2010, 2024), "satuan": "hektar"},
    "luas_lahan_kebun_hutan_rusak": {"rentang": (2010, 2024), "satuan": "hektar"},
    "nilai_kerugian": {"rentang": (2015, 2024), "satuan": "rupiah"},
    "nilai_kerusakan": {"rentang": (2015, 2024), "satuan": "rupiah"},
}

# 9 Kategori Kejadian Bencana Standar BNPB
JENIS_BENCANA = [
    "BANJIR",
    "CUACA EKSTREM",
    "ERUPSI GUNUNG API",
    "GELOMBANG PASANG DAN ABRASI",
    "GEMPABUMI",
    "KEBAKARAN HUTAN DAN LAHAN",
    "KEKERINGAN",
    "TANAH LONGSOR",
    "TSUNAMI",
]
