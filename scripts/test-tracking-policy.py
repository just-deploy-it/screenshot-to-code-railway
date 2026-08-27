#!/usr/bin/env python3
# ---
# author: Antoshka
# project: screenshot-to-code-railway
# purpose: Enforce moving upstream-main tracking without manual commit, version, tag or digest pins
# used_by: GitHub Actions verification and local acceptance
# status: active
# verified: 2026-08-27
# ---
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCKERFILES = (ROOT / "web/Dockerfile", ROOT / "backend/Dockerfile")


def main() -> int:
    errors: list[str] = []
    for path in DOCKERFILES:
        content = path.read_text(encoding="utf-8")
        label = path.relative_to(ROOT)
        if (
            "ADD https://github.com/abi/screenshot-to-code/archive/refs/heads/main.tar.gz "
            "/tmp/upstream-main.tar.gz"
            not in content
        ):
            errors.append(f"{label} must fetch the moving upstream main archive")
        if "tar -xzf /tmp/upstream-main.tar.gz --strip-components=1" not in content:
            errors.append(f"{label} must unpack the moving upstream archive during each invalidated build")
        if "git clone" in content:
            errors.append(f"{label} must not hide upstream tracking behind a cacheable clone layer")
        if "UPSTREAM_COMMIT" in content:
            errors.append(f"{label} must not declare an upstream commit pin")
        if re.search(r"\b[0-9a-f]{40}\b", content):
            errors.append(f"{label} must not contain a 40-character upstream commit")

    workflow = (ROOT / ".github/workflows/verify.yml").read_text(encoding="utf-8")
    for forbidden in ("set-upstream.py", "test-update-repeatability.py", "contents: write"):
        if forbidden in workflow:
            errors.append(f"verify workflow must not contain {forbidden}")

    if "shallow-clones" in (ROOT / "README.md").read_text(encoding="utf-8"):
        errors.append("README must describe the moving archive implementation, not the removed clone implementation")
    for required in (
        "./scripts/test-upstream.sh",
        "docker build --pull -t screenshot-to-code-web",
        "docker build --pull -t screenshot-to-code-backend",
        "persist-credentials: false",
        "schedule:",
    ):
        if required not in workflow:
            errors.append(f"verify workflow must contain {required}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    for forbidden in ("pinned upstream", "immutable upstream commit", "automated updater"):
        if forbidden in readme:
            errors.append(f"README must not claim {forbidden}")

    if errors:
        raise SystemExit("\n".join(errors))
    print("tracking_policy=pass upstream=main manual_pin=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
