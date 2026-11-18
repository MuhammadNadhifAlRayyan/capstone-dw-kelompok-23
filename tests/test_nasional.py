import unittest

import pandas as pd

from src import wilayah as W
from src.gold.nasional import rekonsiliasi


class RekonsiliasiNasionalTests(unittest.TestCase):
    def setUp(self):
        self.baris = []
        nasional_saja = "bnpb/2026-10-20/datastore/data-bencana-indonesia/nasional.json"
        self.baris.append(self._baris("2023", 100, W.INDONESIA, "jenis_bencana=banjir", nasional_saja))

        for periode, nasional in (("2024", 40), ("2025", 100)):
            if periode == "2024":
                sumber = "bnpb/2026-10-20/datastore/data-bencana-indonesia/lengkap.json"
                cermin = "bnpb/2026-10-20/datastore/kompilasi-data-jumlah-dan-dampak-kejadian-bencana-2024/cermin.json"
                for berkas in (sumber, cermin):
                    self.baris.append(self._baris(periode, nasional, W.INDONESIA, "jenis_bencana=banjir", berkas))
                    self.baris.extend(
                        self._baris(periode, 1, kode, "jenis_bencana=banjir", berkas)
                        for kode in W.PROVINSI
                    )
            else:
                sumber = (
                    "bnpb/2026-10-20/tangan/kompilasi-data-kejadian-dan-dampak-bencana-2025/"
                    "43b83e79-c8b6-4b9a-b2f0-d1cbd9cfa636-jumlah-rumah-rusak-akibat-bencana-menurut-provinsi-2025.xlsx"
                )
                self.baris.append(self._baris(periode, nasional, W.INDONESIA, "jenis_bencana=banjir", sumber))
                self.baris.extend([
                    self._baris(periode, 63, next(iter(W.PROVINSI)), "jenis_bencana=banjir", sumber),
                    *(
                        self._baris(periode, 1, kode, "jenis_bencana=banjir", sumber)
                        for kode in list(W.PROVINSI)[1:]
                    ),
                ])

        sumber_rinci = (
            "bnpb/2026-10-20/tangan/kompilasi-data-kejadian-dan-dampak-bencana-2025/"
            "6e947c9c-2404-4c02-b743-34dc5320f399-rekapitulasi-jumlah-kejadian-dan-dampak-bencana-menurut-provinsi-2025.xlsx"
        )
        for tingkat, nilai in (("berat", 30), ("sedang", 20), ("ringan", 49)):
            self.baris.append(
                self._baris(
                    "2025", nilai, W.INDONESIA,
                    f"jenis_bencana=banjir;tingkat_kerusakan={tingkat}", sumber_rinci,
                )
            )
        self.silver = pd.DataFrame(self.baris)

    @staticmethod
    def _baris(periode, nilai, wilayah, rincian, berkas):
        return {
            "seri_kode": "rumah_rusak",
            "periode": periode,
            "nilai": nilai,
            "wilayah_kode": wilayah,
            "rincian": rincian,
            "_berkas_raw": berkas,
        }

    def test_jumlah_provinsi_hanya_dibandingkan_bila_satu_berkas_lengkap(self):
        hasil = rekonsiliasi(self.silver)
        p1 = hasil[hasil["id"] == "P1"].set_index("periode")

        self.assertEqual(set(p1.index), {"2024", "2025"})
        self.assertEqual(p1.loc["2024", "berkas_utama"],
                         "bnpb/2026-10-20/datastore/data-bencana-indonesia/lengkap.json")
        self.assertEqual(p1.loc["2024", "selisih_pembanding_minus_utama"], -2)
        self.assertEqual(p1.loc["2024", "status"], "berbeda")
        self.assertEqual(p1.loc["2025", "selisih_pembanding_minus_utama"], 0)

    def test_jumlah_provinsi_mempertahankan_varian_sumber_yang_berbeda(self):
        sumber_alternatif = "bnpb/2026-10-20/datastore/versi-lain.json"
        varian = self.silver[
            (self.silver["periode"] == "2024")
            & (self.silver["_berkas_raw"].str.endswith("data-bencana-indonesia/lengkap.json"))
        ].copy()
        varian["_berkas_raw"] = sumber_alternatif
        varian.loc[varian["wilayah_kode"] == W.INDONESIA, "nilai"] = 41

        hasil = rekonsiliasi(pd.concat([self.silver, varian], ignore_index=True))
        p1 = hasil[(hasil["id"] == "P1") & (hasil["periode"] == "2024")]

        self.assertEqual(set(p1["selisih_pembanding_minus_utama"]), {-2, -3})
        self.assertIn(sumber_alternatif, set(p1["berkas_utama"]))

    def test_jumlah_rincian_mempertahankan_selisih(self):
        hasil = rekonsiliasi(self.silver)
        p2 = hasil[hasil["id"] == "P2"].iloc[0]

        self.assertEqual(p2["periode"], "2025")
        self.assertEqual(p2["nilai_pembanding"], 99)
        self.assertEqual(p2["selisih_pembanding_minus_utama"], -1)
        self.assertEqual(p2["status"], "berbeda")


if __name__ == "__main__":
    unittest.main()
