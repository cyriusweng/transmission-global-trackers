import importlib.util
import re
import unittest
import urllib.parse
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


build = load_module("tracker_build", ROOT / "scripts" / "build.py")
boost_magnet = load_module("boost_magnet", ROOT / "scripts" / "boost_magnet.py")

LANGUAGE_PAGES = [
    ROOT / "README.md",
    ROOT / "README.zh-CN.md",
    *sorted((ROOT / "docs" / "i18n").glob("README.*.md")),
]
REQUIRED_GUIDE_MARKERS = (
    "lists/transmission/macos.txt",
    "lists/transmission/magnet.txt",
    "lists/transmission/balanced.txt",
    "lists/transmission/aggressive.txt",
    "lists/candidates/all.txt",
    "lists/webtorrent/all.txt",
    "lists/special/",
    "scripts/boost_magnet.py",
    "--open",
    "default_trackers",
    "GitHub Actions",
    "passkey",
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def nonblank_lines(path):
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


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

    def test_macos_and_magnet_lists_are_balanced_primaries(self):
        transmission_dir = ROOT / "lists" / "transmission"
        tiers = [
            nonblank_lines_from_text
            for block in (transmission_dir / "balanced.txt").read_text(encoding="utf-8").strip().split("\n\n")
            if (nonblank_lines_from_text := [line.strip() for line in block.splitlines() if line.strip()])
        ]
        primaries = [tier[0] for tier in tiers]
        macos = nonblank_lines(transmission_dir / "macos.txt")
        magnet = nonblank_lines(transmission_dir / "magnet.txt")

        self.assertEqual(len(primaries), 12)
        self.assertEqual(macos, primaries)
        self.assertEqual(magnet, primaries)
        self.assertEqual(boost_magnet.PROFILES["balanced"], transmission_dir / "magnet.txt")

    def test_balanced_magnet_profile_adds_only_twelve_primaries(self):
        trackers = boost_magnet.tracker_urls(boost_magnet.PROFILES["balanced"])
        result = boost_magnet.boost("magnet:?xt=urn:btih:ABC", trackers)
        query = urllib.parse.parse_qsl(urllib.parse.urlsplit(result).query)
        added_trackers = [value for key, value in query if key == "tr"]

        self.assertEqual(len(added_trackers), 12)
        self.assertEqual(added_trackers, trackers)

    def test_open_in_transmission_uses_macos_application(self):
        magnet = "magnet:?xt=urn:btih:ABC"
        with (
            mock.patch.object(boost_magnet.sys, "platform", "darwin"),
            mock.patch.object(boost_magnet.subprocess, "run") as run,
        ):
            boost_magnet.open_in_transmission(magnet)

        run.assert_called_once_with(
            ["open", "-a", "Transmission", magnet],
            check=True,
        )

    def test_all_language_guides_cover_the_complete_workflow(self):
        self.assertEqual(len(LANGUAGE_PAGES), 21)
        for page in LANGUAGE_PAGES:
            text = page.read_text(encoding="utf-8")
            with self.subTest(page=page.relative_to(ROOT)):
                self.assertGreaterEqual(text.count("\n## "), 6)
                for marker in REQUIRED_GUIDE_MARKERS:
                    self.assertIn(marker.casefold(), text.casefold())

    def test_all_local_markdown_links_exist(self):
        for page in LANGUAGE_PAGES:
            text = page.read_text(encoding="utf-8")
            for target in MARKDOWN_LINK_RE.findall(text):
                parsed = urllib.parse.urlsplit(target)
                if parsed.scheme or target.startswith("#"):
                    continue
                path = urllib.parse.unquote(parsed.path)
                if not path:
                    continue
                resolved = (page.parent / path).resolve()
                with self.subTest(page=page.relative_to(ROOT), target=target):
                    self.assertTrue(resolved.exists(), f"missing local link target: {resolved}")


if __name__ == "__main__":
    unittest.main()
