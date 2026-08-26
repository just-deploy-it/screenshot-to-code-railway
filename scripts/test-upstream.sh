#!/usr/bin/env bash
# author: Just Ship It
# project: screenshot-to-code-railway
# purpose: Run the pinned upstream backend and frontend test suites.
# used_by: GitHub Actions update verification
# status: active
# verified: pending
set -euo pipefail

upstream_commit=${1:?pass an immutable upstream commit}
workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT

git clone https://github.com/abi/screenshot-to-code.git "$workdir/source"
git -C "$workdir/source" checkout --detach "$upstream_commit"

python3 -m pip install --disable-pip-version-check --no-cache-dir 'poetry==1.8.0'
(
  cd "$workdir/source/backend"
  poetry install --with dev --no-interaction --no-ansi
  poetry run pytest
)
(
  cd "$workdir/source/frontend"
  corepack enable
  corepack prepare pnpm@10.32.1 --activate
  pnpm install --frozen-lockfile
  pnpm test -- --runInBand
)
