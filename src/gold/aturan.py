"""Aturan seleksi satu observasi Gold dari baris-barus Silver."""
import csv
import json
import re
from pathlib import Path

import pandas as pd

from src.gold.skema import KODE_NASIONAL, PROVINSI_38_2025, SERI_UTAMA_K23

ROOT = Path(__file__).resolve().parents[2]
LOG_PATH = ROOT / "log-keputusan.csv"
REPORTS = ROOT / "reports"

_LOG_COLUMNS = [
    "id",
    "tanggal",
    "nim",
    "tahap",
    "seri_kode",
    "keputusan",
    "alternatif_ditolak",
    "alasan",
    "dampak_baris",
]
_DETAILS_RUMAH = {
    "total": "total",
    "berat": "berat",
    "rusak berat": "berat",
    "sedang": "sedang",
    "rusak sedang": "sedang",
    "ringan": "ringan",
    "rusak ringan": "ringan",
}


def _detail_indikator(seri, rincian):
    detail = str(rincian).strip().lower()
    if detail == "total":
        return (f"{seri}_total" if seri == "rumah_rusak" else seri, "total")
    if seri == "rumah_rusak" and detail in _DETAILS_RUMAH:
        severity = _DETAILS_RUMAH[detail]
        return f"{seri}_{severity}", "total"
    dimensions = {}
    for pair in detail.split(";"):
        if "=" not in pair:
            return None
        key, value = pair.split("=", 1)
        dimensions[key.strip()] = value.strip()
    disaster = dimensions.get("jenis_bencana")
    severity = _DETAILS_RUMAH.get(dimensions.get("tingkat_kerusakan", ""))
    if set(dimensions).difference({"jenis_bencana", "tingkat_kerusakan"}):
        return None
    if "tingkat_kerusakan" in dimensions and severity is None:
        return None
    if seri == "rumah_rusak":
        if severity:
            indicator = f"{seri}_{severity}"
            return indicator, f"jenis_bencana:{disaster}" if disaster else "total"
        if disaster:
            return f"{seri}_total", f"jenis_bencana:{disaster}"
    elif disaster and not severity:
        return seri, f"jenis_bencana:{disaster}"
    return None


def _snapshot_rank(path):
    """Prioritaskan rilis snapshot terbaru; kompilasi resmi menang pada tanggal sama."""
    text = str(path).lower().replace("\\", "/")
    dates = re.findall(r"20\d{2}-\d{2}-\d{2}", text)
    date = dates[-1] if dates else ""
    if "kompilasi-data-kejadian-dan-dampak-bencana-2025" in text:
        release = 3
    elif "kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024" in text:
        release = 2
    elif "kompilasi" in text:
        release = 1
    else:
        release = 0
    return date, release, str(path).lower()


def _pilih_versi_terbaru(frame, keys):
    if frame.empty:
        return frame.copy(), 0
    ordered = frame.copy()
    ranks = ordered["_berkas_raw"].map(_snapshot_rank)
    ordered["_snapshot_date"] = ranks.map(lambda rank: rank[0])
    ordered["_snapshot_release"] = ranks.map(lambda rank: rank[1])
    ordered = ordered.sort_values(
        keys + ["_snapshot_date", "_snapshot_release", "_berkas_raw"],
        ascending=[True] * len(keys) + [False, False, True],
        kind="mergesort",
    )
    selected = ordered.drop_duplicates(keys, keep="first").drop(
        columns=["_snapshot_date", "_snapshot_release"]
    )
    return selected, len(frame) - len(selected)


def _tahun_tahunan(periode):
    text = str(periode).strip()
    return int(text) if re.fullmatch(r"\d{4}", text) else None


