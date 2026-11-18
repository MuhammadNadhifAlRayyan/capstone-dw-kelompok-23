"""Profil ketersediaan WDI EN.CLC.MDAT.ZS dan irisan periode dengan seri BNPB."""

from pathlib import Path
import re

import pandas as pd

from src.ekstraksi.baca_wdi import baca_semua_wdi, baca_wdi_data
from src.gold.skema import SERI_UTAMA_K23


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
INDICATOR = "EN.CLC.MDAT.ZS"
RINCIAN_UTAMA = {
    "kejadian": "Provinsi; jumlah kejadian, tersedia rincian jenis bencana",
    "rumah_rusak": "Provinsi; tingkat kerusakan dan jenis bencana",
    "rumah_terendam": "Provinsi; jumlah rumah terendam",
    "fasyankes_rusak": "Provinsi; fasilitas kesehatan rusak",
    "satuan_pendidikan_rusak": "Provinsi; satuan pendidikan rusak",
    "jembatan_rusak": "Provinsi; jembatan rusak",
    "kantor_rusak": "Provinsi; kantor rusak",
    "rumah_ibadat_rusak": "Provinsi; rumah ibadat rusak",
    "kios_toko_rusak": "Provinsi; kios/toko rusak",
    "pabrik_rusak": "Provinsi; pabrik rusak",
    "luas_sawah_rusak": "Provinsi pada definisi seri; hektare rusak",
    "luas_lahan_kebun_hutan_rusak": "Provinsi pada definisi seri; hektare rusak",
    "nilai_kerugian": "Provinsi; nilai kerugian",
    "nilai_kerusakan": "Provinsi; nilai kerusakan",
}


def _read_wdi_profile():
    observations = baca_wdi_data()
    indonesia = observations[
        observations["country_id"].astype(str).str.upper().eq("IDN")
        | observations["country_value"].astype(str).str.casefold().eq("indonesia")
    ].copy()
    if indonesia.empty:
        raise ValueError(f"Tidak ada observasi Indonesia untuk indikator {INDICATOR}.")

    non_null = indonesia[pd.to_numeric(indonesia["value"], errors="coerce").notna()].copy()
    if non_null.empty:
        raise ValueError(f"Tidak ada nilai teramati untuk indikator {INDICATOR} di Indonesia.")

    metadata_frames = [
        frame
        for path, frame in baca_semua_wdi().items()
        if "metadata" in path and "id" in frame.columns
    ]
    metadata = pd.concat(metadata_frames, ignore_index=True)
    metadata = metadata[metadata["id"].astype(str).eq(INDICATOR)]
    if metadata.empty:
        raise ValueError(f"Metadata indikator {INDICATOR} tidak ditemukan.")
    indicator_name = str(metadata.iloc[0]["name"])
    period = re.search(r"average\s+(\d{4})-(\d{4})", indicator_name, flags=re.IGNORECASE)
    if not period:
        raise ValueError(f"Tidak dapat membaca periode konseptual dari nama: {indicator_name}")
    conceptual_start, conceptual_end = map(int, period.groups())
    available_years = sorted(pd.to_numeric(non_null["date"], errors="raise").astype(int).unique())
    api_years = sorted(pd.to_numeric(indonesia["date"], errors="raise").astype(int).unique())
    value = pd.to_numeric(non_null["value"], errors="raise")
    unit_raw = metadata.iloc[0].get("unit")
    unit = (
        str(unit_raw).strip()
        if pd.notna(unit_raw) and str(unit_raw).strip()
        else "% populasi (dinyatakan pada nama indikator; kolom unit API kosong)"
    )
    source_note = str(metadata.iloc[0].get("sourceNote", ""))
    return {
        "indicator_name": indicator_name,
        "conceptual_start": conceptual_start,
        "conceptual_end": conceptual_end,
        "available_years": available_years,
        "api_start": min(api_years),
        "api_end": max(api_years),
        "api_record_count": len(indonesia),
        "non_null_count": len(non_null),
        "value": float(value.iloc[0]) if len(value) == 1 else None,
        "unit": unit,
        "unit_raw": "" if pd.isna(unit_raw) else str(unit_raw),
        "country": str(non_null.iloc[0]["country_value"]),
        "source_note": source_note,
        "metadata_sources": sorted(metadata["source.value"].dropna().astype(str).unique())
        if "source.value" in metadata
        else [],
    }


def _period(start, end):
    return f"{start}-{end}"


def _build_tables(profile):
    availability = pd.DataFrame(
        [
            {
                "sumber": "WDI",
                "seri": INDICATOR,
                "nama_indikator": profile["indicator_name"],
                "periode_konseptual": _period(
                    profile["conceptual_start"], profile["conceptual_end"]
                )
                + " (rata-rata)",
                "tahun_label_dengan_nilai": ", ".join(map(str, profile["available_years"])),
                "rentang_tahun_API": _period(profile["api_start"], profile["api_end"]),
                "jumlah_record_API": profile["api_record_count"],
                "jumlah_nilai_non_null": profile["non_null_count"],
                "negara": profile["country"],
                "rincian_geografis": "Indonesia saja pada snapshot; agregat nasional",
                "rincian_demografis": "Tidak ada rincian jenis kelamin, umur, urban/rural, atau kelompok penduduk",
                "rincian_jenis_bencana": "Gabungan kekeringan, banjir, dan suhu ekstrem",
                "satuan": profile["unit"],
                "unit_raw_API": profile["unit_raw"],
                "nilai_non_null": profile["value"],
                "sumber_metadata": "; ".join(profile["metadata_sources"]),
            }
        ]
    )

    comparison_rows = []
    for series, definition in SERI_UTAMA_K23.items():
        start, end = definition["rentang"]
        intersection_start = max(start, profile["conceptual_start"])
        intersection_end = min(end, profile["conceptual_end"])
        overlap = (
            ", ".join(map(str, range(intersection_start, intersection_end + 1)))
            if intersection_start <= intersection_end
            else "Tidak ada"
        )
        comparison_rows.append(
            {
                "seri_utama": series,
                "periode_katalog_seri_utama": _period(start, end),
                "satuan_seri_utama": definition["satuan"],
                "rincian_seri_utama": RINCIAN_UTAMA[series],
                "periode_konseptual_WDI": _period(
                    profile["conceptual_start"], profile["conceptual_end"]
                )
                + " (rata-rata)",
                "tahun_label_nilai_WDI": ", ".join(map(str, profile["available_years"])),
                "tahun_beririsan": overlap,
                "rincian_WDI_kandidat": "Total Indonesia; tidak terdisagregasi",
                "status_keterbandingan": "Konteks saja; tidak sebanding langsung",
                "alasan": (
                    "Tidak ada irisan periode; WDI mengukur persentase penduduk terdampak, "
                    "sedangkan seri BNPB mengukur "
                    f"{definition['satuan']} pada rincian provinsi."
                ),
            }
        )
    return availability, pd.DataFrame(comparison_rows)


