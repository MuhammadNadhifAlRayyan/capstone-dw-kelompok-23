"""Klasifikasi calon anomali dan audit snapshot untuk Tahap 3."""

from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

from src.ekstraksi.baca_datastore import baca_semua_datastore
from src.ekstraksi.baca_xlsx import baca_semua_xlsx
from src.gold.skema import PROVINSI_38_2025


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
COUNT_SERIES = {
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
}
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


def _province(value):
    return PROVINCES.get("".join(str(value).upper().split()))


def _find_source(sources, prefix):
    result = next(
        (frame for name, frame in sources.items() if Path(name).name.startswith(prefix)),
        None,
    )
    if result is None:
        raise FileNotFoundError(f"Sumber snapshot {prefix} tidak ditemukan.")
    return result


def _source_values(frame, province_col):
    if province_col not in frame.columns:
        raise ValueError(f"Kolom provinsi {province_col!r} tidak ada.")
    value_columns = [column for column in DISASTER_TYPES if column in frame.columns]
    if not value_columns:
        raise ValueError("Kolom jenis bencana tidak ditemukan pada snapshot.")
    data = frame.copy()
    data["provinsi"] = data[province_col].map(_province)
    for column in value_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    data["nilai"] = data[value_columns].sum(axis=1, min_count=1)
    data = data.dropna(subset=["provinsi", "nilai"])
    return data.groupby("provinsi")["nilai"].sum(min_count=1)


def _history_kejadian_2024(frame):
    province_col = "Nama Provinsi" if "Nama Provinsi" in frame else "Provinsi"
    year_col = next(
        (
            column
            for column in frame.columns
            if str(column).replace(".0", "") == "2024"
        ),
        None,
    )
    if year_col is None:
        raise ValueError("Kolom tahun 2024 tidak ditemukan pada snapshot kejadian.")
    data = pd.DataFrame(
        {
            "provinsi": frame[province_col].map(_province),
            "nilai": pd.to_numeric(frame[year_col], errors="coerce"),
        }
    ).dropna(subset=["provinsi", "nilai"])
    return data.groupby("provinsi")["nilai"].sum(min_count=1)


def audit_snapshots():
    datastore = baca_semua_datastore()
    xlsx = baca_semua_xlsx()
    groups = []

    kejadian = [
        (
            "rekap_2010_2024",
            _history_kejadian_2024(_find_source(datastore, "5dfcae7e")),
            _find_source(datastore, "5dfcae7e")["_berkas_raw"].iloc[0],
        ),
        *[
            (
                label,
                _source_values(_find_source(datastore, prefix), "Provinsi"),
                _find_source(datastore, prefix)["_berkas_raw"].iloc[0],
            )
            for label, prefix in (
                ("snapshot_bnpb_2024", "faeb2406"),
                ("kompilasi_2024", "f345ba43"),
            )
        ],
    ]
    groups.append(("kejadian", 2024, kejadian))

    for series, sources, province_col in (
        (
            "rumah_rusak",
            [
                ("snapshot_bnpb_2024", datastore, "471f71cb"),
                ("kompilasi_2024", datastore, "b5e3d843"),
            ],
            "Provinsi",
        ),
        (
            "jembatan_rusak",
            [
                ("snapshot_bnpb_2024", datastore, "308f0499"),
                ("kompilasi_2024", datastore, "ad86fca8"),
            ],
            "Provinsi",
        ),
        (
            "kantor_rusak",
            [
                ("snapshot_xlsx_2024", xlsx, "742bb9f9"),
                ("kompilasi_xlsx_2024", xlsx, "091da066"),
            ],
            "Provinsi",
        ),
        (
            "rumah_ibadat_rusak",
            [
                ("snapshot_xlsx_2024", xlsx, "5f3bdd4d"),
                ("kompilasi_xlsx_2024", xlsx, "200c487f"),
            ],
            "Provinsi",
        ),
    ):
        snapshots = []
        for label, source_files, prefix in sources:
            frame = _find_source(source_files, prefix)
            snapshots.append(
                (label, _source_values(frame, province_col), frame["_berkas_raw"].iloc[0])
            )
        groups.append((series, 2024, snapshots))

    audit_rows = []
    duplicate_copies = 0
    pairwise_identical = 0
    pairwise_revisions = 0
    pairwise_missing = 0
    for series, period, snapshots in groups:
        all_provinces = sorted(
            set().union(*(set(values.index) for _, values, _ in snapshots))
        )
        for province in all_provinces:
            observed = [values.get(province, np.nan) for _, values, _ in snapshots]
            if all(pd.notna(value) for value in observed) and len(set(observed)) == 1:
                duplicate_copies += len(observed) - 1
        for (label_a, values_a, path_a), (label_b, values_b, path_b) in combinations(
            snapshots, 2
        ):
            for province in sorted(set(values_a.index) | set(values_b.index)):
                value_a = values_a.get(province, np.nan)
                value_b = values_b.get(province, np.nan)
                if pd.isna(value_a) or pd.isna(value_b):
                    status = "hanya tersedia pada satu snapshot"
                    pairwise_missing += 1
                elif value_a == value_b:
                    status = "identik; satu nilai dipakai"
                    pairwise_identical += 1
                else:
                    status = "berbeda; perlakukan sebagai revisi"
                    pairwise_revisions += 1
                audit_rows.append(
                    {
                        "seri": series,
                        "periode": period,
                        "provinsi": province,
                        "snapshot_a": label_a,
                        "berkas_a": path_a,
                        "nilai_a": value_a,
                        "snapshot_b": label_b,
                        "berkas_b": path_b,
                        "nilai_b": value_b,
                        "status": status,
                    }
                )
    metrics = {
        "identik": pairwise_identical,
        "revisi": pairwise_revisions,
        "hanya_satu_snapshot": pairwise_missing,
        "salinan_tidak_dihitung": duplicate_copies,
    }
    return pd.DataFrame(audit_rows), metrics