def _flag_tables():
    """Baca tanda Sprint 1 jika laporan tersedia; Silver flags tetap dapat dipakai."""
    classifications_path = REPORTS / "klasifikasi-anomali.csv"
    breaks_path = REPORTS / "uji-patahan-seri.csv"
    classifications = (
        pd.read_csv(classifications_path)
        if classifications_path.exists()
        else pd.DataFrame()
    )
    breaks = pd.read_csv(breaks_path) if breaks_path.exists() else pd.DataFrame()

    province_codes = {
        "".join(name.upper().split()): code
        for code, name in PROVINSI_38_2025.items()
    }
    if not classifications.empty:
        classifications["wilayah_kode"] = classifications["provinsi"].map(
            lambda name: province_codes.get("".join(str(name).upper().split()))
        )
        classifications["periode"] = classifications["periode"].astype(str)
        classifications["flag_outlier"] = classifications["kategori"].eq(
            "outlier asli"
        )
        classifications["flag_patahan"] = classifications["kategori"].eq(
            "patahan seri"
        )
        classifications = classifications.dropna(subset=["wilayah_kode"])
        classifications["wilayah_kode"] = classifications["wilayah_kode"].astype(int)
        classifications = classifications[
            [
                "seri",
                "wilayah_kode",
                "periode",
                "flag_outlier",
                "flag_patahan",
            ]
        ].rename(columns={"seri": "seri_kode"})

    if not breaks.empty:
        breaks = breaks[
            breaks["ambang_patahan_terpenuhi"].astype(str).str.lower().eq("true")
        ].copy()
        breaks["periode"] = breaks["periode_sesudah"].astype(str)
        breaks["wilayah_kode"] = KODE_NASIONAL
        breaks["flag_patahan"] = True
        breaks["flag_outlier"] = False
        breaks = breaks[
            [
                "seri",
                "wilayah_kode",
                "periode",
                "flag_outlier",
                "flag_patahan",
            ]
        ].rename(columns={"seri": "seri_kode"})
    return classifications, breaks


def _pasang_flag(selected, flags=None):
    result = selected.copy()
    has_flags = {"flag_outlier", "flag_patahan"}.issubset(result.columns)
    if flags is None:
        classifications, breaks = _flag_tables()
        flag_parts = [part for part in (classifications, breaks) if not part.empty]
        flags = (
            pd.concat(flag_parts, ignore_index=True)
            if flag_parts
            else pd.DataFrame()
        )
    if not flags.empty:
        national_breaks = flags[
            flags["wilayah_kode"].eq(KODE_NASIONAL)
            & flags["flag_patahan"].fillna(False)
        ]
        if not national_breaks.empty:
            provinces = selected[
                selected["wilayah_kode"].ne(KODE_NASIONAL)
                & selected.set_index(
                    ["seri_kode", "periode"]
                ).index.isin(
                    national_breaks.set_index(["seri_kode", "periode"]).index
                )
            ][["seri_kode", "wilayah_kode", "periode"]].drop_duplicates()
            if not provinces.empty:
                broadcast = provinces.assign(
                    flag_outlier=False,
                    flag_patahan=True,
                )
                flags = pd.concat([flags, broadcast], ignore_index=True)
        keys = ["seri_kode", "wilayah_kode", "periode"]
        flags = flags.groupby(keys, as_index=False)[
            ["flag_outlier", "flag_patahan"]
        ].max()
        result = result.merge(flags, how="left", on=keys, suffixes=("", "_sprint1"))
        for flag in ("flag_outlier", "flag_patahan"):
            source_flag = (
                f"{flag}_sprint1" if flag in selected.columns else flag
            )
            if flag not in selected.columns:
                result[flag] = result[source_flag].fillna(False)
            else:
                result[flag] = result[flag].fillna(False) | result[source_flag].fillna(
                    False
                )
            if source_flag != flag:
                result = result.drop(columns=source_flag)
    elif not has_flags:
        result["flag_outlier"] = pd.NA
        result["flag_patahan"] = pd.NA
    return result


