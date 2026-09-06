# CivicConnect

A Django app for reporting and tracking local civic issues (waste, street lights, water problems, etc.), with public signup/login and an admin panel for verifying and resolving reports.

## What was fixed

The uploaded project had one bug that stopped it from starting at all: `config/settings.py` contained an **unresolved Git merge conflict** (`<<<<<<< HEAD` / `=======` / `>>>>>>>` markers around `STATIC_ROOT`), which is a Python syntax error. That block has been removed and `STATIC_ROOT` is defined once, correctly.

Also cleaned up for deployment:
- Removed the `venv/` folder, `.git/` history, and `__pycache__` files — these should never be committed/shipped; they bloated the zip enormously and aren't needed for deployment.
- Removed the local `db.sqlite3` and generated `staticfiles/` — these get created automatically by the migrate/collectstatic steps, so shipping stale copies just causes confusion.
- `SECRET_KEY` and `ALLOWED_HOSTS` now read from environment variables with safe fallbacks, so the same code works locally, on Render, or anywhere else without editing the file each time.
- Added `runtime.txt`, `Procfile`, and an updated `render.yaml` so it deploys cleanly on multiple platforms.

I ran `manage.py check`, `migrate`, `collectstatic`, the Django dev server, and gunicorn (the production server) locally — all passed, and the home page, signup, and login pages all returned HTTP 200.

## Project structure

```
config/         Django project settings, URLs, WSGI/ASGI entry points
problems/       The main app: models, views, admin, templates, migrations
static/         Source CSS/JS/images (collected into staticfiles/ at deploy time)
templates/      Site-wide templates (currently just the admin branding override)
media/          User-uploaded images (problem photos)
manage.py       Django's command-line entry point
requirements.txt   Python dependencies
render.yaml     One-click config for Render
Procfile        Start/release commands for Heroku/Railway-style platforms
runtime.txt     Pins the Python version (3.12.3)
```

## Run it locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`.

`DEBUG` is `False` by default unless you set `DJANGO_DEBUG=True`. The app will **not** crash either way now, but Django's own dev server only serves CSS/JS/image files itself when `DEBUG=True` — with `DEBUG=False` the page loads with no styling. For a normal-looking local dev site, do one of:

- set the env var before running the server: `DJANGO_DEBUG=True python manage.py runserver` (Windows PowerShell: `$env:DJANGO_DEBUG="True"; python manage.py runserver`; Windows CMD: `set DJANGO_DEBUG=True && python manage.py runserver`), or
- run `python manage.py collectstatic --no-input` once, so styling is served the same way it will be in production.

## Deploying

### Option A: Render (recommended — a `render.yaml` is already included)

1. Push this project to a GitHub/GitLab repo (a fresh one, since `.git` was removed).
2. Go to https://render.com → **New** → **Blueprint** → connect your repo. Render will read `render.yaml` automatically and set everything up (build command, start command, Python version, and a generated `SECRET_KEY`).
3. Alternatively, **New → Web Service** manually with:
   - Build command: `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate --no-input`
   - Start command: `gunicorn config.wsgi:application`
   - Add env var `DJANGO_SECRET_KEY` (any long random string).
4. Once deployed, Render gives you a `*.onrender.com` URL — the app already auto-detects it via `RENDER_EXTERNAL_HOSTNAME`, so you don't need to edit `ALLOWED_HOSTS`.

**Important caveat:** Render's free web services use an ephemeral filesystem — the SQLite database (`db.sqlite3`) and any uploaded images in `media/` will be wiped on every redeploy or restart. That's fine for a demo/hackathon, but for anything persistent you should either upgrade to a Render paid instance with a persistent disk, or switch to a hosted database (see below).

### Option B: Railway

1. Push to GitHub, then in Railway: **New Project → Deploy from GitHub repo**.
2. Railway auto-detects `Procfile`. Set env vars `DJANGO_SECRET_KEY` and `DJANGO_DEBUG=False`.
3. Same ephemeral-storage caveat as Render applies unless you add a Railway volume.

### Option C: PythonAnywhere / a VPS (persistent storage out of the box)

Good if you want the SQLite database and uploaded images to actually stick around without extra configuration. Follow PythonAnywhere's "Manual configuration" Django guide, pointing it at `config/wsgi.py`.

### Using a real database instead of SQLite (recommended for production)

For anything beyond a demo, swap SQLite for Postgres (Render/Railway both offer a free Postgres instance):

```bash
pip install psycopg2-binary dj-database-url
```

```python
# settings.py
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
}
```

Then set a `DATABASE_URL` env var on your host and it'll switch automatically.

## Environment variables

| Variable | Purpose | Default |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django's cryptographic secret key | insecure dev fallback (set this in production!) |
| `DJANGO_DEBUG` | `True`/`False` | `False` |
| `DJANGO_ALLOWED_HOSTS` | comma-separated extra hostnames (e.g. a custom domain) | none |
| `RENDER_EXTERNAL_HOSTNAME` | set automatically by Render | — |
