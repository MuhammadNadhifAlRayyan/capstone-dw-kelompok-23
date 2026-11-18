import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

import pandas as pd

from src.common.manifest import baca
from src.silver.sqlite import muat_dataframe


class MuatSilverSQLiteTests(unittest.TestCase):
    def setUp(self):
        manifest = baca()
        raw_path = (
            "bnpb/2026-10-20/datastore/data-bencana-indonesia/"
            "03d7c28f-db2d-4fa3-a1e9-66109d7162d5.json"
        )
        self.data = pd.DataFrame(
            [
                {
                    "sumber": "bnpb",
                    "seri_kode": "nilai_kerusakan",
                    "wilayah_kode": 1300,
                    "nama_wilayah": "Sumatera Barat",
                    "periode": "2024",
                    "jenis_periode": "tahun",
                    "rincian": "uji",
                    "nilai": 137292872000,
                    "satuan": "rupiah",
                    "_berkas_raw": raw_path,
                    "_sha256_raw": manifest[raw_path],
                }
            ]
        )
        self.temp = tempfile.TemporaryDirectory()
        self.database = Path(self.temp.name) / "silver.sqlite"

    def tearDown(self):
        self.temp.cleanup()

    def test_memuat_observasi_ke_tabel_dengan_kunci_primer(self):
        jumlah = muat_dataframe(self.data, self.database)

        with closing(sqlite3.connect(self.database)) as koneksi:
            tersimpan = koneksi.execute(
                "SELECT seri_kode, nilai, _berkas_raw FROM silver"
            ).fetchall()
            kunci = koneksi.execute("PRAGMA table_info(silver)").fetchall()

        self.assertEqual(jumlah, 1)
        self.assertEqual(
            tersimpan,
            [("nilai_kerusakan", 137292872000, self.data.loc[0, "_berkas_raw"])],
        )
        self.assertEqual(sum(kolom[5] > 0 for kolom in kunci), 6)

    def test_muat_ulang_mengganti_isi_tabel(self):
        muat_dataframe(self.data, self.database)
        perubahan = self.data.copy()
        perubahan.loc[0, "nilai"] = 34547150000
        muat_dataframe(perubahan, self.database)

        with closing(sqlite3.connect(self.database)) as koneksi:
            hasil = koneksi.execute("SELECT COUNT(*), nilai FROM silver").fetchone()
        self.assertEqual(hasil, (1, 34547150000))

    def test_menolak_kunci_ganda_tanpa_mengubah_tabel(self):
        muat_dataframe(self.data, self.database)
        with self.assertRaises(ValueError):
            muat_dataframe(pd.concat([self.data, self.data], ignore_index=True), self.database)

        with closing(sqlite3.connect(self.database)) as koneksi:
            jumlah = koneksi.execute("SELECT COUNT(*) FROM silver").fetchone()[0]
        self.assertEqual(jumlah, 1)


if __name__ == "__main__":
    unittest.main()
