import unittest
import tempfile
import csv
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from src.gold import aturan
from src.gold.aturan import pilih_observasi_gold
from src.gold.panel import bentuk_panel_gold, transformasi_log1p


class GoldRuleTests(unittest.TestCase):
    def setUp(self):
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        self.log_patch = patch(
            "src.gold.aturan.LOG_PATH",
            Path(temporary_directory.name) / "log-keputusan.csv",
        )
        self.log_patch.start()
        self.addCleanup(self.log_patch.stop)
        self.silver = pd.DataFrame(
            [
                self.row("kejadian", "total", "2020", "bnpb/2026-10-20/datastore/old.json", 10),
                self.row(
                    "kejadian",
                    "total",
                    "2020",
                    "bnpb/2026-10-20/datastore/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/new.json",
                    12,
                ),
                self.row(
                    "kejadian",
                    "jenis_bencana=banjir",
                    "2020",
                    "bnpb/old.json",
                    5,
                ),
                self.row("rumah_rusak", "berat", "2020", "bnpb/house.json", 2),
                self.row("kejadian", "total", "2020-01", "bnpb/month.json", 3, "bulan"),
                self.row("EN.CLC.MDAT.ZS", "total", "2009", "wdi/data.json", 4, "tahun", 9999, "INDONESIA"),
            ]
        )

    @staticmethod
    def row(
        series,
        detail,
        period,
        path,
        value,
        period_type="tahun",
        region=1100,
        region_name="ACEH",
    ):
        return {
            "sumber": "bnpb" if region != 9999 else "wdi",
            "seri_kode": series,
            "wilayah_kode": region,
            "nama_wilayah": region_name,
            "periode": period,
            "jenis_periode": period_type,
            "rincian": detail,
            "nilai": value,
            "satuan": "unit",
            "_berkas_raw": path,
            "_sha256_raw": "hash",
        }

    def test_selects_one_snapshot_and_only_panel_details(self):
        flags = pd.DataFrame(
            [
                {
                    "seri_kode": "kejadian",
                    "wilayah_kode": 1100,
                    "periode": "2020",
                    "flag_outlier": True,
                    "flag_patahan": True,
                }
            ]
        )
        panel_rows, national, counts = pilih_observasi_gold(self.silver, flags=flags)

        self.assertEqual(len(panel_rows.query("seri_kode == 'kejadian'")), 1)
        selected = panel_rows.query("seri_kode == 'kejadian'").iloc[0]
        self.assertEqual(selected["nilai"], 12)
        self.assertTrue(selected["flag_outlier"])
        self.assertTrue(selected["flag_patahan"])
        self.assertEqual(panel_rows["_indikator"].tolist(), ["kejadian", "rumah_rusak_berat"])
        self.assertEqual(
            counts,
            {
                "K-101": 1,
                "K-102": 1,
                "K-103": 1,
                "K-104": 0,
                "K-105": 0,
            },
        )
        self.assertEqual(national["indikator"].tolist(), ["EN.CLC.MDAT.ZS"])
        with aturan.LOG_PATH.open(encoding="utf-8", newline="") as logged:
            decisions = {row["id"]: row for row in csv.DictReader(logged)}
        self.assertEqual(decisions["K-101"]["tahap"], "gold")
        self.assertEqual(decisions["K-101"]["dampak_baris"], "1")
        self.assertIn("tidak disesuaikan dengan inflasi", decisions["K-104"]["keputusan"])
        self.assertIn("flag outlier serta patahan", decisions["K-105"]["keputusan"])
        self.assertEqual(decisions["K-104"]["dampak_baris"], "0")
        self.assertEqual(decisions["K-105"]["dampak_baris"], "0")

    def test_builds_unique_wide_panel_and_keeps_flags(self):
        with patch(
            "src.gold.aturan._flag_tables",
            return_value=(pd.DataFrame(), pd.DataFrame()),
        ):
            panel, national = bentuk_panel_gold(self.silver)
        self.assertEqual(len(panel), 38 * 16)
        aceh_2020 = panel.query("wilayah_kode == 1100 and tahun == 2020").iloc[0]
        self.assertEqual(aceh_2020["kejadian"], 12)
        self.assertTrue(pd.isna(aceh_2020["kejadian__flag_outlier"]))
        self.assertEqual(len(national), 1)

    def test_sums_disaster_type_rows_when_no_direct_total_exists(self):
        source = pd.DataFrame(
            [
                self.row("kejadian", "jenis_bencana=banjir", "2021", "bnpb/a.json", 3),
                self.row("kejadian", "jenis_bencana=tsunami", "2021", "bnpb/a.json", 2),
            ]
        )
        panel_rows, _, counts = pilih_observasi_gold(source, flags=pd.DataFrame())
        self.assertEqual(panel_rows.iloc[0]["nilai"], 5)
        self.assertEqual(counts["K-102"], 0)

    def test_house_total_comes_from_three_levels_only_when_all_exist(self):
        source = pd.DataFrame(
            [
                self.row("rumah_rusak", "tingkat_kerusakan=berat", "2021", "bnpb/a.json", 2),
                self.row("rumah_rusak", "tingkat_kerusakan=sedang", "2021", "bnpb/a.json", 3),
                self.row("rumah_rusak", "tingkat_kerusakan=ringan", "2021", "bnpb/a.json", 4),
            ]
        )
        panel_rows, _, _ = pilih_observasi_gold(source, flags=pd.DataFrame())
        values = panel_rows.set_index("_indikator")["nilai"]
        self.assertEqual(values["rumah_rusak_total"], 9)

    def test_log1p_does_not_adjust_inflation_or_clip_negative_values(self):
        transformed = transformasi_log1p(pd.Series([0, 9]))
        self.assertAlmostEqual(transformed.iloc[1], 2.30258509299)
        with self.assertRaises(ValueError):
            transformasi_log1p(pd.Series([-1]))


if __name__ == "__main__":
    unittest.main()