def _gabungkan_rincian(rows, indicator):
    """Agregasikan hanya dimensi jenis bencana; pilih total langsung bila tersedia."""
    direct = rows[rows["_komponen"].eq("total")]
    selected = (
        direct
        if not direct.empty
        else rows[rows["_komponen"].str.startswith("jenis_bencana:", na=False)]
    )
    if selected.empty:
        return None

    flags = {}
    for flag in ("flag_outlier", "flag_patahan"):
        if selected[flag].isna().all():
            flags[flag] = pd.NA
        else:
            flags[flag] = bool(selected[flag].fillna(False).any())
    lineage = (
        selected[["_berkas_raw", "_sha256_raw"]]
        .drop_duplicates()
        .to_dict("records")
    )
    result = selected.iloc[0].to_dict()
    result["nilai"] = selected["nilai"].sum(min_count=1)
    result["_indikator"] = indicator
    result["rincian"] = (
        f"tingkat_kerusakan={indicator.rsplit('_', 1)[-1]}"
        if indicator.startswith("rumah_rusak_")
        and indicator != "rumah_rusak_total"
        else "total"
    )
    result["_lineage"] = json.dumps(lineage, ensure_ascii=False)
    result["_berkas_raw"] = "|".join(item["_berkas_raw"] for item in lineage)
    result["_sha256_raw"] = "|".join(item["_sha256_raw"] for item in lineage)
    result["_source_indices"] = selected.index.tolist()
    result.update(flags)
    return result, set(selected.index)


def _agregasikan_observasi(rows):
    """Kembalikan satu baris per wilayah, periode, dan indikator."""
    output = []
    detail_discarded = 0
    group_keys = ["wilayah_kode", "periode", "seri_kode"]
    for _, group in rows.groupby(group_keys, sort=False, dropna=False):
        series = group["seri_kode"].iloc[0]
        used = set()
        if series != "rumah_rusak":
            combined = _gabungkan_rincian(group, series)
            if combined:
                row, used = combined
                output.append(row)
        else:
            severity_rows = {}
            for severity in ("berat", "sedang", "ringan"):
                indicator = f"rumah_rusak_{severity}"
                selected = group[group["_indikator"].eq(indicator)]
                if selected.empty:
                    continue
                combined = _gabungkan_rincian(selected, indicator)
                if combined:
                    row, source_indices = combined
                    output.append(row)
                    used.update(source_indices)
                    severity_rows[severity] = row

            totals = group[group["_indikator"].eq("rumah_rusak_total")]
            if not totals.empty:
                combined = _gabungkan_rincian(totals, "rumah_rusak_total")
                if combined:
                    row, source_indices = combined
                    output.append(row)
                    used.update(source_indices)
            elif all(level in severity_rows for level in ("berat", "sedang", "ringan")):
                components = [severity_rows[level] for level in ("berat", "sedang", "ringan")]
                row = components[0].copy()
                row["nilai"] = sum(component["nilai"] for component in components)
                row["_indikator"] = "rumah_rusak_total"
                row["rincian"] = "total"
                lineage = sorted(
                    {
                        (source["_berkas_raw"], source["_sha256_raw"])
                        for component in components
                        for source in json.loads(component["_lineage"])
                    }
                )
                row["_lineage"] = json.dumps(
                    [
                        {"_berkas_raw": path, "_sha256_raw": checksum}
                        for path, checksum in lineage
                    ],
                    ensure_ascii=False,
                )
                row["_berkas_raw"] = "|".join(path for path, _ in lineage)
                row["_sha256_raw"] = "|".join(checksum for _, checksum in lineage)
                for flag in ("flag_outlier", "flag_patahan"):
                    row[flag] = any(
                        pd.notna(component[flag]) and bool(component[flag])
                        for component in components
                    )
                output.append(row)
                used.update(index for component in severity_rows.values()
                            for index in component["_source_indices"])
        detail_discarded += len(set(group.index) - used)

    result = pd.DataFrame(output)
    if "_source_indices" in result:
        result = result.drop(columns="_source_indices")
    if result.duplicated(["wilayah_kode", "periode", "_indikator"]).any():
        raise ValueError("Agregasi Gold menghasilkan kunci indikator ganda.")
    return result, detail_discarded


