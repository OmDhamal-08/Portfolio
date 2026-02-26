## Django Portfolio – Vercel Deployment

This is a Django portfolio web application configured to run on Vercel using the Python (WSGI) runtime.

### Project structure

- **Root**: `vercel.json`, `api/wsgi.py`, deployment docs (`README.md`), legacy Render scripts (`render.yaml`, `build.sh`, `start.sh`, `runtime.txt`)
- **Django project**: `django-portfolio/`
  - Django settings and URLs in `core/`
  - Application code in `portfolio_app/`

### Local development

1. Create and activate a virtual environment (Python 3.11 or newer).
2. Install dependencies:
   - `cd django-portfolio`
   - `pip install -r requirements.txt`
3. Create a `.env` file next to `manage.py` (inside `django-portfolio`) with at least:
   - `SECRET_KEY=your-secret-key`
   - `DEBUG=True`
   - Optionally: `DATABASE_URL`, `CUSTOM_DOMAIN`, `EMAIL_*`, `DEFAULT_FROM_EMAIL`, `REDIS_URL`
4. Apply migrations and run the server:
   - `python manage.py migrate`
   - `python manage.py runserver`

### Deploying to Vercel

1. Push this project to a Git repository (GitHub, GitLab, etc.).
2. In the Vercel dashboard, import the repository as a new project.
3. In **Project Settings → Environment Variables**, configure at least:
   - `SECRET_KEY`
   - `DEBUG` set to `False`
   - Optional: `DATABASE_URL`, `CUSTOM_DOMAIN`, `EMAIL_*`, `DEFAULT_FROM_EMAIL`, `REDIS_URL`
4. Ensure the root directory is the repository root (where `vercel.json` and `api/` live).
5. Trigger a deployment. Vercel will:
   - Install Python dependencies from `django-portfolio/requirements.txt`
   - Use `api/wsgi.py` as the WSGI entrypoint (see `vercel.json`)

All incoming requests are routed to the Django application, which serves both dynamic content and static files via WhiteNoise.

