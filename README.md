# Django Portfolio

Personal portfolio web application built with Django and deployed through
Vercel's Python WSGI runtime.

## Architecture

This project uses a hybrid content architecture:

- Portfolio content is loaded directly from JSON files in `django-portfolio/content/`.
- The database is kept only for Django admin authentication/session tables, contact messages, and resume uploads.
- Django views convert file-backed content into template-friendly objects.
- Templates render responsive server-side pages using Tailwind utility classes.
- WhiteNoise serves static files from the Django app.

## Project Structure

- `vercel.json` routes requests to the Django WSGI entrypoint.
- `api/wsgi.py` exposes the Django app to Vercel.
- `django-portfolio/core/` contains Django settings and project URLs.
- `django-portfolio/content/` contains file-backed portfolio data.
- `django-portfolio/portfolio_app/content_loader.py` loads and validates JSON content.
- `django-portfolio/portfolio_app/models.py` contains only database-backed operational models.
- `django-portfolio/portfolio_app/views.py` renders pages using file content plus database-backed contact/resume flows.
- `django-portfolio/static/` contains local static assets such as the profile image and resume fallback.

## Local Development

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   cd django-portfolio
   pip install -r requirements.txt
   ```

3. Create `django-portfolio/.env`:

   ```env
   DEBUG=True
   SECRET_KEY=local-dev-secret
   ```

4. Apply migrations:

   ```bash
   python manage.py migrate
   ```

5. Validate file-backed content:

   ```bash
   python manage.py validate_content
   ```

6. Run the app:

   ```bash
   python manage.py runserver
   ```

## Editing Portfolio Content

Edit these files directly:

- `django-portfolio/content/projects.json`
- `django-portfolio/content/certifications.json`
- `django-portfolio/content/achievements.json`
- `django-portfolio/content/education.json`
- `django-portfolio/content/skills.json`

For images or PDFs, put assets in `django-portfolio/static/` and reference them
with paths relative to that folder, for example:

```json
"featured_image": "images/projects/example.png"
```

## Database Usage

The database is intentionally limited to operational data:

- Django admin users, permissions, and sessions
- `ContactMessage`
- `Resume`

Projects, certifications, achievements, education, and skills do not use
database tables anymore.

## Vercel Environment Variables

Set these in Vercel Project Settings:

- `SECRET_KEY`
- `DEBUG=False`
- `DATABASE_URL`
- `CUSTOM_DOMAIN` if using a custom domain
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_USE_TLS`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `DEFAULT_FROM_EMAIL`
- `CONTACT_EMAIL`

`DATABASE_URL` is still required in production because Django admin, contact
messages, and resume uploads use the database.

After creating the production database, run migrations once with `DATABASE_URL`
pointed at that database:

```bash
cd django-portfolio
python manage.py migrate
```

## Backend Summary

The app uses Django's model-view-template pattern:

- Views load portfolio content from JSON files.
- The content loader gives templates model-like objects with display helpers.
- Contact messages are stored in the database and reviewed from Django admin.
- Resume PDFs can be uploaded from Django admin, with one active version served by the download endpoint.
- Templates render responsive pages with loops, filters, conditionals, and reusable layout blocks.
