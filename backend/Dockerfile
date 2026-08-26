# author: Just Ship It
# project: screenshot-to-code-railway
# purpose: Build the pinned upstream FastAPI and Playwright backend.
# used_by: Railway Backend service
# status: active
# verified: pending
FROM python:3.12.3-slim-bookworm@sha256:fd3817f3a855f6c2ada16ac9468e5ee93e361005bd226fd5a5ee1a504e038c84

ARG UPSTREAM_COMMIT=d026163f586dfa8c5c10d28c36edd59a9d3b0e88
ENV POETRY_VERSION=1.8.0 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir "poetry==$POETRY_VERSION"
WORKDIR /app
RUN git clone https://github.com/abi/screenshot-to-code.git . && git checkout "$UPSTREAM_COMMIT"
WORKDIR /app/backend
RUN poetry install --only main --no-interaction --no-ansi && playwright install --with-deps chromium
ENV SCREENSHOT_TO_CODE_DATA_DIR=/data \
    LOCAL_ASSET_DIR=/data/local_assets \
    BACKEND_PORT=7001
EXPOSE 7001
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7001"]