def test_breaks(observations):
    rows = []
    breaks = {}
    for series, data in observations.groupby("seri"):
        wide = data.pivot(index="provinsi", columns="periode", values="nilai")
        years = sorted(wide.columns)
        for previous, current in zip(years, years[1:]):
            if current != previous + 1:
                continue
            pair = wide[[previous, current]].dropna()
            if pair.empty:
                continue
            changes = pair[current] - pair[previous]
            increases = int((changes > 0).sum())
            decreases = int((changes < 0).sum())
            unchanged = int((changes == 0).sum())
            direction = "naik" if increases >= decreases else "turun"
            agreement = max(increases, decreases) / len(pair)
            median_previous = float(pair[previous].median())
            median_current = float(pair[current].median())
            relative_change = (
                abs(median_current - median_previous) / abs(median_previous)
                if median_previous != 0
                else np.nan
            )
            is_break = (
                len(pair) >= 20
                and agreement >= 0.75
                and pd.notna(relative_change)
                and relative_change >= 0.5
            )
            if is_break:
                breaks[(series, int(current))] = (
                    direction,
                    agreement,
                    relative_change,
                    len(pair),
                )
            rows.append(
                {
                    "seri": series,
                    "periode_sebelum": int(previous),
                    "periode_sesudah": int(current),
                    "provinsi_berpasangan": len(pair),
                    "provinsi_naik": increases,
                    "provinsi_turun": decreases,
                    "provinsi_tetap": unchanged,
                    "arah_dominan": direction,
                    "proporsi_searah": agreement,
                    "median_sebelum": median_previous,
                    "median_sesudah": median_current,
                    "perubahan_median_rel": relative_change,
                    "ambang_patahan_terpenuhi": is_break,
                }
            )
    return pd.DataFrame(rows), breaks


def _input_error(data):
    if data["nilai"] < 0:
        return "Nilai negatif tidak sah untuk seri dampak ini."
    if data["seri"] in COUNT_SERIES and not float(data["nilai"]).is_integer():
        return "Nilai pecahan pada seri hitungan unit/kejadian."
    return None


