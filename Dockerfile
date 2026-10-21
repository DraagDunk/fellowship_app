# BUILD STAGE
FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.13.4 /uv /uvx /bin/
RUN python -m pip install --upgrade "pip>=26.2.2"

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv

RUN apt-get update && apt-get install -y --no-install-recommends gettext \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev --no-install-project

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable

RUN python manage.py compilemessages

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
