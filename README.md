# Screenshot to Code on Railway

Minimal Railway wrapper for [abi/screenshot-to-code](https://github.com/abi/screenshot-to-code) at `d026163f586dfa8c5c10d28c36edd59a9d3b0e88`.

## Architecture

- `Web` builds the pinned pnpm frontend and serves it with Caddy.
- `Backend` runs the pinned FastAPI application and Playwright Chromium.
- Web is the sole public service. It provides Basic Auth and routes only core API, WebSocket and local asset paths to Backend over Railway private networking.
- Backend mounts `/data`. Design systems and local assets live there.

## Required variables

- `Web.BASIC_AUTH_PASSWORD` - generated Railway secret.
- `Web.BACKEND_HOST=${{Backend.RAILWAY_PRIVATE_DOMAIN}}`
- `Web.BACKEND_PORT=${{Backend.PORT}}`
- `Backend.SCREENSHOT_TO_CODE_DATA_DIR=/data`
- `Backend.LOCAL_ASSET_DIR=/data/local_assets`

Provider keys are intentionally not included. Configure a supported model provider only after reviewing upstream requirements and your provider's terms.

## Verification

`docker build -f web/Dockerfile web` and `docker build -f backend/Dockerfile backend` are the local clean-build checks. `scripts/test-upstream.sh d026163f586dfa8c5c10d28c36edd59a9d3b0e88` runs the pinned upstream backend and frontend test suites. Railway deploys must pass `/healthz` on Web and Backend `/` before template creation.

## Upstream updates

The wrapper pins an immutable upstream commit. The scheduled updater tests the candidate commit and rebuilds both images before opening a pull request. Do not move to a mutable tag.

## License notices

This wrapper is MIT licensed in [LICENSE](LICENSE). [NOTICE](NOTICE) preserves the upstream Screenshot to Code MIT copyright and permission notice. The final Web image also includes that notice at `/usr/share/caddy/NOTICE` alongside the compiled upstream assets.
