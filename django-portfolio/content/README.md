# Portfolio Content

Portfolio sections are loaded directly from these JSON files instead of from
database tables:

- `projects.json`
- `certifications.json`
- `achievements.json`
- `education.json`
- `skills.json`

The database is still used for:

- Django admin users, permissions, and sessions
- Contact form messages
- Resume uploads

After editing content, run:

```bash
python manage.py validate_content
python manage.py test
```

Static image and PDF paths should be relative to `django-portfolio/static/`.
For example:

```json
"featured_image": "images/projects/portfolio.png"
```

