# BUILD STAGE
FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.13.4 /uv /uvx /bin/
RUN python -m pip install --upgrade "pip>=26.2.2"

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
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

RUN python manage.py compilemessages

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable

# PRODUCTION STAGE
FROM python:3.14-slim

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=1000
ARG GID=1000

RUN useradd -m -r -u ${UID} appuser

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder --chown=appuser:appuser /app/entrypoint.sh /app/entrypoint.sh
COPY --from=builder --chown=appuser:appuser /app/templates /app/templates
COPY --from=builder --chown=appuser:appuser /app/static /app/static

RUN mkdir -p /app/staticfiles /app/static &&\
    chmod +x /app/entrypoint.sh &&\
    chown -R appuser:appuser /app/staticfiles &&\
    DJANGO_SETTINGS_MODULE=fellowship_app.settings python -m django check

USER appuser

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
