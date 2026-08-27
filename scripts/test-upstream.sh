#!/usr/bin/env bash
# author: Just Deploy It
# project: screenshot-to-code-railway
# purpose: Run the latest upstream main backend and frontend test suites.
# used_by: GitHub Actions compatibility verification
# status: active
# verified: pending
set -euo pipefail

workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT

git clone --depth 1 --branch main https://github.com/abi/screenshot-to-code.git "$workdir/source"

python3 -m venv "$workdir/poetry-runner"
"$workdir/poetry-runner/bin/python" -m pip install --disable-pip-version-check --no-cache-dir 'poetry==1.8.0'
(
  cd "$workdir/source/backend"
  "$workdir/poetry-runner/bin/poetry" install --with dev --no-interaction --no-ansi
  "$workdir/poetry-runner/bin/poetry" run pytest
)
(
  cd "$workdir/source/frontend"
  npx --yes pnpm@10.32.1 install --frozen-lockfile
  npx --yes pnpm@10.32.1 exec jest --passWithNoTests --runInBand
)
