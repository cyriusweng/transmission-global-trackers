import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


build = load_module("tracker_build", ROOT / "scripts" / "build.py")
boost_magnet = load_module("boost_magnet", ROOT / "scripts" / "boost_magnet.py")


class BuildTests(unittest.TestCase):
    def test_normalise_tracker(self):
        self.assertEqual(
            build.normalise_url("HTTPS://Tracker.Example.COM:443/announce"),
            "https://tracker.example.com/announce",
        )
        self.assertEqual(
            build.normalise_url("udp://[2001:4860:4860::8888]:6969/announce"),
            "udp://[2001:4860:4860::8888]:6969/announce",
        )

    def test_rejects_private_and_malformed_trackers(self):
        self.assertIsNone(build.normalise_url("udp://127.0.0.1:6969/announce"))
        self.assertIsNone(build.normalise_url("udp://tracker.example.com/announce"))
        self.assertIsNone(build.normalise_url("ftp://tracker.example.com/announce"))

    def test_balanced_tier_format(self):
        text = build.tier_text([["udp://a.example:80/announce", "https://b.example/announce"], ["udp://c.example:80/announce"]])
        self.assertEqual(
            text,
            "udp://a.example:80/announce\nhttps://b.example/announce\n\nudp://c.example:80/announce\n",
        )

    def test_boost_magnet_deduplicates_trackers(self):
        magnet = "magnet:?xt=urn:btih:ABC&tr=udp://one.example:80/announce"
        result = boost_magnet.boost(
            magnet,
            ["udp://one.example:80/announce", "https://two.example/announce"],
        )
        self.assertEqual(result.count("udp://one.example:80/announce"), 1)
        self.assertIn("https://two.example/announce", result)


if __name__ == "__main__":
    unittest.main()
