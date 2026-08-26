#!/usr/bin/env python3
# author: Just Ship It
# project: screenshot-to-code-railway
# purpose: Read or atomically advance every declared immutable upstream pin.
# used_by: GitHub Actions updater and repeatability test
# status: active
# verified: 2026-08-26
from __future__ import annotations

import argparse
import re
from pathlib import Path


PIN = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
PIN_FILES = (
    "README.md",
    "NOTICE",
    "web/NOTICE",
    "web/Dockerfile",
    "backend/Dockerfile",
)


def pins(root: Path) -> set[str]:
    found: set[str] = set()
    for name in PIN_FILES:
        matches = PIN.findall((root / name).read_text(encoding="utf-8"))
        if not matches:
            raise ValueError(f"missing upstream pin in {name}")
        found.update(matches)
    return found


def current_pin(root: Path) -> str:
    found = pins(root)
    if len(found) != 1:
        raise ValueError(f"upstream pins disagree: {sorted(found)}")
    return found.pop()


def set_pin(root: Path, new_pin: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", new_pin):
        raise ValueError("upstream pin must be 40 lowercase hex characters")
    current_pin(root)
    for name in PIN_FILES:
        path = root / name
        updated, count = PIN.subn(new_pin, path.read_text(encoding="utf-8"))
        if count == 0:
            raise ValueError(f"failed to update {name}")
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(updated, encoding="utf-8")
        temporary.replace(path)
    if current_pin(root) != new_pin:
        raise ValueError("upstream pin update did not converge")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pin", nargs="?")
    parser.add_argument("--current", action="store_true")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    arguments = parser.parse_args()
    if arguments.current == bool(arguments.pin):
        parser.error("choose exactly one of PIN or --current")
    root = arguments.root.resolve()
    if arguments.current:
        print(current_pin(root))
    else:
        set_pin(root, arguments.pin)
        print(arguments.pin)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