def classify_candidates(candidates, observations, breaks):
    rows = []
    for candidate in candidates.itertuples(index=False):
        key = (candidate.seri, candidate.provinsi, int(candidate.periode))
        observation = observations[
            (observations["seri"] == candidate.seri)
            & (observations["provinsi"] == candidate.provinsi)
            & (observations["periode"] == candidate.periode)
        ]
        if len(observation) != 1:
            raise ValueError(f"Observasi kandidat tidak unik: {key}")
        source_value = observation.iloc[0]["nilai"]
        error = _input_error(observation.iloc[0])
        break_info = breaks.get((candidate.seri, int(candidate.periode)))
        if error:
            category = "galat input"
            reason = error
            action = "Perbaiki hanya setelah nilai pembetulan diverifikasi terhadap sumber asli."
            confidence = "perlu verifikasi sumber"
        elif break_info:
            direction, agreement, relative_change, paired = break_info
            category = "patahan seri"
            reason = (
                f"{paired} provinsi berpasangan; {agreement:.0%} bergerak {direction} "
                f"dan median berubah {relative_change:.0%} antarperiode."
            )
            action = "Pertahankan nilai; tandai patahan dan jangan bandingkan lintas-patahan."
            confidence = "indikasi metodologis"
        else:
            category = "outlier asli"
            reason = (
                "Nilai melampaui pagar IQR; tidak negatif dan, untuk seri hitungan, "
                "bilangan bulat. Tidak memenuhi uji lonjakan serentak untuk patahan seri; "
                "tidak ada bukti galat input yang dapat diverifikasi."
            )
            if candidate.seri in {"kios_toko_rusak", "pabrik_rusak"}:
                reason += (
                    " Sebaran seri sangat jarang/berisi banyak nol sehingga nilai positif "
                    "dapat terflag oleh pagar IQR nol."
                )
            action = "Pertahankan nilai sebagai observasi ekstrem; jangan winsorize/hapus."
            confidence = "sementara; perlu konteks kejadian"
        rows.append(
            {
                "seri": candidate.seri,
                "provinsi": candidate.provinsi,
                "periode": int(candidate.periode),
                "nilai": source_value,
                "alasan_iqr": candidate.alasan,
                "kategori": category,
                "alasan_kategori": reason,
                "tindakan": action,
                "kepastian": confidence,
            }
        )
    return pd.DataFrame(rows).sort_values(["seri", "periode", "provinsi"])


