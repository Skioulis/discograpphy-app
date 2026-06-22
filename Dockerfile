# Discography app — production image (gunicorn).
# Built for arm64 (64-bit Raspberry Pi OS / CasaOS). The python slim images are
# multi-arch, so this also builds on amd64 for local testing.
FROM python:3.13-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    FLASK_ENV=production \
    FLASK_APP=run-prod.py

WORKDIR /app

# libpq5 is the runtime Postgres client lib. build-essential + libpq-dev are only
# needed as a fallback in case a binary wheel (e.g. psycopg2) isn't available for
# this platform; they're purged afterwards to keep the image small.
COPY requirements.txt .
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && pip install -r requirements.txt \
    && apt-get purge -y build-essential libpq-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN chmod +x /app/docker/entrypoint.sh

EXPOSE 9292

ENTRYPOINT ["/app/docker/entrypoint.sh"]