def _write_report(profile, availability, comparison):
    path = REPORTS / "tahap-2-ketersediaan-pembanding-wdi.md"
    years = ", ".join(map(str, profile["available_years"]))
    value = "—" if profile["value"] is None else f'{profile["value"]:.5f}'
    lines = [
        "# Tahap 2 — Ketersediaan seri pembanding WDI",
        "",
        f"## `{INDICATOR}`",
        "",
        f"- **Nama:** {profile['indicator_name']}",
        f"- **Periode yang dimaksud indikator:** "
        f"{profile['conceptual_start']}–{profile['conceptual_end']} (rata-rata periode), "
        "bukan deret nilai tahunan.",
        f"- **Observasi Indonesia non-null:** {years} (nilai {value}). "
        f"Snapshot memuat {profile['api_record_count']} baris tahun API "
        f"{profile['api_start']}–{profile['api_end']}, tetapi hanya "
        f"{profile['non_null_count']} nilai non-null.",
        "- **Satuan:** % populasi menurut nama indikator; kolom `unit` API kosong.",
        "- **Rincian tersedia:** Indonesia/agregat nasional. Tidak ada pemisahan provinsi, "
        "jenis kelamin, umur, atau kelompok urban/rural. Indikator menggabungkan dampak "
        "kekeringan, banjir, dan suhu ekstrem.",
        "",
        "Metadata menjelaskan penduduk terdampak sebagai penduduk yang terluka, kehilangan "
        "tempat tinggal, atau membutuhkan bantuan segera. Persentase adalah rata-rata untuk "
        "periode yang tercantum, dihitung dari jumlah terdampak dibagi jumlah populasi tahunan "
        "selama periode tersebut.",
        "",
        "## Ketersediaan dan keterbandingan dengan seri utama",
        "",
        "| Seri utama | Periode seri utama | Rincian seri utama | Satuan | Periode WDI | Tahun beririsan | Rincian WDI kandidat | Status dan alasan |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in comparison.to_dict("records"):
        lines.append(
            f'| `{row["seri_utama"]}` | {row["periode_katalog_seri_utama"]} | '
            f'{row["rincian_seri_utama"]} | {row["satuan_seri_utama"]} | '
            f'{row["periode_konseptual_WDI"]} | {row["tahun_beririsan"]} | '
            f'{row["rincian_WDI_kandidat"]} | {row["status_keterbandingan"]}. '
            f'{row["alasan"]} |'
        )
    lines.extend(
        [
            "",
            "Untuk semua seri utama, irisan tahun adalah **tidak ada**: periode BNPB dimulai "
            "pada 2010 atau sesudahnya, sedangkan indikator WDI merangkum 1990–2009. Label "
            "API `2009` menandai satu nilai ringkasan itu dan tidak menjadikannya pengamatan "
            "tahunan 2009 yang sebanding.",
            "",
            "## Rekomendasi untuk Tahap 6",
            "",
            "Rincian WDI yang tersedia hanya **total nasional Indonesia**. Rincian ini dapat "
            "dipertahankan sebagai konteks, tetapi tidak ada rincian yang sebanding untuk "
            "rekonsiliasi numerik dengan 14 seri utama: konsep, satuan/granularitas, dan "
            "periode tidak cocok. Jangan menghitung selisih atau menggabungkannya ke panel "
            "provinsi.",
            "",
            "Tabel terstruktur: [`ketersediaan-wdi-en-clc-mdat-zs.csv`](ketersediaan-wdi-en-clc-mdat-zs.csv) "
            "dan [`irisan-wdi-seri-utama.csv`](irisan-wdi-seri-utama.csv).",
            "",
            "## Sumber",
            "",
            "Data observasi WDI `kelompok-01-hal-01.json`; metadata indikator dari "
            "`sumber2_indikator.json` dan `sumber46_indikator.json` pada snapshot 2026-10-20. "
            "Kedua metadata menyajikan definisi indikator yang sama.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    profile = _read_wdi_profile()
    availability, comparison = _build_tables(profile)
    availability.to_csv(REPORTS / "ketersediaan-wdi-en-clc-mdat-zs.csv", index=False)
    comparison.to_csv(REPORTS / "irisan-wdi-seri-utama.csv", index=False)
    _write_report(profile, availability, comparison)
    print(
        f"{INDICATOR}: {profile['non_null_count']} nilai non-null "
        f"({', '.join(map(str, profile['available_years']))}); "
        f"{len(comparison)} seri utama, irisan periode tidak ada."
    )


if __name__ == "__main__":
    main()