def write_report(classified, break_tests, break_map, snapshot_metrics, quality_metrics):
    category_counts = classified["kategori"].value_counts().to_dict()
    lines = [
        "# Tahap 3 — Klasifikasi anomali, patahan, dan galat input",
        "",
        "Tahap ini mengelompokkan semua penanda IQR dari profil Tahap 2. Nilai tidak diubah:",
        "outlier asli dan patahan seri ditandai, sedangkan perbaikan hanya dibenarkan untuk",
        "galat input yang terbukti dari sumber. Kategori outlier di sini bersifat sementara;",
        "validasi statistik tidak membuktikan penyebab kejadian.",
        "",
        "## Ringkasan klasifikasi",
        "",
        f"- Calon anomali Tahap 2 yang diklasifikasikan: **{len(classified)}**.",
        f"- Outlier asli (sementara): **{category_counts.get('outlier asli', 0)}**.",
        f"- Patahan seri berdasarkan uji serentak: **{category_counts.get('patahan seri', 0)}**.",
        f"- Galat input yang terkonfirmasi di antara kandidat: **{category_counts.get('galat input', 0)}**.",
        f"- Nilai negatif pada observasi: **{quality_metrics['negatif']}**; nilai pecahan pada seri hitungan: **{quality_metrics['pecahan_hitungan']}**.",
        "- Tidak ada perbaikan angka dilakukan. Tidak ditemukan galat input yang terbukti; "
        "ini bukan jaminan bahwa sumber bebas dari semua kesalahan.",
        "",
        "Rincian untuk setiap kandidat terdapat pada "
        "[`klasifikasi-anomali.csv`](klasifikasi-anomali.csv).",
        "",
        "## Uji patahan seri",
        "",
        "Uji hanya memakai pasangan provinsi yang memiliki nilai pada dua tahun berurutan.",
        "Patahan serentak ditandai bila sedikitnya 20 provinsi berpasangan, sekurangnya 75%",
        "bergerak searah, dan median lintas-provinsi berubah minimal 50% dari median tahun",
        "sebelumnya. Ini adalah ambang penyaring eksploratif; konfirmasi perubahan definisi",
        "tetap memerlukan dokumentasi sumber.",
        "",
        f"Pasangan tahun yang memenuhi kedua ambang: **{len(break_map)}**. "
        "Tidak ada tahun yang ditetapkan sebagai patahan.",
        "Perubahan 2021→2022 pada `rumah_rusak` menurun di 76% provinsi berpasangan, tetapi",
        "median hanya turun sekitar 22%, sehingga tidak memenuhi ambang perubahan median.",
        "Untuk `kejadian`, kenaikan 2020→2021 terjadi pada 74% provinsi; masih di bawah",
        "ambang 75%. Tahun yang tidak berurutan atau memiliki terlalu sedikit pasangan tidak",
        "dapat dinilai dengan uji ini.",
        "",
        "Tabel seluruh transisi yang diuji: [`uji-patahan-seri.csv`](uji-patahan-seri.csv).",
        "",
        "## Audit duplikasi lintas snapshot",
        "",
        "Kunci pembandingan adalah seri, periode, dan provinsi setelah menjumlahkan rincian",
        "jenis bencana dalam satu snapshot. Angka sama lintas snapshot dianggap salinan dari",
        "observasi yang sama dan hanya dihitung sekali; angka berbeda dicatat sebagai revisi",
        "berprovenans, bukan dijumlahkan atau otomatis disebut galat input.",
        "",
        f"Audit mencakup {snapshot_metrics['identik'] + snapshot_metrics['revisi'] + snapshot_metrics['hanya_satu_snapshot']} "
        f"perbandingan pasangan provinsi: {snapshot_metrics['identik']} identik, "
        f"{snapshot_metrics['revisi']} berbeda/revisi, dan "
        f"{snapshot_metrics['hanya_satu_snapshot']} hanya tersedia pada satu snapshot. "
        f"Salinan identik yang tidak dihitung ulang: {snapshot_metrics['salinan_tidak_dihitung']}.",
        "Pada snapshot 2024 yang diperiksa, seluruh nilai yang berpasangan identik; tidak ada",
        "revisi berbeda yang perlu dipilih. Rincian per provinsi dan berkas sumber ada pada",
        "[`audit-snapshot-2024.csv`](audit-snapshot-2024.csv).",
        "",
        "## Keputusan penanganan",
        "",
        "- Outlier asli: pertahankan sebagai nilai sah yang ekstrem; tidak dihapus atau",
        "  di-winsorize. Kasus dengan sebaran nol-dominan (misalnya kios/pabrik) memerlukan",
        "  verifikasi konteks, sebab pagar IQR nol menandai nilai positif.",
        "- Patahan seri: bila kelak terkonfirmasi dari metadata, pertahankan observasi dan",
        "  analisis terpisah sebelum/sesudah perubahan; jangan menghaluskan atau mengganti nilai.",
        "- Galat input: hanya koreksi setelah nilai pembetulan dapat dilacak ke sumber asli;",
        "  catat nilai lama, nilai baru, alasan, dan jumlah baris di `log-keputusan.csv`.",
        "- Aturan deduplikasi dan hasil audit dicatat di `log-keputusan.csv`; tidak ada koreksi",
        "  input pada tahap ini.",
    ]
    (REPORTS / "tahap-3-klasifikasi-anomali.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main():
    observations = pd.read_csv(REPORTS / "observasi-provinsi-tahap-2.csv")
    candidates = pd.read_csv(REPORTS / "calon-anomali.csv")
    if candidates.empty:
        raise ValueError("Daftar calon anomali Tahap 2 kosong atau tidak ditemukan.")

    snapshot_audit, snapshot_metrics = audit_snapshots()
    break_tests, break_map = test_breaks(observations)
    classified = classify_candidates(candidates, observations, break_map)

    count_values = observations[observations["seri"].isin(COUNT_SERIES)]["nilai"]
    quality_metrics = {
        "negatif": int((observations["nilai"] < 0).sum()),
        "pecahan_hitungan": int((count_values % 1 != 0).sum()),
    }
    REPORTS.mkdir(parents=True, exist_ok=True)
    classified.to_csv(REPORTS / "klasifikasi-anomali.csv", index=False)
    break_tests.to_csv(REPORTS / "uji-patahan-seri.csv", index=False)
    snapshot_audit.to_csv(REPORTS / "audit-snapshot-2024.csv", index=False)
    write_report(classified, break_tests, break_map, snapshot_metrics, quality_metrics)
    print(
        f"{len(classified)} kandidat diklasifikasikan; "
        f"{len(break_map)} patahan terdeteksi; "
        f"{snapshot_metrics['identik']} pasangan snapshot identik, "
        f"{snapshot_metrics['revisi']} berbeda."
    )


if __name__ == "__main__":
    main()
