# BUILD STAGE
FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.12.24 /uv /uvx /bin/

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev --no-install-project

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable

# PRODUCTION STAGE
FROM python:3.14-slim

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd -m -r appuser

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder --chown=appuser:appuser /app .

RUN mkdir -p /app/staticfiles /app/static &&\
    chown -R appuser:appuser /app/staticfiles /app/static

USER appuser

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
