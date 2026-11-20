"""Membangun grid panel, inventaris tingkat wilayah, dan audit agregasi BNPB."""

from __future__ import annotations

import csv
import math
import re
from datetime import date
from pathlib import Path

import pandas as pd

from src.ekstraksi.baca_datastore import baca_semua_datastore
from src.ekstraksi.baca_xlsx import baca_semua_xlsx
from src.gold.skema import (
    JENIS_BENCANA,
    PROVINSI_38_2025,
    SERI_UTAMA_K23,
    TAHUN_AKHIR,
    TAHUN_AWAL,
)

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
YEARS = range(TAHUN_AWAL, TAHUN_AKHIR + 1)
REGION_NAMES = set(PROVINSI_38_2025.values())
REGION_CODES = {name: code for code, name in PROVINSI_38_2025.items()}
NEW_REGION_STARTS = {
    "KALIMANTAN UTARA": 2012,
    "PAPUA BARAT DAYA": 2022,
    "PAPUA SELATAN": 2022,
    "PAPUA TENGAH": 2022,
    "PAPUA PEGUNUNGAN": 2022,
}
DISASTER_COLUMNS = list(JENIS_BENCANA)
DAMAGED_HOUSE_COLUMNS = {
    "berat": "Kerusakan - Rumah Rusak Berat",
    "sedang": "Kerusakan - Rumah Rusak Sedang",
    "ringan": "Kerusakan - Rumah Rusak Ringan",
}
METRIC_COLUMNS_2021_22 = {
    "kejadian": ["Jumlah Kejadian"],
    "rumah_rusak": list(DAMAGED_HOUSE_COLUMNS.values()),
    "rumah_terendam": ["Kerusakan - Rumah Terendam"],
    "fasyankes_rusak": ["Kerusakan - Sarana Kesehatan"],
    "satuan_pendidikan_rusak": ["Kerusakan - Sarana Pendidikan"],
    "rumah_ibadat_rusak": ["Kerusakan - Sarana Peribadatan"],
    "kantor_rusak": ["Kerusakan - Perkantoran"],
    "jembatan_rusak": ["Kerusakan - Jembatan"],
}
REGIONAL_2024 = {
    "kejadian": ("f345ba43", "5ff9f41f"),
    "rumah_rusak": ("b5e3d843", "5c9f7ea9"),
    "fasyankes_rusak": ("26858365", "353da3aa"),
    "satuan_pendidikan_rusak": ("76c8231d", "8eea8adc"),
    "rumah_ibadat_rusak": ("200c487f", "d81153ed"),
    "kantor_rusak": ("091da066", "caefcb96"),
    "kios_toko_rusak": ("cbc56396", "135f1962"),
    "pabrik_rusak": ("5f69273d", "11ba1fdc"),
    "jembatan_rusak": ("ad86fca8", "fdebc70a"),
}
NATIONAL_HISTORY = {
    "kejadian": "9b41007e",
    "rumah_rusak": "27bbeb6b",
    "rumah_ibadat_rusak": "759ee230",
    "fasyankes_rusak": "b2b878ac",
    "kantor_rusak": "4dac65ee",
    "kios_toko_rusak": "69882257",
    "jembatan_rusak": "f34f5637",
    "luas_sawah_rusak": "cda5f236",
    "luas_lahan_kebun_hutan_rusak": "1e489e0a",
}
NATIONAL_2025_COLUMNS = {
    "kejadian": ["Jumlah Kejadian"],
    "rumah_rusak": [
        "Rumah Rusak Berat",
        "Rumah Rusak Sedang",
        "Rumah Rusak Ringan",
    ],
    "satuan_pendidikan_rusak": ["Satuan Pendidikan Rusak"],
    "rumah_ibadat_rusak": ["Rumah Ibadat Rusak"],
    "fasyankes_rusak": ["Fasilitas Pelayanan Kesehatan Rusak"],
    "kantor_rusak": ["Kantor Rusak"],
    "jembatan_rusak": ["Jembatan Rusak"],
}
MONEY_PREFIXES = (
    "03d7c28f",
    "36ec22b9",
    "520b34fd",
    "53f8dc76",
    "a66a93b0",
    "b1aa4eb5",
    "bcf4f458",
    "c013b8a0",
    "cf6d0735",
    "e2c2ed75",
    "fefc94c0",
)


def _key(value: object) -> str:
    return re.sub(r"[^A-Z0-9]", "", str(value).upper())


REGION_ALIASES = {_key(name): name for name in REGION_NAMES}
REGION_ALIASES.update(
    {
        _key("P A P U A"): "PAPUA",
        _key("DI YOGYAKARTA"): "DAERAH ISTIMEWA YOGYAKARTA",
        _key("D.I. YOGYAKARTA"): "DAERAH ISTIMEWA YOGYAKARTA",
        _key("YOGYAKARTA"): "DAERAH ISTIMEWA YOGYAKARTA",
    }
)
DISASTER_ALIASES = {_key(name): name for name in JENIS_BENCANA}
DISASTER_ALIASES.update(
    {
        _key("Letusan Gunung Api"): "ERUPSI GUNUNG API",
        _key("Gempa Bumi"): "GEMPABUMI",
        _key("Gelombang Pasang / Abrasi"): "GELOMBANG PASANG DAN ABRASI",
        _key("Gelombang Pasang dan Abrasi"): "GELOMBANG PASANG DAN ABRASI",
    }
)


def canonical_region(value: object) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    if _key(text).startswith("PROVINSI"):
        text = re.sub(r"(?i)^provinsi\s*", "", text)
    return REGION_ALIASES.get(_key(text))


def canonical_disaster(value: object) -> str:
    result = DISASTER_ALIASES.get(_key(value))
    if result is None:
        raise ValueError(f"Jenis bencana tidak dikenal: {value!r}")
    return result


def find_source(sources: dict[str, pd.DataFrame], prefix: str) -> pd.DataFrame | None:
    return next(
        (frame for name, frame in sources.items() if Path(name).name.startswith(prefix)),
        None,
    )


