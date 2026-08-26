#!/usr/bin/env python3
# author: Just Ship It
# project: screenshot-to-code-railway
# purpose: Prove upstream pin updates remain repeatable after the first update.
# used_by: GitHub Actions verification
# status: active
# verified: 2026-08-26
from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "README.md",
    "NOTICE",
    "web/NOTICE",
    "web/Dockerfile",
    "backend/Dockerfile",
)


class UpstreamUpdateTests(unittest.TestCase):
    def test_two_consecutive_updates_advance_every_pin(self):
        first = "1" * 40
        second = "2" * 40
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            for name in FILES:
                target = checkout / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / name, target)

            subprocess.run(
                ["python3", str(ROOT / "scripts/set-upstream.py"), first, "--root", str(checkout)],
                check=True,
            )
            subprocess.run(
                ["python3", str(ROOT / "scripts/set-upstream.py"), second, "--root", str(checkout)],
                check=True,
            )
            current = subprocess.run(
                ["python3", str(ROOT / "scripts/set-upstream.py"), "--current", "--root", str(checkout)],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

            self.assertEqual(second, current)
            for name in FILES:
                text = (checkout / name).read_text(encoding="utf-8")
                self.assertIn(second, text, name)
                self.assertNotIn(first, text, name)

    def test_workflow_derives_and_updates_the_current_pin(self):
        workflow = (ROOT / ".github/workflows/verify.yml").read_text(encoding="utf-8")

        self.assertNotIn("d026163f586dfa8c5c10d28c36edd59a9d3b0e88", workflow)
        self.assertEqual(2, workflow.count("actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"))
        self.assertIn("set-upstream.py --current", workflow)
        self.assertIn("test-update-repeatability.py", workflow)
        self.assertIn('set-upstream.py "$UPSTREAM_SHA"', workflow)
        self.assertIn("git add README.md NOTICE web/NOTICE web/Dockerfile backend/Dockerfile", workflow)


if __name__ == "__main__":
    unittest.main()
