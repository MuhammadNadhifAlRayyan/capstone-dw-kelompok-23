"""Profil statistik dan calon anomali BNPB untuk Tahap 2."""

from pathlib import Path
import re

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.ekstraksi.baca_datastore import baca_semua_datastore
from src.ekstraksi.baca_xlsx import baca_semua_xlsx
from src.gold.skema import PROVINSI_38_2025


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "gambar"
SERIES = [
    "kejadian",
    "rumah_rusak",
    "rumah_terendam",
    "fasyankes_rusak",
    "satuan_pendidikan_rusak",
    "jembatan_rusak",
    "kantor_rusak",
    "rumah_ibadat_rusak",
    "kios_toko_rusak",
    "pabrik_rusak",
    "luas_sawah_rusak",
    "luas_lahan_kebun_hutan_rusak",
    "nilai_kerugian",
    "nilai_kerusakan",
]
PROVINCES = {
    "".join(name.upper().split()): name for name in PROVINSI_38_2025.values()
}
DISASTER_TYPES = [
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
YEARLY_PROPOSAL_FILES = {
    "36ec22b9": 2015,
    "520b34fd": 2016,
    "e2c2ed75": 2017,
    "b1aa4eb5": 2018,
    "bcf4f458": 2019,
    "c013b8a0": 2020,
    "53f8dc76": 2021,
    "cf6d0735": 2022,
    "a66a93b0": 2023,
    "03d7c28f": 2024,
}


def _province_name(value):
    if pd.isna(value):
        return None
    return PROVINCES.get("".join(str(value).upper().split()))


def _number(values):
    return pd.to_numeric(values, errors="coerce")


def _year(value):
    if pd.isna(value):
        return None
    match = re.search(r"\b(20\d{2})\b", str(value))
    return int(match.group(1)) if match else None


def _exact_year(value):
    if pd.isna(value):
        return None
    text = str(value).strip()
    match = re.fullmatch(r"(20\d{2})(?:\.0+)?", text)
    return int(match.group(1)) if match else None


def _append_rows(observations, series, frame, province_col, year, value):
    if province_col not in frame.columns:
        return
    rows = pd.DataFrame(
        {
            "seri": series,
            "provinsi": frame[province_col].map(_province_name),
            "periode": year,
            "nilai": value,
        }
    )
    rows = rows.dropna(subset=["provinsi", "nilai"])
    if not rows.empty:
        observations.append(rows)


def _numeric_total(frame, columns):
    present = [column for column in columns if column in frame.columns]
    if not present:
        return pd.Series(np.nan, index=frame.index, dtype=float)
    return frame[present].apply(_number).sum(axis=1, min_count=1)


def _aggregate(observations):
    if not observations:
        return pd.DataFrame(columns=["seri", "provinsi", "periode", "nilai"])
    raw = pd.concat(observations, ignore_index=True)
    raw["periode"] = pd.to_numeric(raw["periode"], errors="coerce")
    raw["nilai"] = pd.to_numeric(raw["nilai"], errors="coerce")
    raw = raw.dropna(subset=["seri", "provinsi", "periode", "nilai"])
    raw["periode"] = raw["periode"].astype(int)
    # Multiple disaster-type rows or proposal records are components of one province-year total.
    return (
        raw.groupby(["seri", "provinsi", "periode"], as_index=False)["nilai"]
        .sum(min_count=1)
        .sort_values(["seri", "periode", "provinsi"])
        .reset_index(drop=True)
    )


def collect_observations():
    """Read only provincial records; keep national and district records out of the panel."""
    observations = []
    monetary_period_notes = {"ambiguous": 0, "outside_scope": 0}
    datastore = baca_semua_datastore()
    xlsx = baca_semua_xlsx()

    kejadian = next(
        (df for name, df in datastore.items() if Path(name).stem.startswith("5dfcae7e")),
        None,
    )
    if kejadian is not None:
        province_col = "Nama Provinsi" if "Nama Provinsi" in kejadian else "Provinsi"
        year_columns = []
        for column in kejadian.columns:
            year = _year(column)
            if year and str(column).replace(".0", "").isdigit():
                year_columns.append((column, year))
        for column, year in year_columns:
            _append_rows(
                observations, "kejadian", kejadian, province_col, year, _number(kejadian[column])
            )

    province_metrics_2024 = {
        "471f71cb": "rumah_rusak",
        "26858365": "fasyankes_rusak",
        "76c8231d": "satuan_pendidikan_rusak",
        "ad86fca8": "jembatan_rusak",
        "5f69273d": "pabrik_rusak",
    }
    for prefix, series in province_metrics_2024.items():
        frame = next(
            (df for name, df in datastore.items() if Path(name).stem.startswith(prefix)),
            None,
        )
        if frame is None:
            continue
        province_col = "Provinsi" if "Provinsi" in frame else "Nama Provinsi"
        total = _numeric_total(frame, DISASTER_TYPES)
        _append_rows(observations, series, frame, province_col, 2024, total)

    province_metrics_2024_xlsx = {
        "742bb9f9": "kantor_rusak",
        "5f3bdd4d": "rumah_ibadat_rusak",
        "cbc56396": "kios_toko_rusak",
    }
    for prefix, series in province_metrics_2024_xlsx.items():
        frame = next(
            (df for name, df in xlsx.items() if Path(name).name.startswith(prefix)),
            None,
        )
        if frame is None:
            continue
        _append_rows(
            observations,
            series,
            frame,
            "Provinsi",
            2024,
            _numeric_total(frame, DISASTER_TYPES),
        )

    year_files = [
        (name, frame)
        for name, frame in xlsx.items()
        if "per-provinsi.xlsx" in name.lower()
        and ("tahun-2021" in name.lower() or "tahun-2022" in name.lower())
    ]
    for name, frame in year_files:
        year = 2021 if "tahun-2021" in name.lower() else 2022
        metrics = {
            "rumah_rusak": [
                "Kerusakan - Rumah Rusak Berat",
                "Kerusakan - Rumah Rusak Sedang",
                "Kerusakan - Rumah Rusak Ringan",
            ],
            "rumah_terendam": ["Kerusakan - Rumah Terendam"],
            "fasyankes_rusak": ["Kerusakan - Sarana Kesehatan"],
            "satuan_pendidikan_rusak": ["Kerusakan - Sarana Pendidikan"],
            "jembatan_rusak": ["Kerusakan - Jembatan"],
            "kantor_rusak": ["Kerusakan - Perkantoran"],
            "rumah_ibadat_rusak": ["Kerusakan - Sarana Peribadatan"],
        }
        for series, columns in metrics.items():
            _append_rows(
                observations,
                series,
                frame,
                "Provinsi",
                year,
                _numeric_total(frame, columns),
            )

    for name, frame in xlsx.items():
        lower_name = Path(name).name.lower()
        if "jumlah-kejadian-bencana-menurut-provinsi-2025.xlsx" in lower_name:
            _append_rows(
                observations,
                "kejadian",
                frame,
                "Provinsi",
                2025,
                _numeric_total(frame, DISASTER_TYPES),
            )
        elif "jumlah-rumah-rusak-akibat-bencana-menurut-provinsi-2025.xlsx" in lower_name:
            _append_rows(
                observations,
                "rumah_rusak",
                frame,
                "Provinsi",
                2025,
                _numeric_total(frame, DISASTER_TYPES),
            )

    for name, frame in datastore.items():
        prefix = Path(name).stem[:8]
        if prefix not in YEARLY_PROPOSAL_FILES:
            continue
        fallback_year = YEARLY_PROPOSAL_FILES[prefix]
        if not {"Provinsi", "Nilai Kerugian", "Nilai Kerusakan"}.issubset(frame.columns):
            continue
        year_values = (
            frame["Tahun Kejadian"].map(_exact_year)
            if "Tahun Kejadian" in frame
            else None
        )
        if year_values is not None:
            monetary_period_notes["ambiguous"] += int(
                (frame["Tahun Kejadian"].notna() & year_values.isna()).sum()
            )
            monetary_period_notes["outside_scope"] += int(
                (year_values.notna() & ~year_values.between(2015, 2024)).sum()
            )
        for series, column in (
            ("nilai_kerugian", "Nilai Kerugian"),
            ("nilai_kerusakan", "Nilai Kerusakan"),
        ):
            years = (
                year_values
                if year_values is not None
                else pd.Series(fallback_year, index=frame.index)
            )
            years = years.where(years.between(2015, 2024))
            _append_rows(
                observations,
                series,
                frame,
                "Provinsi",
                years,
                _number(frame[column]),
            )

    return _aggregate(observations), monetary_period_notes


def _summary_tables(data):
    series_rows = []
    province_rows = []
    anomaly_frames = []
    thresholds = {}

    for series in SERIES:
        subset = data[data["seri"] == series]
        values = subset["nilai"].dropna()
        if values.empty:
            thresholds[series] = (np.nan, np.nan, np.nan, np.nan)
            series_rows.append(
                {
                    "seri": series,
                    "n": 0,
                    "n_provinsi": 0,
                    "n_periode": 0,
                    "periode_awal": np.nan,
                    "periode_akhir": np.nan,
                    "mean": np.nan,
                    "median": np.nan,
                    "std": np.nan,
                    "min": np.nan,
                    "q1": np.nan,
                    "q3": np.nan,
                    "max": np.nan,
                    "batas_bawah_iqr": np.nan,
                    "batas_atas_iqr": np.nan,
                    "n_calon_anomali": 0,
                }
            )
            continue

        q1, q3 = values.quantile([0.25, 0.75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        thresholds[series] = (q1, q3, lower, upper)
        flagged = subset[(subset["nilai"] < lower) | (subset["nilai"] > upper)].copy()
        flagged["batas_bawah_iqr"] = lower
        flagged["batas_atas_iqr"] = upper
        flagged["alasan"] = np.where(
            flagged["nilai"] > upper,
            "nilai di atas pagar atas IQR (Q3 + 1,5 x IQR)",
            "nilai di bawah pagar bawah IQR (Q1 - 1,5 x IQR)",
        )
        anomaly_frames.append(flagged)

        series_rows.append(
            {
                "seri": series,
                "n": len(values),
                "n_provinsi": subset["provinsi"].nunique(),
                "n_periode": subset["periode"].nunique(),
                "periode_awal": int(subset["periode"].min()),
                "periode_akhir": int(subset["periode"].max()),
                "mean": values.mean(),
                "median": values.median(),
                "std": values.std(),
                "min": values.min(),
                "q1": q1,
                "q3": q3,
                "max": values.max(),
                "batas_bawah_iqr": lower,
                "batas_atas_iqr": upper,
                "n_calon_anomali": len(flagged),
            }
        )

        for province, group in subset.groupby("provinsi"):
            province_values = group["nilai"]
            province_rows.append(
                {
                    "seri": series,
                    "provinsi": province,
                    "n": len(province_values),
                    "periode_awal": int(group["periode"].min()),
                    "periode_akhir": int(group["periode"].max()),
                    "mean": province_values.mean(),
                    "median": province_values.median(),
                    "std": province_values.std(),
                    "min": province_values.min(),
                    "max": province_values.max(),
                    "n_calon_anomali": int(
                        ((province_values < lower) | (province_values > upper)).sum()
                    ),
                }
            )

    anomalies = (
        pd.concat(anomaly_frames, ignore_index=True)
        if anomaly_frames
        else pd.DataFrame(
            columns=[
                "seri",
                "provinsi",
                "periode",
                "nilai",
                "batas_bawah_iqr",
                "batas_atas_iqr",
                "alasan",
            ]
        )
    )
    return (
        pd.DataFrame(series_rows),
        pd.DataFrame(province_rows),
        anomalies.sort_values(["seri", "periode", "provinsi"]).reset_index(drop=True),
        thresholds,
    )


def _make_charts(data, anomalies):
    FIGURES.mkdir(parents=True, exist_ok=True)
    for series in SERIES:
        subset = data[data["seri"] == series]
        flags = anomalies[anomalies["seri"] == series]
        fig, (box_ax, time_ax) = plt.subplots(1, 2, figsize=(14, 5.5))
        fig.suptitle(series.replace("_", " ").title(), fontsize=14, fontweight="bold")
        if subset.empty:
            message = "Tidak ada observasi tingkat provinsi pada snapshot data yang tersedia."
            for ax in (box_ax, time_ax):
                ax.text(0.5, 0.5, message, ha="center", va="center", wrap=True)
                ax.set_axis_off()
        else:
            years = sorted(subset["periode"].unique())
            box_ax.boxplot(
                [subset.loc[subset["periode"] == year, "nilai"].values for year in years],
                tick_labels=[str(year) for year in years],
                showfliers=True,
            )
            box_ax.set_title("Sebaran nilai antarprovinsi per tahun")
            box_ax.set_xlabel("Periode")
            box_ax.set_ylabel("Nilai (data mentah)")
            box_ax.tick_params(axis="x", rotation=45)
            box_ax.grid(axis="y", alpha=0.25)

            for _, group in subset.groupby("provinsi"):
                time_ax.plot(group["periode"], group["nilai"], color="#9aa0a6", alpha=0.35, lw=0.8)
            medians = subset.groupby("periode")["nilai"].median()
            time_ax.plot(
                medians.index,
                medians.values,
                color="#1769aa",
                marker="o",
                lw=2,
                label="Median provinsi",
            )
            if not flags.empty:
                time_ax.scatter(
                    flags["periode"],
                    flags["nilai"],
                    color="#c62828",
                    marker="*",
                    s=70,
                    label="Calon anomali IQR",
                    zorder=4,
                )
            time_ax.set_title("Deret waktu provinsi dan median")
            time_ax.set_xlabel("Periode")
            time_ax.set_ylabel("Nilai (data mentah)")
            time_ax.grid(alpha=0.25)
            time_ax.legend()
            if series in {"nilai_kerugian", "nilai_kerusakan"}:
                box_ax.set_yscale("symlog", linthresh=1)
                time_ax.set_yscale("symlog", linthresh=1)
                box_ax.set_ylabel("Nilai rupiah (skala symlog)")
                time_ax.set_ylabel("Nilai rupiah (skala symlog)")
        fig.tight_layout(rect=(0, 0, 1, 0.93))
        fig.savefig(FIGURES / f"{series}.png", dpi=150, bbox_inches="tight")
        plt.close(fig)


def _write_report(series_summary, anomalies, monetary_period_notes):
    report_path = REPORTS / "tahap-2-profil-anomali.md"
    lines = [
        "# Tahap 2 — Profil deskriptif dan calon anomali",
        "",
        "Analisis menggunakan data mentah yang tersedia pada snapshot repo; belum menjalankan",
        "pembersihan atau mengubah nilai. Hanya observasi berlabel provinsi yang dianalisis.",
        "Data level Indonesia dan kabupaten/kota dikecualikan agar tidak tercampur dengan",
        "observasi provinsi. Beberapa indikator hanya tersedia untuk sejumlah tahun pada sumber",
        "yang ada; statistik bukan klaim bahwa rentang tahun tersebut lengkap.",
        "",
        "Jalankan ulang dari akar repo dengan `python -m src.analisis_tahap2`.",
        "",
        "## Metode",
        "",
        "- Statistik mencakup n, provinsi/periode teramati, mean, median, simpangan baku, kuartil,",
        "  minimum, dan maksimum. Pengamatan dengan beberapa baris jenis bencana/proposal",
        "  dijumlahkan pada tingkat provinsi-periode untuk membentuk satu observasi.",
        "- Calon anomali ditandai menggunakan pagar IQR per seri pada gabungan observasi",
        "  provinsi-periode: di bawah Q1 − 1,5×IQR atau di atas Q3 + 1,5×IQR. Ini hanya",
        "  penanda eksploratif; nilai tidak dihapus atau dianggap salah.",
        "- Nilai kerugian/kerusakan diagregasi per provinsi dan tahun kejadian yang tercatat.",
        "  Baris dengan rentang tahun kejadian, bukan satu tahun, tidak dialokasikan agar tidak",
        "  membuat pembagian nilai yang tidak didukung sumber. Dataset berasal dari proposal",
        "  RRRP, bukan pencatatan menyeluruh seluruh dampak ekonomi aktual.",
        f"  Sebanyak {monetary_period_notes['ambiguous']} baris dengan periode tidak tunggal/"
        "tidak terbaca dan "
        f"{monetary_period_notes['outside_scope']} baris dengan tahun di luar 2015–2024 "
        "tidak dimasukkan.",
        "- Seri luas sawah dan luas lahan/kebun/hutan hanya tersedia sebagai agregat nasional",
        "  menurut jenis bencana pada snapshot ini, sehingga tidak dibuat statistik provinsi.",
        "  Grafiknya tetap disimpan dan menandai keterbatasan tersebut.",
        "",
        "## Ringkasan per seri",
        "",
        "| Seri | n | Provinsi | Periode | Mean | Median | Min | Maks | Calon anomali | Grafik |",
        "|---|---:|---:|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in series_summary.to_dict("records"):
        if row["n"]:
            period = (
                f'{int(row["periode_awal"])}–{int(row["periode_akhir"])}'
            )
            vals = [f'{row[k]:,.3g}' for k in ("mean", "median", "min", "max")]
        else:
            period = "—"
            vals = ["—"] * 4
        chart = f'[Boxplot & deret waktu](gambar/{row["seri"]}.png)'
        lines.append(
            f'| `{row["seri"]}` | {row["n"]} | {row["n_provinsi"]} | {period} | '
            f'{vals[0]} | {vals[1]} | {vals[2]} | {vals[3]} | '
            f'{row["n_calon_anomali"]} | {chart} |'
        )

    lines.extend(
        [
            "",
            "Rincian statistik per seri tersimpan di [`profil-per-seri.csv`](profil-per-seri.csv),",
            "dan statistik per seri-provinsi di [`profil-per-provinsi.csv`](profil-per-provinsi.csv).",
            "Seluruh calon anomali tersedia di [`calon-anomali.csv`](calon-anomali.csv).",
            "",
            "## Calon anomali",
            "",
            "Daftar berikut menampilkan sampai lima observasi dengan nilai tertinggi per seri;",
            "CSV memuat seluruh observasi yang melampaui pagar IQR.",
            "",
        ]
    )
    for series in SERIES:
        candidates = anomalies[anomalies["seri"] == series].sort_values(
            "nilai", ascending=False
        )
        lines.append(f"### `{series}`")
        if candidates.empty:
            if int(series_summary.loc[series_summary["seri"] == series, "n"].iloc[0]) == 0:
                lines.append(
                    "Tidak ada observasi tingkat provinsi; calon anomali tidak dapat dinilai "
                    "dari sumber yang tersedia."
                )
            else:
                lines.append("Tidak ada observasi yang melampaui pagar IQR.")
        else:
            lines.append("")
            lines.append("| Provinsi | Periode | Nilai | Alasan |")
            lines.append("|---|---:|---:|---|")
            for item in candidates.head(5).itertuples():
                lines.append(
                    f"| {item.provinsi} | {item.periode} | {item.nilai:,.6g} | {item.alasan} |"
                )
        lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    data, monetary_period_notes = collect_observations()
    series_summary, province_summary, anomalies, _ = _summary_tables(data)
    series_summary.to_csv(REPORTS / "profil-per-seri.csv", index=False)
    province_summary.to_csv(REPORTS / "profil-per-provinsi.csv", index=False)
    anomalies.to_csv(REPORTS / "calon-anomali.csv", index=False)
    data.to_csv(REPORTS / "observasi-provinsi-tahap-2.csv", index=False)
    _make_charts(data, anomalies)
    _write_report(series_summary, anomalies, monetary_period_notes)
    print(
        f"Tahap 2 selesai: {len(data)} observasi provinsi-periode, "
        f"{len(anomalies)} calon anomali, {len(SERIES)} grafik."
    )


if __name__ == "__main__":
    main()
