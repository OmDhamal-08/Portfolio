# Om Dhamal Portfolio

A Django portfolio website deployed on Vercel. The public portfolio sections are
loaded from JSON files, while the database is kept only for operational features
such as contact messages, admin login, and resume uploads.

## Highlights

- Server-rendered Django pages using the MVT pattern
- File-based content system for projects, certifications, achievements,
  education, and skills
- Contact form with validation, honeypot spam protection, rate limiting, email
  delivery, and database-backed message storage
- Admin-managed resume upload with static PDF fallback
- WhiteNoise static file serving for Vercel deployment
- Focused test coverage for content loading and main pages

## Architecture

```text
Browser
  -> Vercel / api/wsgi.py
  -> Django URL routing
  -> portfolio_app.views
  -> content_loader.py reads django-portfolio/content/*.json
  -> Django templates render HTML
```

Database usage is intentionally limited:

- Django admin users, permissions, and sessions
- `ContactMessage`
- `Resume`

Portfolio content does not need database tables. It lives in version-controlled
JSON files under `django-portfolio/content/`.

## Project Structure

```text
.
|-- api/
|   |-- requirements.txt
|   `-- wsgi.py
|-- django-portfolio/
|   |-- content/
|   |   |-- achievements.json
|   |   |-- certifications.json
|   |   |-- education.json
|   |   |-- projects.json
|   |   `-- skills.json
|   |-- core/
|   |-- portfolio_app/
|   |   |-- content_loader.py
|   |   |-- forms.py
|   |   |-- models.py
|   |   |-- views.py
|   |   |-- templates/
|   |   `-- management/commands/validate_content.py
|   |-- static/
|   |-- manage.py
|   `-- requirements.txt
|-- requirements.txt
`-- vercel.json
```

## Local Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create `django-portfolio/.env`:

```env
DEBUG=True
SECRET_KEY=local-dev-secret
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Run migrations and validate content:

```powershell
cd django-portfolio
python manage.py migrate
python manage.py validate_content
python manage.py check
```

Start the local server:

```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Editing Portfolio Content

Update portfolio data directly in:

- `django-portfolio/content/projects.json`
- `django-portfolio/content/certifications.json`
- `django-portfolio/content/achievements.json`
- `django-portfolio/content/education.json`
- `django-portfolio/content/skills.json`

After editing content, run:

```powershell
python manage.py validate_content
python manage.py test
```

Static asset paths in JSON are relative to `django-portfolio/static/`.

Example:

```json
"featured_image": "images/projects/example.png"
```

## Environment Variables

For local development, use `DEBUG=True` and SQLite.

For Vercel or any production environment, add these in
`Project Settings -> Environment Variables`:

```env
DEBUG=False
SECRET_KEY=your-secure-secret-key
DATABASE_URL=your-production-database-url
CONTACT_EMAIL=your-email@example.com
DEFAULT_FROM_EMAIL=your-email@example.com
```

You can generate a Django secret key locally with:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

If you connect Vercel Postgres, Vercel may provide `POSTGRES_URL`
automatically. The app accepts either `DATABASE_URL` or `POSTGRES_URL`.

Optional email settings:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Deployment

The repository is configured for Vercel:

- `vercel.json` routes all traffic to `api/wsgi.py`
- `api/wsgi.py` loads the Django project from `django-portfolio/`
- `requirements.txt` contains direct dependency pins for Vercel
- WhiteNoise serves static assets

Before deploying, make sure the production database has migrations applied:

```powershell
cd django-portfolio
python manage.py migrate
```

## Validation

Useful commands:

```powershell
python manage.py validate_content
python manage.py check
python manage.py test
python manage.py makemigrations --check --dry-run
```

## Interview Explanation

This is a hybrid Django portfolio. Static portfolio content is file-backed and
version-controlled, which makes projects and certifications easy to update
without database records. The database is reserved for data that truly needs
persistence: contact submissions, admin authentication, and resume uploads. The
result is simpler than a full CMS while still showing real Django backend skills:
views, forms, templates, migrations, admin, validation, email, static files, and
deployment.
