## Django Portfolio – Render Deployment

This is a Django portfolio web application configured to run on Render using a PostgreSQL database and Gunicorn.

### Project structure

- **Root**: Render config and deploy scripts (`render.yaml`, `build.sh`, `start.sh`, `runtime.txt`, `README.md`)
- **Django project**: `django-portfolio/`
  - Django settings and URLs in `core/`
  - Application code in `portfolio_app/`

### Local development

1. Create and activate a virtual environment (Python 3.11).
2. Install dependencies:
   - `cd django-portfolio`
   - `pip install -r requirements.txt`
3. Set environment variables (for example in a `.env` file in `django-portfolio`):
   - `SECRET_KEY=your-secret-key`
   - `DEBUG=True`
4. Apply migrations and run the server:
   - `python manage.py migrate`
   - `python manage.py runserver`

### Deploying to Render

1. Push this project to a Git repository (GitHub, GitLab, etc.).
2. On Render, create a **Blueprint** from this repo; `render.yaml` will:
   - Create a **Web Service** (`portfolio-website`) with:
     - `buildCommand: ./build.sh`
     - `startCommand: ./start.sh`
     - `env: python`, `runtime.txt` set to Python 3.11.8
   - Create a **PostgreSQL** instance (`portfolio-db`).
3. In the Render dashboard for the web service, ensure these environment variables exist:
   - `SECRET_KEY` (auto-generated from `render.yaml`, or set manually)
   - `DEBUG` set to `"False"`
   - Optional: `CUSTOM_DOMAIN`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`
4. The build process (`build.sh`) will:
   - `cd django-portfolio`
   - Install dependencies from `requirements.txt`
   - Collect static files
   - Run migrations
5. The start process (`start.sh`) will:
   - `cd django-portfolio`
   - Run migrations
   - Start Gunicorn with `core.wsgi:application` bound to `$PORT`.

Once the first deploy succeeds, your portfolio will be available at the Render URL (and any custom domain you configure).

