# Screenshot to Code on Railway

Minimal Railway wrapper for the latest `main` branch of [abi/screenshot-to-code](https://github.com/abi/screenshot-to-code).

## Architecture

- `Web` builds the latest upstream pnpm frontend and serves it with Caddy.
- `Backend` runs the latest upstream FastAPI application and Playwright Chromium.
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

`docker build -f web/Dockerfile web` and `docker build -f backend/Dockerfile backend` are the local clean-build checks. `scripts/test-upstream.sh` runs the latest upstream `main` backend and frontend test suites. Railway deploys must pass `/healthz` on Web and Backend `/` before template creation.

## Upstream updates

Every image build downloads and unpacks the moving upstream `main` source archive. Redeploy the Railway template to build the current upstream code. Scheduled CI reruns the upstream tests and both clean image builds so compatibility breakage is detected without a manual commit, version, tag or digest update.

## License notices

This wrapper is MIT licensed in [LICENSE](LICENSE). [NOTICE](NOTICE) preserves the upstream Screenshot to Code MIT copyright and permission notice. The final Web image also includes that notice at `/usr/share/caddy/NOTICE` alongside the compiled upstream assets.