def numeric_sum(frame: pd.DataFrame, columns: list[str]) -> pd.Series:
    missing = [column for column in columns if column not in frame.columns]
    if missing:
        raise KeyError(f"Kolom sumber tidak ditemukan: {missing}")
    return frame[columns].apply(pd.to_numeric, errors="coerce").sum(axis=1, min_count=1)


def source_year_columns(frame: pd.DataFrame) -> dict[int, str]:
    result = {}
    for column in frame.columns:
        match = re.fullmatch(r"(\d{4})(?:\.0)?", str(column))
        if match:
            result[int(match.group(1))] = column
    return result


def add_national_record(
    records: list[dict],
    seri: str,
    year: int,
    value: object,
    source: str,
    method: str,
) -> None:
    number = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.notna(number):
        records.append(
            {
                "seri": seri,
                "periode": year,
                "nilai": number,
                "wilayah_kode": 9999,
                "wilayah": "INDONESIA",
                "sumber": source,
                "metode": method,
            }
        )


def build_national_observations(
    json_sources: dict[str, pd.DataFrame],
    xlsx_sources: dict[str, pd.DataFrame],
) -> tuple[pd.DataFrame, dict[str, dict[int, list[str]]]]:
    records: list[dict] = []
    national_sources: dict[str, dict[int, list[str]]] = {}

    def register(seri: str, year: int, source: str) -> None:
        national_sources.setdefault(seri, {}).setdefault(year, []).append(source)

    for seri, prefix in NATIONAL_HISTORY.items():
        frame = find_source(json_sources, prefix)
        if frame is None:
            raise FileNotFoundError(f"Sumber nasional tidak ditemukan: {prefix}")
        columns = source_year_columns(frame)
        for year in range(2010, 2025):
            column = columns.get(year)
            if column is None:
                continue
            if year == 2024 and seri in REGIONAL_2024:
                continue
            values = pd.to_numeric(frame[column], errors="coerce")
            if values.notna().any():
                add_national_record(
                    records,
                    seri,
                    year,
                    values.sum(min_count=1),
                    Path(frame["_berkas_raw"].iloc[0]).name,
                    "jumlah kategori jenis bencana pada tabel nasional",
                )
                register(seri, year, Path(frame["_berkas_raw"].iloc[0]).name)

    for seri, (province_prefix, _) in REGIONAL_2024.items():
        frame = find_source(json_sources, province_prefix)
        if frame is None:
            frame = find_source(xlsx_sources, province_prefix)
        if frame is None:
            raise FileNotFoundError(f"Sumber provinsi 2024 tidak ditemukan: {province_prefix}")
        national = frame[
            frame["Provinsi"].astype(str).str.strip().str.casefold() == "indonesia"
        ]
        if len(national) != 1:
            raise ValueError(
                f"Harus ada satu baris Indonesia pada sumber 2024 {seri}, ditemukan {len(national)}"
            )
        value = numeric_sum(national, DISASTER_COLUMNS).sum(min_count=1)
        source = Path(frame["_berkas_raw"].iloc[0]).name
        add_national_record(
            records, seri, 2024, value, source, "baris Indonesia pada tabel provinsi"
        )
        register(seri, 2024, source)

    recap = find_source(xlsx_sources, "6e947c9c")
    if recap is None:
        raise FileNotFoundError("Sumber rekap nasional 2025 tidak ditemukan")
    total = recap[recap["Jenis Bencana"].astype(str).str.strip().str.casefold() == "total"]
    if len(total) != 1:
        raise ValueError(f"Baris Total rekap 2025 harus tepat satu, ditemukan {len(total)}")
    recap_source = Path(recap["_berkas_raw"].iloc[0]).name
    for seri, columns in NATIONAL_2025_COLUMNS.items():
        add_national_record(
            records,
            seri,
            2025,
            numeric_sum(total, columns).iloc[0],
            recap_source,
            "baris Total rekap nasional; tidak menjumlahkan baris Total dengan rinciannya",
        )
        register(seri, 2025, recap_source)

    national = pd.DataFrame(records).sort_values(["seri", "periode"]).reset_index(drop=True)
    if national.duplicated(["seri", "periode"]).any():
        duplicates = national[national.duplicated(["seri", "periode"], keep=False)]
        raise ValueError(f"Observasi nasional duplikat: {duplicates[['seri', 'periode']]}")
    return national, national_sources


