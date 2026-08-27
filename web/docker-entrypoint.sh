#!/bin/sh
# author: Just Deploy It
# project: screenshot-to-code-railway
# purpose: Derive the runtime-only Caddy Basic Auth hash from a Railway secret.
# used_by: Railway Web service
# status: active
# verified: pending
set -eu
: "${BASIC_AUTH_PASSWORD:?BASIC_AUTH_PASSWORD is required}"
: "${BACKEND_HOST:?BACKEND_HOST is required}"
: "${BACKEND_PORT:?BACKEND_PORT is required}"
: "${PORT:?PORT is required}"
export BASIC_AUTH_HASH="$(caddy hash-password --algorithm bcrypt --plaintext "$BASIC_AUTH_PASSWORD")"
exec caddy run --config /etc/caddy/Caddyfile --adapter caddyfile
