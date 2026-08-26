# author: Just Ship It
# project: screenshot-to-code-railway
# purpose: Build pinned upstream frontend and serve it behind authenticated Caddy.
# used_by: Railway Web service
# status: active
# verified: pending
FROM node:22.15.0-bookworm-slim@sha256:01cbafb3480d272d73613e5e74206ec79326f4a9ebb4d089f636b53d12d87a04 AS build

ARG UPSTREAM_COMMIT=d026163f586dfa8c5c10d28c36edd59a9d3b0e88
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone https://github.com/abi/screenshot-to-code.git . && git checkout "$UPSTREAM_COMMIT"
WORKDIR /src/frontend
RUN corepack enable && corepack prepare pnpm@10.32.1 --activate && pnpm install --frozen-lockfile && pnpm build

FROM caddy:2.8.4-alpine@sha256:b95ed06fbc6d74d24a40902090c8cc6086ce7d08ba60a3a7e8e62bf164a9d7bb
COPY --from=build /src/frontend/dist /usr/share/caddy
COPY NOTICE /usr/share/caddy/NOTICE
COPY Caddyfile /etc/caddy/Caddyfile
COPY docker-entrypoint.sh /usr/local/bin/screenshot-to-code-web
RUN chmod 755 /usr/local/bin/screenshot-to-code-web
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/screenshot-to-code-web"]