def build_grid(observations: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    obs = observations.copy()
    obs["provinsi"] = obs["provinsi"].map(canonical_region)
    if obs["provinsi"].isna().any():
        unknown = observations.loc[obs["provinsi"].isna(), "provinsi"].unique().tolist()
        raise ValueError(f"Nama wilayah pada observasi tahap 2 tidak dikenal: {unknown}")
    obs["wilayah_kode"] = obs["provinsi"].map(REGION_CODES)
    obs["periode"] = pd.to_numeric(obs["periode"], errors="raise").astype(int)
    obs["nilai"] = pd.to_numeric(obs["nilai"], errors="coerce")
    if obs.duplicated(["seri", "periode", "wilayah_kode"]).any():
        raise ValueError("Observasi provinsi memiliki kunci seri-periode-wilayah duplikat")
    lookup = {
        (row.seri, int(row.periode), int(row.wilayah_kode)): row.nilai
        for row in obs.itertuples(index=False)
    }
    published = {
        seri: set(frame.periode.astype(int))
        for seri, frame in obs.groupby("seri")
    }
    grid_records = []
    for seri, config in SERI_UTAMA_K23.items():
        start, end = config["rentang"]
        for year in YEARS:
            for code, region in PROVINSI_38_2025.items():
                original = lookup.get((seri, year, code), math.nan)
                formed = year >= NEW_REGION_STARTS.get(region, TAHUN_AWAL)
                if year < start or year > end:
                    status = "di_luar_rentang_katalog"
                elif not formed:
                    status = "wilayah_belum_terbentuk"
                elif year not in published.get(seri, set()):
                    status = "tidak_ada_sumber_provinsi"
                elif pd.isna(original):
                    status = "kosong_dalam_sumber"
                else:
                    status = "terisi"
                grid_records.append(
                    {
                        "seri": seri,
                        "periode": year,
                        "wilayah_kode": code,
                        "provinsi": region,
                        "nilai_sumber_asli": original,
                        "nilai": original if status == "terisi" else math.nan,
                        "status": status,
                    }
                )
    grid = pd.DataFrame(grid_records)
    if len(grid) != len(SERI_UTAMA_K23) * len(YEARS) * len(PROVINSI_38_2025):
        raise AssertionError("Ukuran grid tidak sesuai 14 seri x 16 tahun x 38 provinsi")
    if grid.duplicated(["seri", "periode", "wilayah_kode"]).any():
        raise AssertionError("Grid memiliki kunci duplikat")

    summary = (
        grid.groupby(["seri", "periode", "status"], dropna=False)
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    for column in (
        "terisi",
        "kosong_dalam_sumber",
        "tidak_ada_sumber_provinsi",
        "wilayah_belum_terbentuk",
        "di_luar_rentang_katalog",
    ):
        if column not in summary:
            summary[column] = 0
    summary["wilayah_aktif"] = 0
    summary["sumber_provinsi_tersedia"] = False
    summary["persen_terisi"] = math.nan
    for index, row in summary.iterrows():
        start, end = SERI_UTAMA_K23[row.seri]["rentang"]
        published_years = published.get(row.seri, set())
        in_range = start <= int(row.periode) <= end
        active = sum(
            int(int(row.periode) >= NEW_REGION_STARTS.get(region, TAHUN_AWAL))
            for region in PROVINSI_38_2025.values()
        )
        summary.loc[index, "wilayah_aktif"] = active if in_range else 0
        available = in_range and int(row.periode) in published_years
        summary.loc[index, "sumber_provinsi_tersedia"] = available
        if available and active:
            summary.loc[index, "persen_terisi"] = (
                100 * row.get("terisi", 0) / active
            )
    summary["sel_kosong_grid"] = summary["kosong_dalam_sumber"]
    return grid, summary.sort_values(["seri", "periode"]).reset_index(drop=True)


def build_availability(
    grid_summary: pd.DataFrame,
    national_sources: dict[str, dict[int, list[str]]],
    json_sources: dict[str, pd.DataFrame],
    xlsx_sources: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    direct_sources: dict[tuple[str, int, str], list[str]] = {}

    def add(seri: str, year: int, level: str, source: str) -> None:
        direct_sources.setdefault((seri, year, level), []).append(source)

    for seri, years in national_sources.items():
        for year, sources in years.items():
            for source in sources:
                add(seri, year, "nasional", source)

    for seri, group in grid_summary.groupby("seri"):
        for row in group.itertuples(index=False):
            if row.sumber_provinsi_tersedia:
                year = int(row.periode)
                source_names = []
                if seri == "kejadian":
                    if year <= 2023:
                        source_names.append("5dfcae7e-6f86-4490-840a-c1bc6393102b.json")
                    if year in (2021, 2022):
                        prefix = "0c165adc" if year == 2021 else "692df9e1"
                        frame = find_source(xlsx_sources, prefix)
                        if frame is not None:
                            source_names.append(Path(frame["_berkas_raw"].iloc[0]).name)
                    if year == 2024:
                        source_names.append("f345ba43-99aa-428c-82d8-4b6a0bba380e.json")
                    if year == 2025:
                        frame = find_source(xlsx_sources, "df39e8c3")
                        if frame is not None:
                            source_names.append(Path(frame["_berkas_raw"].iloc[0]).name)
                elif year in (2021, 2022) and seri in METRIC_COLUMNS_2021_22:
                    prefix = (
                        "0c165adc" if year == 2021 else "692df9e1"
                    )
                    frame = find_source(xlsx_sources, prefix)
                    if frame is not None:
                        source_names.append(Path(frame["_berkas_raw"].iloc[0]).name)
                elif year == 2024 and seri in REGIONAL_2024:
                    prefix = REGIONAL_2024[seri][0]
                    frame = find_source(json_sources, prefix)
                    if frame is None:
                        frame = find_source(xlsx_sources, prefix)
                    if frame is not None:
                        source_names.append(Path(frame["_berkas_raw"].iloc[0]).name)
                elif year == 2025 and seri == "rumah_rusak":
                    frame = find_source(xlsx_sources, "43b83e79")
                    if frame is not None:
                        source_names.append(Path(frame["_berkas_raw"].iloc[0]).name)
                elif seri not in ("nilai_kerusakan", "nilai_kerugian"):
                    source_names.append("observasi-provinsi-tahap-2.csv")
                for source in source_names:
                    add(seri, year, "provinsi", source)

    for year in range(2010, 2025):
        add(
            "kejadian",
            year,
            "kabupaten_kota",
            "21044ffd-c397-4b3c-acbd-5adaa03d79e3.json",
        )
    for year in (2021, 2022):
        for seri in METRIC_COLUMNS_2021_22:
            add(seri, year, "kabupaten_kota", f"rekap kabupaten/kota {year} XLSX")
    for seri, (_, county_prefix) in REGIONAL_2024.items():
        county = find_source(json_sources, county_prefix)
        source = (
            Path(county["_berkas_raw"].iloc[0]).name
            if county is not None
            else f"sumber kabupaten/kota {county_prefix}"
        )
        add(seri, 2024, "kabupaten_kota", source)

    for prefix in MONEY_PREFIXES:
        frame = find_source(json_sources, prefix)
        if frame is None or "Tahun Kejadian" not in frame:
            continue
        year_values = pd.to_numeric(frame["Tahun Kejadian"], errors="coerce")
        for seri, column in (
            ("nilai_kerugian", "Nilai Kerugian"),
            ("nilai_kerusakan", "Nilai Kerusakan"),
        ):
            if column not in frame:
                continue
            rows = frame[year_values.notna() & pd.to_numeric(frame[column], errors="coerce").notna()]
            if "Provinsi" in rows:
                for year in pd.to_numeric(rows["Tahun Kejadian"], errors="coerce").dropna().unique():
                    if rows.loc[
                        pd.to_numeric(rows["Tahun Kejadian"], errors="coerce").eq(year),
                        "Provinsi",
                    ].map(canonical_region).notna().any():
                        add(seri, int(year), "provinsi", Path(frame["_berkas_raw"].iloc[0]).name)
            if "Kabupaten" in rows:
                district = rows[rows["Kabupaten"].notna()]
                for year, count in pd.to_numeric(district["Tahun Kejadian"], errors="coerce").groupby(
                    pd.to_numeric(district["Tahun Kejadian"], errors="coerce")
                ).size().items():
                    if pd.notna(year) and count:
                        add(seri, int(year), "kabupaten_kota", Path(frame["_berkas_raw"].iloc[0]).name)

    rows = []
    for seri in SERI_UTAMA_K23:
        for year in YEARS:
            for level in ("nasional", "provinsi", "kabupaten_kota"):
                sources = sorted(set(direct_sources.get((seri, year, level), [])))
                if seri in ("nilai_kerugian", "nilai_kerusakan") and level == "provinsi" and sources:
                    method = (
                        "agregat provinsi tahap 2 dari catatan proposal; bukan tabel provinsi langsung"
                    )
                elif sources:
                    method = (
                        "observasi tahap 2 dari sumber provinsi"
                        if level == "provinsi"
                        else "langsung dari sumber"
                    )
                else:
                    method = "tidak ditemukan sumber pada tingkat wilayah ini"
                rows.append(
                    {
                        "seri": seri,
                        "periode": year,
                        "tingkat_wilayah": level,
                        "ada_sumber": bool(sources),
                        "sumber": " | ".join(sources),
                        "metode": method,
                    }
                )
    availability = pd.DataFrame(rows)
    if len(availability) != len(SERI_UTAMA_K23) * len(YEARS) * 3:
        raise AssertionError("Matriks ketersediaan tidak mencakup semua seri-tahun-tingkat")
    return availability


def build_house_dictionary() -> pd.DataFrame:
    source_aliases = {
        "BANJIR": ("BANJIR", "Banjir"),
        "CUACA EKSTREM": ("CUACA EKSTREM", "Cuaca Ekstrem"),
        "ERUPSI GUNUNG API": ("LETUSAN GUNUNG API", "Letusan Gunung Api"),
        "GELOMBANG PASANG DAN ABRASI": (
            "GELOMBANG PASANG / ABRASI",
            "Gelombang Pasang / Abrasi",
        ),
        "GEMPABUMI": ("GEMPA BUMI", "Gempa Bumi"),
        "KEBAKARAN HUTAN DAN LAHAN": (
            "KEBAKARAN HUTAN DAN LAHAN",
            "Kebakaran Hutan dan Lahan",
        ),
        "KEKERINGAN": ("KEKERINGAN", "Kekeringan"),
        "TANAH LONGSOR": ("TANAH LONGSOR", "Tanah Longsor"),
        "TSUNAMI": (None, None),
    }
    records = []
    for disaster in JENIS_BENCANA:
        alias_2021, alias_2022 = source_aliases[disaster]
        for level, column in DAMAGED_HOUSE_COLUMNS.items():
            records.append(
                {
                    "jenis_bencana_baku": disaster,
                    "alias_sumber_2021": alias_2021,
                    "alias_sumber_2022": alias_2022,
                    "tingkat_kerusakan_baku": level,
                    "kolom_sumber_2021_2022": column if alias_2021 else "",
                    "ketersediaan_2021_2022": (
                        "rincian tersedia" if alias_2021 else "jenis bencana tidak ada pada tabel"
                    ),
                    "ketersediaan_2010_2020_2023_2024": "hanya total per jenis bencana",
                    "ketersediaan_2025_nasional": "rincian tersedia pada rekap nasional",
                    "aturan": "Jangan isi tingkat kerusakan yang tidak tersedia dengan nol.",
                }
            )
        records.append(
            {
                "jenis_bencana_baku": disaster,
                "alias_sumber_2021": alias_2021,
                "alias_sumber_2022": alias_2022,
                "tingkat_kerusakan_baku": "total",
                "kolom_sumber_2021_2022": "jumlah tingkat berat+sedang+ringan",
                "ketersediaan_2021_2022": (
                    "dapat dijumlahkan dari tiga tingkat" if alias_2021 else "jenis bencana tidak ada pada tabel"
                ),
                "ketersediaan_2010_2020_2023_2024": "total per jenis bencana",
                "ketersediaan_2025_nasional": "jumlah tingkat berat+sedang+ringan",
                "aturan": "Total 2021/2022 dihitung hanya dari rincian non-null; sumber total tidak dijumlahkan ulang.",
            }
        )
    return pd.DataFrame(records)


def build_house_detail(
    json_sources: dict[str, pd.DataFrame],
    xlsx_sources: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    records: list[dict] = []

    def append(
        year: int,
        level: str,
        region: str,
        disaster: object,
        detail: str,
        value: object,
        source: str,
        disclosure: str,
    ) -> None:
        number = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
        if pd.notna(number):
            records.append(
                {
                    "periode": year,
                    "tingkat_wilayah": level,
                    "wilayah": region,
                    "jenis_bencana_baku": canonical_disaster(disaster),
                    "tingkat_kerusakan_baku": detail,
                    "nilai": number,
                    "keteruraian_sumber": disclosure,
                    "sumber": source,
                }
            )

    history = find_source(json_sources, NATIONAL_HISTORY["rumah_rusak"])
    if history is None:
        raise FileNotFoundError("Sumber nasional rumah rusak historis tidak ditemukan")
    history_cols = source_year_columns(history)
    for year, column in history_cols.items():
        if year > 2023:
            continue
        for _, row in history.iterrows():
            if pd.notna(row.get(column)):
                append(
                    year,
                    "nasional",
                    "INDONESIA",
                    row["JENIS BENCANA"],
                    "total",
                    row[column],
                    Path(history["_berkas_raw"].iloc[0]).name,
                    "total; tingkat kerusakan tidak dipisah",
                )

    for year, province_prefix, county_prefix in (
        (2021, "0c165adc", "6ec0418d"),
        (2022, "692df9e1", "9170802b"),
    ):
        for level, prefix in (("provinsi", province_prefix), ("kabupaten_kota", county_prefix)):
            frame = find_source(xlsx_sources, prefix)
            if frame is None:
                raise FileNotFoundError(f"Tabel rumah rusak {year} tidak ditemukan: {prefix}")
            source = Path(frame["_berkas_raw"].iloc[0]).name
            for _, row in frame.iterrows():
                region = canonical_region(row["Provinsi"])
                if level == "provinsi":
                    if region is None:
                        raise ValueError(f"Nama provinsi rumah rusak tidak dikenal: {row['Provinsi']!r}")
                    location = region
                else:
                    if region is None:
                        raise ValueError(f"Provinsi induk rumah rusak tidak dikenal: {row['Provinsi']!r}")
                    location = f"{region} / {str(row['Kabupaten/Kota']).strip()}"
                if not location or location == "nan":
                    continue
                event = canonical_disaster(row["Jenis Bencana"])
                present = False
                for detail, column in DAMAGED_HOUSE_COLUMNS.items():
                    value = pd.to_numeric(pd.Series([row.get(column)]), errors="coerce").iloc[0]
                    if pd.notna(value):
                        present = True
                        append(year, level, location, event, detail, value, source, "rincian tersedia")
                values = pd.to_numeric(
                    pd.Series([row.get(column) for column in DAMAGED_HOUSE_COLUMNS.values()]),
                    errors="coerce",
                )
                if present:
                    append(
                        year,
                        level,
                        location,
                        event,
                        "total",
                        values.sum(min_count=1),
                        source,
                        "total dihitung dari rincian non-null",
                    )

    for year, province_prefix, county_prefix in (
        (2024, "b5e3d843", "5c9f7ea9"),
        (2025, "43b83e79", None),
    ):
        province_frame = find_source(json_sources, province_prefix)
        if province_frame is None:
            province_frame = find_source(xlsx_sources, province_prefix)
        if province_frame is None:
            raise FileNotFoundError(f"Tabel rumah rusak provinsi {year} tidak ditemukan")
        for _, row in province_frame.iterrows():
            raw_region = row.get("Provinsi")
            region = canonical_region(raw_region)
            is_national = str(raw_region).strip().casefold() == "indonesia"
            if not region and not is_national:
                raise ValueError(f"Nama wilayah rumah rusak tidak dikenal: {raw_region!r}")
            level = "nasional" if is_national else "provinsi"
            location = "INDONESIA" if is_national else region
            if year == 2025 and is_national:
                continue
            source = Path(province_frame["_berkas_raw"].iloc[0]).name
            for disaster in DISASTER_COLUMNS:
                append(
                    year,
                    level,
                    location,
                    disaster,
                    "total",
                    row.get(disaster),
                    source,
                    "total; tingkat kerusakan tidak dipisah",
                )
        if county_prefix:
            county_frame = find_source(json_sources, county_prefix)
            if county_frame is None:
                raise FileNotFoundError("Tabel kabupaten rumah rusak 2024 tidak ditemukan")
            province_code_lookup = {
                int(float(row["Kode Wilayah Provinsi"])): canonical_region(row["Provinsi"])
                for _, row in province_frame[
                    ["Kode Wilayah Provinsi", "Provinsi"]
                ].dropna().iterrows()
                if canonical_region(row["Provinsi"])
            }
            county_code_column = "Kode Wilayah Kabupaten / Kota"
            for _, row in county_frame.iterrows():
                county_name = str(row.get("Nama Kabupaten/Kota", "")).strip()
                if county_name.casefold() == "indonesia":
                    continue
                code = pd.to_numeric(pd.Series([row.get(county_code_column)]), errors="coerce").iloc[0]
                parent = (
                    province_code_lookup.get(int(code) // 100)
                    if pd.notna(code)
                    else None
                )
                if parent is None:
                    raise ValueError(f"Provinsi induk kabupaten rumah rusak tidak dikenal: {code!r}")
                location = f"{parent} / {county_name}"
                source = Path(county_frame["_berkas_raw"].iloc[0]).name
                for disaster in DISASTER_COLUMNS:
                    append(
                        2024,
                        "kabupaten_kota",
                        location,
                        disaster,
                        "total",
                        row.get(disaster),
                        source,
                        "total; tingkat kerusakan tidak dipisah",
                    )

    recap = find_source(xlsx_sources, "6e947c9c")
    total = recap[recap["Jenis Bencana"].astype(str).str.strip().str.casefold() == "total"]
    for _, row in recap[
        recap["Jenis Bencana"].astype(str).str.strip().str.casefold() != "total"
    ].iterrows():
        event = canonical_disaster(row["Jenis Bencana"])
        source = Path(recap["_berkas_raw"].iloc[0]).name
        for detail, column in (
            ("berat", "Rumah Rusak Berat"),
            ("sedang", "Rumah Rusak Sedang"),
            ("ringan", "Rumah Rusak Ringan"),
        ):
            append(2025, "nasional", "INDONESIA", event, detail, row[column], source, "rincian tersedia")
        append(
            2025,
            "nasional",
            "INDONESIA",
            event,
            "total",
            sum(
                pd.to_numeric(pd.Series([row[column]]), errors="coerce").iloc[0]
                for column in ("Rumah Rusak Berat", "Rumah Rusak Sedang", "Rumah Rusak Ringan")
            ),
            source,
            "total dihitung dari rincian nasional",
        )

    return pd.DataFrame(records).sort_values(
        ["periode", "tingkat_wilayah", "wilayah", "jenis_bencana_baku", "tingkat_kerusakan_baku"]
    ).reset_index(drop=True)


def grouped_totals(
    frame: pd.DataFrame, columns: list[str], key_column: str
) -> pd.Series:
    working = frame.copy()
    working["_nilai"] = numeric_sum(working, columns)
    return working.dropna(subset=[key_column, "_nilai"]).groupby(key_column)["_nilai"].sum(min_count=1)


def compare_totals(
    series: str,
    year: int,
    source_pair: str,
    province_totals: pd.Series,
    county_totals: pd.Series,
) -> list[dict]:
    joined = pd.concat(
        [province_totals.rename("nilai_provinsi"), county_totals.rename("jumlah_kabupaten_kota")],
        axis=1,
    )
    output = []
    for region, row in joined.iterrows():
        province_value = row["nilai_provinsi"]
        county_value = row["jumlah_kabupaten_kota"]
        if pd.isna(province_value) or pd.isna(county_value):
            status = "tidak_ada_pasangan"
            difference = math.nan
        else:
            difference = county_value - province_value
            status = "cocok" if math.isclose(county_value, province_value, abs_tol=1e-9) else "berbeda"
        output.append(
            {
                "seri": series,
                "periode": year,
                "provinsi": region,
                "sumber_pasangan": source_pair,
                "nilai_provinsi": province_value,
                "jumlah_kabupaten_kota": county_value,
                "selisih_kabupaten_minus_provinsi": difference,
                "status": status,
            }
        )
    return output


def build_aggregation_audit(
    json_sources: dict[str, pd.DataFrame],
    xlsx_sources: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    rows: list[dict] = []
    province_history = find_source(json_sources, "5dfcae7e")
    county_history = find_source(json_sources, "21044ffd")
    if province_history is None or county_history is None:
        raise FileNotFoundError("Sumber kejadian historis provinsi/kabupaten tidak ditemukan")
    code_map = {}
    for _, row in province_history[["Kode Wilayah Provinsi", "Nama Provinsi"]].dropna().iterrows():
        region = canonical_region(row["Nama Provinsi"])
        if region:
            code_map[int(float(row["Kode Wilayah Provinsi"]))] = region
    county_code_column = "Kode Wilayah Kabupaten / Kota"
    county_history = county_history.copy()
    county_history["_provinsi"] = pd.to_numeric(
        county_history[county_code_column], errors="coerce"
    ).map(lambda code: code_map.get(int(code) // 100) if pd.notna(code) else None)
    for year, column in source_year_columns(province_history).items():
        if year > 2024:
            continue
        province_history["_provinsi"] = province_history["Nama Provinsi"].map(canonical_region)
        province_totals = grouped_totals(province_history, [column], "_provinsi")
        county_totals = grouped_totals(county_history, [column], "_provinsi")
        rows.extend(
            compare_totals(
                "kejadian",
                year,
                "historis 2010-2024: dataset provinsi vs kabupaten",
                province_totals,
                county_totals,
            )
        )

    for year, province_prefix, county_prefix in (
        (2021, "0c165adc", "6ec0418d"),
        (2022, "692df9e1", "9170802b"),
    ):
        province_frame = find_source(xlsx_sources, province_prefix)
        county_frame = find_source(xlsx_sources, county_prefix)
        if province_frame is None or county_frame is None:
            raise FileNotFoundError(f"Sumber XLSX kabupaten/provinsi {year} tidak ditemukan")
        for series, columns in METRIC_COLUMNS_2021_22.items():
            province_totals = grouped_totals(
                province_frame.assign(_provinsi=province_frame["Provinsi"].map(canonical_region)),
                columns,
                "_provinsi",
            )
            county_totals = grouped_totals(
                county_frame.assign(_provinsi=county_frame["Provinsi"].map(canonical_region)),
                columns,
                "_provinsi",
            )
            rows.extend(
                compare_totals(
                    series,
                    year,
                    f"rekap provinsi vs kabupaten/kota {year} XLSX",
                    province_totals,
                    county_totals,
                )
            )

    for series, (province_prefix, county_prefix) in REGIONAL_2024.items():
        province_frame = find_source(json_sources, province_prefix)
        if province_frame is None:
            province_frame = find_source(xlsx_sources, province_prefix)
        county_frame = find_source(json_sources, county_prefix)
        if county_frame is None:
            county_frame = find_source(xlsx_sources, county_prefix)
        if province_frame is None or county_frame is None:
            raise FileNotFoundError(f"Pasangan sumber 2024 tidak lengkap untuk {series}")
        province_frame = province_frame.copy()
        province_frame["_provinsi"] = province_frame["Provinsi"].map(canonical_region)
        province_totals = grouped_totals(province_frame, DISASTER_COLUMNS, "_provinsi")
        code_lookup = {}
        for _, row in province_frame[["Kode Wilayah Provinsi", "Provinsi"]].dropna().iterrows():
            region = canonical_region(row["Provinsi"])
            if region:
                code_lookup[int(float(row["Kode Wilayah Provinsi"]))] = region
        county_frame = county_frame.copy()
        county_code = next(
            (column for column in county_frame if "Kode Wilayah Kabupaten" in str(column)),
            None,
        )
        if county_code is None:
            raise KeyError(f"Kode kabupaten/kota tidak ditemukan untuk {series}")
        county_frame["_provinsi"] = pd.to_numeric(county_frame[county_code], errors="coerce").map(
            lambda code: code_lookup.get(int(code) // 100) if pd.notna(code) else None
        )
        county_totals = grouped_totals(county_frame, DISASTER_COLUMNS, "_provinsi")
        rows.extend(
            compare_totals(
                series,
                2024,
                f"tabel provinsi vs kabupaten/kota 2024 ({province_prefix}/{county_prefix})",
                province_totals,
                county_totals,
            )
        )
    audit = pd.DataFrame(rows).sort_values(["seri", "periode", "provinsi"]).reset_index(drop=True)
    return audit


def write_report(
    grid: pd.DataFrame,
    summary: pd.DataFrame,
    availability: pd.DataFrame,
    house_detail: pd.DataFrame,
    aggregation: pd.DataFrame,
    observation_count: int,
    outlier_count: int,
) -> None:
    active_missing = summary[
        summary["sumber_provinsi_tersedia"] & (summary["sel_kosong_grid"] > 0)
    ]
    aggregate_summary = (
        aggregation.groupby(["seri", "periode", "sumber_pasangan", "status"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    if "cocok" not in aggregate_summary:
        aggregate_summary["cocok"] = 0
    if "berbeda" not in aggregate_summary:
        aggregate_summary["berbeda"] = 0
    if "tidak_ada_pasangan" not in aggregate_summary:
        aggregate_summary["tidak_ada_pasangan"] = 0
    lines = [
        "# Tahap 3 — Grid panel dan kelengkapan wilayah",
        "",
        "## Aturan grid dan missing",
        "",
        f"- Grid berisi {len(grid):,} sel (14 seri × 16 tahun × 38 provinsi); baris Indonesia disimpan terpisah di `observasi-nasional-tahap-3.csv`.",
        f"- Input provinsi berisi {observation_count:,} observasi seri-provinsi-periode; ini adalah grain keluaran profil tahap 2, bukan klaim jumlah seluruh baris tabel Silver mentah.",
        "- `terisi` hanya menyalin nilai dari sumber provinsi; `kosong_dalam_sumber` hanya dipakai jika sumber provinsi tersedia tetapi provinsinya tidak memiliki observasi.",
        "- `tidak_ada_sumber_provinsi` tidak dihitung sebagai missing. Nilai sel kosong tidak diisi nol.",
        "- `nilai_sumber_asli` dipertahankan untuk audit. Nilai provinsi pemekaran sebelum tahun pembentukan tidak dipakai pada `nilai` dan berstatus `wilayah_belum_terbentuk`.",
        "- Denominator kelengkapan mengikuti jumlah provinsi yang sudah terbentuk pada tahun itu (33 pada 2010–2011; 34 pada 2012–2021; 38 mulai 2022).",
        "",
        "## Kelengkapan pada tahun dengan sumber provinsi",
        "",
        "| Seri | Tahun | Terisi | Kosong | Denominator aktif | Persen |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in summary.itertuples(index=False):
        if row.sumber_provinsi_tersedia:
            lines.append(
                f"| {row.seri} | {row.periode} | {row.terisi} | {row.sel_kosong_grid} | {row.wilayah_aktif} | {row.persen_terisi:.1f}% |"
            )
    lines.extend(
        [
            "",
            "Tahun di luar rentang katalog dan tahun tanpa sumber provinsi tetap tercantum di grid, tetapi tidak masuk denominator kelengkapan. Rincian setiap sel ada di `grid-provinsi-tahap-3.csv`; rekap semua seri-tahun ada di `kelengkapan-panel-per-tahun.csv`.",
            "",
            "## Matriks tingkat wilayah",
            "",
            "Matriks `ketersediaan-seri-wilayah-tahap-3.csv` membedakan sumber nasional, provinsi, dan kabupaten/kota untuk seluruh seri dan 2010–2025. Rekap proposal nilai kerusakan/kerugian memuat catatan tingkat kabupaten; agregat provinsi tahap 2 tidak diperlakukan sebagai tabel provinsi independen.",
            "",
            "## Kamus rumah rusak",
            "",
            f"Kamus kategori mencakup {len(JENIS_BENCANA)} jenis bencana baku dan tingkat berat/sedang/ringan/total. Tabel rincian terharmonisasi memiliki {len(house_detail):,} baris: 2021–2022 memuat tingkat kerusakan, sumber nasional historis dan tabel 2024 tidak memisahkan tingkat, sedangkan rekap nasional 2025 menyediakan tingkat per jenis bencana. Tsunami tidak muncul pada tabel XLSX provinsi/kabupaten 2021–2022.",
            "Alias `Letusan Gunung Api` disatukan dengan `ERUPSI GUNUNG API`; `Gempa Bumi` dengan `GEMPABUMI`; dan variasi penulisan gelombang pasang disatukan. Kategori yang tidak tersedia dibiarkan tanpa nilai, bukan nol.",
            "",
            "Lihat `kamus-rincian-rumah-rusak.csv` dan `rincian-rumah-rusak-harmonisasi.csv`.",
            "",
            "## Audit jumlah kabupaten/kota ke provinsi",
            "",
            "| Seri | Tahun | Pasangan wilayah | Cocok | Berbeda | Tanpa pasangan |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in aggregate_summary.itertuples(index=False):
        lines.append(
            f"| {row.seri} | {row.periode} | {row.cocok + row.berbeda + row.tidak_ada_pasangan} | {row.cocok} | {row.berbeda} | {row.tidak_ada_pasangan} |"
        )
    lines.extend(
        [
            "",
            "Audit memakai sumber kabupaten dan provinsi yang tersedia secara berpasangan; nilai tidak disesuaikan. Untuk kejadian historis, perbandingan mencakup 2010–2024; untuk dampak 2021–2022 memakai XLSX rekap; dan untuk 2024 memakai tabel kompilasi provinsi/kabupaten. Proposal nilai kerusakan/kerugian tidak dibandingkan karena agregat provinsinya dibentuk dari catatan proposal yang sama, bukan pembanding independen.",
            "",
            f"Jumlah calon anomali yang tetap ditandai: {outlier_count}. Tidak ada outlier yang dihapus atau diperbaiki pada tahap ini.",
            "",
        ]
    )
    (REPORTS / "tahap-3-grid-kelengkapan.md").write_text("\n".join(lines), encoding="utf-8")


def append_decisions(
    grid: pd.DataFrame,
    house_detail: pd.DataFrame,
    aggregation: pd.DataFrame,
) -> None:
    path = ROOT / "log-keputusan.csv"
    with path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        existing = list(reader)
    if not fieldnames or "id" not in fieldnames:
        raise ValueError(f"Skema log keputusan tidak valid: {path}")
    existing_ids = {row["id"] for row in existing}
    missing_groups = (
        grid[grid["status"].eq("kosong_dalam_sumber")]
        .groupby(["seri", "periode"])["provinsi"]
        .agg(lambda values: sorted(values.tolist()))
        .reset_index()
    )
    diff_count = int(aggregation["status"].eq("berbeda").sum())
    raw_unformed = int(
        grid.loc[grid["status"].eq("wilayah_belum_terbentuk"), "nilai_sumber_asli"].notna().sum()
    )
    base_decisions = [
        {
            "id": "K-006",
            "tanggal": date.today().isoformat(),
            "nim": "124450091",
            "tahap": "panel",
            "seri_kode": "semua",
            "keputusan": (
                "Membentuk grid tetap 38 provinsi × 2010–2025 untuk 14 seri; memisahkan Indonesia; "
                "membedakan nilai terisi, kosong pada tahun bersumber, tidak ada sumber provinsi, "
                "di luar rentang katalog, dan wilayah belum terbentuk."
            ),
            "alternatif_ditolak": "Menghilangkan sel kosong dan menganggap tahun tanpa publikasi atau angka kosong sebagai nol.",
            "alasan": (
                "Ketiadaan sumber provinsi bukan missing. Missing hanya ditetapkan pada sel provinsi aktif "
                "ketika sumber untuk seri-tahun tersedia tetapi observasi tidak ada; nilai kosong tidak diimputasi."
            ),
            "dampak_baris": len(grid),
        },
        {
            "id": "K-007",
            "tanggal": date.today().isoformat(),
            "nim": "124450091",
            "tahap": "panel",
            "seri_kode": "semua",
            "keputusan": (
                "Sesuai K-001, Kalimantan Utara baru aktif mulai 2012 dan empat provinsi Papua baru mulai 2022. "
                f"Nilai sumber retrospektif pada {raw_unformed} sel pra-pembentukan dipertahankan di "
                "`nilai_sumber_asli`, tetapi `nilai` analisis dikosongkan."
            ),
            "alternatif_ditolak": "Memakai nilai retrospektif seolah provinsi sudah ada atau menggabungkannya ke provinsi induk.",
            "alasan": "Menjaga susunan wilayah sesuai aturan Sprint 0 tanpa mengubah batas wilayah historis.",
            "dampak_baris": int(grid["status"].eq("wilayah_belum_terbentuk").sum()),
        },
        {
            "id": "K-008",
            "tanggal": date.today().isoformat(),
            "nim": "124450091",
            "tahap": "panel",
            "seri_kode": "rumah_rusak",
            "keputusan": (
                "Menyatukan alias jenis bencana dan tingkat rumah rusak ke kamus baku; rincian berat/sedang/ringan "
                "dipertahankan hanya pada sumber yang memilikinya, sementara sumber yang hanya memuat total tetap total."
            ),
            "alternatif_ditolak": "Menganggap ketiadaan rincian sebagai nol atau menyamakan total dengan satu tingkat kerusakan.",
            "alasan": (
                "XLSX 2021–2022 memuat tiga tingkat untuk delapan jenis bencana; tabel 2024 tidak memisahkan tingkat; "
                "rekap nasional 2025 memuat rincian dan baris Total yang tidak boleh dihitung ganda."
            ),
            "dampak_baris": len(house_detail),
        },
        {
            "id": "K-009",
            "tanggal": date.today().isoformat(),
            "nim": "124450091",
            "tahap": "validasi",
            "seri_kode": "agregasi_kabupaten_provinsi",
            "keputusan": (
                f"Menguji {len(aggregation)} pasangan wilayah; {len(aggregation) - diff_count} cocok dan "
                f"{diff_count} berbeda. Selisih dipertahankan dan tidak dikoreksi otomatis."
            ),
            "alternatif_ditolak": "Mengganti total provinsi dengan jumlah kabupaten/kota atau memaksa angka agar sama.",
            "alasan": "Sumber dapat berbeda cakupan atau revisi; semua pasangan dan selisih disimpan untuk penelusuran.",
            "dampak_baris": diff_count,
        },
    ]
    decisions = [row for row in base_decisions if row["id"] not in existing_ids]
    missing_start = 10
    for offset, row in enumerate(missing_groups.itertuples(index=False)):
        decision_id = f"K-{missing_start + offset:03d}"
        if decision_id in existing_ids:
            continue
        regions = ", ".join(row.provinsi)
        decisions.append(
            {
                "id": decision_id,
                "tanggal": date.today().isoformat(),
                "nim": "124450091",
                "tahap": "panel",
                "seri_kode": row.seri,
                "keputusan": (
                    f"{row.seri} tahun {int(row.periode)}: {len(row.provinsi)} sel provinsi ditandai "
                    f"kosong, bukan nol. Provinsi terdampak: {regions}."
                ),
                "alternatif_ditolak": "Mengisi sel kosong dengan nol atau menghapus tahun tersebut.",
                "alasan": (
                    "Sumber tingkat provinsi untuk seri-tahun ini tersedia, tetapi nilai/baris provinsi tidak "
                    "tercatat. Status dan barisnya dapat ditelusuri di grid-provinsi-tahap-3.csv."
                ),
                "dampak_baris": len(row.provinsi),
            }
        )
    if decisions:
        with path.open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="ignore")
            writer.writerows(decisions)


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    json_sources = baca_semua_datastore()
    xlsx_sources = baca_semua_xlsx()
    observations_path = REPORTS / "observasi-provinsi-tahap-2.csv"
    if not observations_path.exists():
        raise FileNotFoundError(observations_path)
    observations = pd.read_csv(observations_path)
    grid, summary = build_grid(observations)
    national, national_sources = build_national_observations(json_sources, xlsx_sources)
    availability = build_availability(summary, national_sources, json_sources, xlsx_sources)
    dictionary = build_house_dictionary()
    house_detail = build_house_detail(json_sources, xlsx_sources)
    aggregation = build_aggregation_audit(json_sources, xlsx_sources)

    anomalies_path = REPORTS / "klasifikasi-anomali.csv"
    outlier_count = len(pd.read_csv(anomalies_path)) if anomalies_path.exists() else 0
    grid.to_csv(REPORTS / "grid-provinsi-tahap-3.csv", index=False)
    summary.to_csv(REPORTS / "kelengkapan-panel-per-tahun.csv", index=False)
    national.to_csv(REPORTS / "observasi-nasional-tahap-3.csv", index=False)
    availability.to_csv(REPORTS / "ketersediaan-seri-wilayah-tahap-3.csv", index=False)
    dictionary.to_csv(REPORTS / "kamus-rincian-rumah-rusak.csv", index=False)
    house_detail.to_csv(REPORTS / "rincian-rumah-rusak-harmonisasi.csv", index=False)
    aggregation.to_csv(REPORTS / "uji-agregasi-kabupaten-provinsi.csv", index=False)
    write_report(
        grid,
        summary,
        availability,
        house_detail,
        aggregation,
        len(observations),
        outlier_count,
    )
    append_decisions(grid, house_detail, aggregation)
    missing_cells = int(summary["sel_kosong_grid"].sum())
    print(
        f"Grid={len(grid)}; observasi_provinsi={len(observations)}; "
        f"sel_kosong_grid={missing_cells}; outlier={outlier_count}; "
        f"uji_agregasi={len(aggregation)}"
    )
    print(
        "Status grid:",
        grid["status"].value_counts().sort_index().to_dict(),
    )
    print(
        "Audit agregasi:",
        aggregation["status"].value_counts().sort_index().to_dict(),
    )


if __name__ == "__main__":
    main()
