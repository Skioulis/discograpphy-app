# Deploying to a Raspberry Pi (Docker + CasaOS)

This app ships as a Docker stack: the Flask app (served by gunicorn) plus a
PostgreSQL database. Configuration is read from a `.env` file, the database is
persisted in a named volume, and external media (mp3s / images) live in a
bind-mounted host directory.

## 0. Confirm the Pi is 64-bit

The `postgres:16-alpine` image requires arm64. On the Pi:

```bash
uname -m
```

- `aarch64` → good (64-bit Raspberry Pi OS).
- `armv7l` → 32-bit OS; the Postgres image won't pull. Switch to an
  armv7-compatible Postgres image in `docker-compose.yml` first.

---

## Path A — build on the Pi (recommended)

### 1. Verify Docker + Compose

CasaOS bundles them. Check:

```bash
docker version && docker compose version
```

### 2. Clone the repo

```bash
git clone https://github.com/Skioulis/discograpphy-app.git
cd discograpphy-app
```

### 3. Create the real `.env`

The `.env` is gitignored and never leaves your dev machine, so create it on the Pi:

```bash
cp .env.docker.example .env
nano .env
```

Fill in:

| Variable          | Notes                                                              |
| ----------------- | ------------------------------------------------------------------ |
| `DB_USER`         | Any value.                                                         |
| `DB_NAME`         | Any value.                                                         |
| `DB_PASSWORD`     | A strong password.                                                 |
| `SECRET_KEY`      | Generate: `python3 -c "import secrets; print(secrets.token_hex(32))"` |
| `WEB_PORT`        | Host port, e.g. `9292`.                                            |
| `MEDIA_HOST_PATH` | Host dir for mp3s/images, e.g. `/DATA/AppData/discography/media`.  |

### 4. Create the media directory

Must match `MEDIA_HOST_PATH` so the bind mount has a real target:

```bash
mkdir -p /DATA/AppData/discography/media
```

### 5. Build and start

```bash
docker compose up -d --build
```

The first build is slow on a Pi (pulling/compiling Python wheels). On startup the
app waits for Postgres, runs `flask db upgrade` (creating the schema from the
baseline migration), then starts gunicorn on `WEB_PORT`.

### 6. Verify

```bash
docker compose ps
docker compose logs -f web      # expect: Listening at: http://0.0.0.0:9292
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:9292/
```

App is reachable at `http://<pi-ip>:<WEB_PORT>`.

---

## Connecting a database client

The `db` service publishes Postgres on the host so you can connect a client
(DBeaver, DataGrip, pgAdmin) directly. The host port is set by `DB_PORT_HOST`
in `.env` (defaults to `5432`).

Connection settings:

| Field    | Value                                                    |
| -------- | -------------------------------------------------------- |
| Host     | `<pi-ip>` (or `localhost` if the client runs on the Pi)  |
| Port     | `DB_PORT_HOST` (default `5432`)                          |
| Database | `DB_NAME`                                                |
| User     | `DB_USER`                                                |
| Password | `DB_PASSWORD`                                            |

Apply a change to the port mapping by recreating the container (`restart` does
not pick up port changes):

```bash
docker compose up -d
```

Notes:

- If `5432` is already taken on the host (e.g. a native Postgres), set a
  different `DB_PORT_HOST` such as `5433` in `.env` and connect on that port.
- This exposes the database to your LAN — fine on a trusted home network. If the
  Pi is ever internet-facing, do **not** expose it; tunnel over SSH instead
  (bind `127.0.0.1:5432:5432` and use your client's SSH-tunnel feature).

---

## Path B — cross-build on a dev machine, push to a registry

Only worth it if the Pi is too slow to build. From the dev machine:

```bash
docker buildx build --platform linux/arm64 \
  -t <registry-user>/discography:latest --push .
```

Then on the Pi, replace `build: .` with `image: <registry-user>/discography:latest`
in `docker-compose.yml` and run `docker compose up -d`.

---

## CasaOS integration

Once running via Compose, CasaOS detects the containers automatically. To manage
it as a CasaOS app, use **App Store → Custom Install → Import** and paste
`docker-compose.yml`. Notes:

- Set env values in the CasaOS UI, or keep the `.env` next to the compose file.
- Keep `MEDIA_HOST_PATH` under `/DATA/...` — that is CasaOS's persistent storage
  area, where you'll drop mp3s/images.

---

## Day-2 operations

```bash
git pull && docker compose up -d --build   # redeploy after code changes
docker compose down                         # stop (data is kept)
docker compose logs -f web                  # tail app logs
docker compose restart web                  # restart just the app
```

### Volumes

- **Database** persists in the `pgdata` named volume across restarts and rebuilds.
  `docker compose down -v` is the only command that wipes it — never use `-v` in
  production.
- **Media** lives in the host directory at `MEDIA_HOST_PATH`, mounted into the
  container at `/app/media`. Add/replace files on the host directly.

### Backups

```bash
# Back up the database
docker compose exec db pg_dump -U <DB_USER> <DB_NAME> > backup.sql

# Restore
cat backup.sql | docker compose exec -T db psql -U <DB_USER> <DB_NAME>
```

---

## Notes

- The Docker Postgres starts **empty** and builds a fresh schema from the baseline
  migration (`migrations/versions/e0f0808b9f6a_baseline_schema_from_models.py`).
  The legacy external database is not touched. Migrating real data into this stack
  is a separate task.
- The image is based on `python:3.13-slim` and is architecture-neutral; the
  Dockerfile includes a build-tools fallback so wheels that lack an arm64 binary
  can compile on the Pi.