def _write_decisions(counts):
    rows = []
    if LOG_PATH.exists():
        with LOG_PATH.open("r", encoding="utf-8-sig", newline="") as source:
            reader = csv.DictReader(source)
            rows = list(reader)
            columns = reader.fieldnames or _LOG_COLUMNS
    else:
        columns = _LOG_COLUMNS

    definitions = [
        {
            "id": "K-101",
            "seri_kode": "semua seri Gold",
            "keputusan": "Untuk kunci wilayah × periode × indikator yang bersumber dari beberapa snapshot, pakai snapshot dengan tanggal terbaru; jika tanggal sama, prioritaskan kompilasi BNPB terbaru, lalu urutkan _berkas_raw secara leksikografis sebagai pemutus seri.",
            "alternatif_ditolak": "Menjumlahkan snapshot, memilih angka terbesar, atau menghapus revisi tanpa aturan.",
            "alasan": "Snapshot adalah versi/revisi observasi yang sama, bukan rincian tambahan. Pilihan satu versi tetap dapat ditelusuri lewat _berkas_raw dan _sha256_raw.",
        },
        {
            "id": "K-102",
            "seri_kode": "14 seri utama",
            "keputusan": "Panel provinsi memakai total sumber bila tersedia; bila hanya ada rincian jenis_bencana, nilai rincian dijumlahkan sekali untuk indikator total. rumah_rusak juga mempertahankan berat/sedang/ringan sebagai indikator terpisah, dan total hanya diturunkan dari tiga tingkat bila ketiganya tersedia. Rincian jenis bencana tetap di Silver.",
            "alternatif_ditolak": "Menjumlahkan baris total dengan rinciannya atau menganggap rincian yang tidak tersedia sebagai nol.",
            "alasan": "Mencegah hitung ganda, tetap membentuk total dari rincian aditif tanpa nilai total, serta menjaga tingkat kerusakan rumah; nilai kerugian dan nilai kerusakan tetap dua seri berbeda.",
        },
        {
            "id": "K-103",
            "seri_kode": "periode panel provinsi",
            "keputusan": "Panel provinsi tahap ini hanya berisi periode tahunan kanonik 2010–2025. Semester dan bulan tidak dijumlahkan atau dipaksakan menjadi tahun; observasi sub-tahunan tetap di Silver. Tabel nasional mempertahankan periode aslinya.",
            "alternatif_ditolak": "Menjumlahkan sub-periode tanpa bukti kelengkapan cakupan atau menggandakan satu nilai tahunan ke setiap sub-periode.",
            "alasan": "Frekuensi observasi tidak dicampur; data sub-tahunan tetap dapat digunakan pada analisis dengan frekuensi yang sesuai.",
        },
        {
            "id": "K-104",
            "seri_kode": "nilai_kerugian; nilai_kerusakan",
            "keputusan": "Simpan nilai rupiah nominal dan tambahkan transformasi log1p untuk analisis; nilai tidak disesuaikan dengan inflasi karena indeks harga dan tahun dasar yang sesuai belum ditetapkan.",
            "alternatif_ditolak": "Menggabungkan kerugian dengan kerusakan atau menyajikan nilai nominal seolah-olah sudah riil.",
            "alasan": "Kerugian dan kerusakan adalah konsep terpisah. log1p mengurangi rentang skala tanpa menghapus nilai asli atau mengklaim daya beli antarwaktu yang belum dihitung.",
        },
        {
            "id": "K-105",
            "seri_kode": "semua seri Gold",
            "keputusan": "Pertahankan nilai dan teruskan flag outlier serta patahan dari klasifikasi Sprint 1 ke indikator Gold; flag tidak menjadi alasan untuk menghapus, mengubah, atau mengimputasi nilai.",
            "alternatif_ditolak": "Menghapus outlier, menghaluskan patahan, atau menghilangkan penanda saat membentuk Gold.",
            "alasan": "Observasi ekstrem dan perubahan seri yang teridentifikasi tetap dapat diaudit dan dipertimbangkan saat analisis.",
        },
    ]
    by_id = {row.get("id"): row for row in rows}
    for rule in definitions:
        row = {
            "id": rule["id"],
            "tanggal": "2026-11-24",
            "nim": "124450048",
            "tahap": "gold",
            "seri_kode": rule["seri_kode"],
            "keputusan": rule["keputusan"],
            "alternatif_ditolak": rule["alternatif_ditolak"],
            "alasan": rule["alasan"],
            "dampak_baris": int(counts[rule["id"]]),
        }
        by_id[rule["id"]] = row
    rows = list(by_id.values())
    with LOG_PATH.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def pilih_observasi_gold(silver, flags=None):
    """Pilih baris Gold dan kembalikan tabel provinsi/nasional beserta hitungan eksklusi."""
    required = {
        "seri_kode",
        "wilayah_kode",
        "nama_wilayah",
        "periode",
        "jenis_periode",
        "rincian",
        "nilai",
        "_berkas_raw",
        "_sha256_raw",
    }
    missing = required.difference(silver.columns)
    if missing:
        raise ValueError(f"Kolom Silver wajib tidak ada: {sorted(missing)}")

    data = silver.copy()
    series = set(SERI_UTAMA_K23)
    candidates = data[data["seri_kode"].isin(series)].copy()
    decoded = candidates.apply(
        lambda row: _detail_indikator(row["seri_kode"], row["rincian"]),
        axis=1,
    )
    candidates["_indikator"] = decoded.map(
        lambda value: value[0] if value is not None else None
    )
    candidates["_komponen"] = decoded.map(
        lambda value: value[1] if value is not None else None
    )
    keep_detail = candidates[candidates["_indikator"].notna()].copy()
    detail_excluded = len(candidates) - len(keep_detail)

    national_mask = keep_detail["wilayah_kode"].eq(KODE_NASIONAL) | (
        keep_detail["nama_wilayah"].astype(str).str.upper().eq("INDONESIA")
    )
    provincial = keep_detail[~national_mask].copy()
    national_main = keep_detail[national_mask].copy()
    provincial["periode"] = provincial["periode"].astype(str)
    annual_years = provincial["periode"].map(_tahun_tahunan)
    annual_mask = (
        provincial["jenis_periode"].eq("tahun")
        & annual_years.between(2010, 2025)
    )
    period_excluded = int((~annual_mask).sum())
    provincial = provincial[annual_mask].copy()
    provincial["tahun"] = annual_years[annual_mask].astype(int)

    provincial, provincial_snapshot_excluded = _pilih_versi_terbaru(
        provincial,
        ["wilayah_kode", "periode", "_indikator", "_komponen"],
    )
    national_main, national_snapshot_excluded = _pilih_versi_terbaru(
        national_main,
        ["wilayah_kode", "periode", "_indikator", "_komponen"],
    )

    provincial = _pasang_flag(provincial, flags)
    national_main = _pasang_flag(national_main, flags)
    provincial, provincial_detail_excluded = _agregasikan_observasi(provincial)
    national_main, national_detail_excluded = _agregasikan_observasi(national_main)

    other_national = data[
        (data["wilayah_kode"].eq(KODE_NASIONAL)
         | data["nama_wilayah"].astype(str).str.upper().eq("INDONESIA"))
        & ~data["seri_kode"].isin(series)
    ].copy()
    if not other_national.empty:
        other_national["_indikator"] = other_national.apply(
            lambda row: (
                row["seri_kode"]
                if str(row["rincian"]).strip().lower() == "total"
                else f'{row["seri_kode"]}_{str(row["rincian"]).strip().lower()}'
            ),
            axis=1,
        )
        other_national["_komponen"] = "langsung"
        other_national, other_snapshot_excluded = _pilih_versi_terbaru(
            other_national,
            ["wilayah_kode", "periode", "_indikator", "_komponen"],
        )
        other_national = _pasang_flag(other_national, flags)
        other_national["_lineage"] = other_national.apply(
            lambda row: json.dumps(
                [
                    {
                        "_berkas_raw": row["_berkas_raw"],
                        "_sha256_raw": row["_sha256_raw"],
                    }
                ],
                ensure_ascii=False,
            ),
            axis=1,
        )
    else:
        other_snapshot_excluded = 0

    national = pd.concat(
        [national_main, other_national], ignore_index=True, sort=False
    ).rename(columns={"_indikator": "indikator"})
    detail_excluded += provincial_detail_excluded + national_detail_excluded
    provincial = provincial.drop(columns=["_komponen"], errors="ignore")
    national = national.drop(columns=["_komponen"], errors="ignore")
    counts = {
        "K-101": provincial_snapshot_excluded
        + national_snapshot_excluded
        + other_snapshot_excluded,
        "K-102": detail_excluded,
        "K-103": period_excluded,
        "K-104": 0,
        "K-105": 0,
    }
    _write_decisions(counts)
    return provincial, national, counts
