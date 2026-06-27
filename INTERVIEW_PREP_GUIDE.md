# Interview Prep Guide

## One-Line Pitch

This is a Django portfolio that uses a file-based content system for projects,
certifications, achievements, education, and skills, while keeping the database
only for operational features like contact messages, admin login, and resume
uploads.

## Why This Architecture Is Strong

- Portfolio content is version-controlled in `content/*.json`.
- The database is not overloaded with content that can live safely in files.
- The admin panel is still useful for messages and resume management.
- The project demonstrates Django MVT, forms, admin, migrations, static files,
  email handling, validation, and deployment.
- It is easy to explain because each responsibility has a clear boundary.

## Current Project Structure

```text
Port/
  api/
    wsgi.py
  django-portfolio/
    content/
      projects.json
      certifications.json
      achievements.json
      education.json
      skills.json
    core/
      settings.py
      urls.py
    portfolio_app/
      content_loader.py
      models.py
      views.py
      forms.py
      admin.py
      templates/
      management/
        commands/
          validate_content.py
    static/
      css/
      images/
      resume.pdf
```

## Main Files To Explain

### `content_loader.py`

This is the custom file-based content layer. It reads JSON files, validates
required fields, parses dates, converts image paths into static URLs, and returns
objects that behave like the old model objects in templates.

Important examples:

- `list_projects(project_type, status)`
- `get_project(slug)`
- `list_certifications(cert_type, level)`
- `list_achievements(category)`
- `list_education()`
- `group_skills_by_category()`

### `models.py`

The active models are intentionally small:

- `ContactMessage`
- `Resume`

Admin users, sessions, and permissions are provided by Django's built-in apps.

### `views.py`

Views combine two sources:

- File-backed portfolio content from `content_loader.py`
- Database-backed contact and resume behavior from Django models

Example flow:

```text
/projects/ -> projects() -> content.list_projects() -> projects.html
```

### `admin.py`

The admin only manages:

- Contact messages
- Resume uploads

It does not manage projects, certifications, achievements, education, or skills.
Those are edited directly in JSON files.

## How To Explain Page Rendering

When a user opens `/projects/`, Django routes the request to `projects()`.
The view reads optional query parameters like `type` and `status`, asks
`content_loader.py` for matching projects, and renders `projects.html`.

The template does not care whether the project came from a database or a file.
It receives objects with fields like `title`, `slug`, `short_description`,
`github_link`, and helper methods like `get_tech_list()`.

## Why JSON Instead Of Database For Portfolio Content?

Use the database for data that changes through user/admin actions. Use files for
content that is part of the portfolio source itself.

In this project:

- Projects are portfolio content, so JSON is simpler.
- Skills are portfolio content, so JSON is simpler.
- Certifications and education are portfolio content, so JSON is simpler.
- Contact messages are user-submitted data, so the database is correct.
- Resume uploads are admin-managed files, so the database is useful.

## What Happens In Production?

Vercel loads `api/wsgi.py`, which points to the Django app. Django settings read
environment variables, configure the database from `DATABASE_URL`, and serve
static files through WhiteNoise.

Portfolio pages can render from JSON files without needing database rows.
Contact and resume features still use the production database.

## Commands To Know

```bash
python manage.py migrate
python manage.py validate_content
python manage.py test
python manage.py runserver
python manage.py createsuperuser
```

## Best Interview Answer

> I designed this portfolio as a hybrid Django app. The portfolio sections are
> file-backed, so projects, skills, certifications, achievements, and education
> are loaded directly from JSON files. This keeps the content easy to edit,
> version-controlled, and deployment-friendly. I kept the database for the parts
> that actually need persistence: contact form messages, admin authentication,
> and resume uploads. The result is simpler than a full CMS, but still shows
> real backend engineering with Django views, forms, admin, migrations,
> validation, static files, email handling, and deployment.

## Likely Questions

**Why not use Django admin for everything?**  
Because the portfolio content is mostly static and version-controlled. Admin is
better for operational data like messages and uploaded resumes.

**Can filters still work without a database?**  
Yes. The view reads JSON data into Python objects and filters the list in memory.
For a portfolio-sized dataset, this is fast and simple.

**Can this scale later?**  
Yes. The templates already receive model-like objects. If the project later needs
a CMS or API, the loader can be replaced without rewriting the UI.

**What is the database used for now?**  
Django admin login/session data, contact messages, and resume upload records.

**How do you avoid broken content?**  
The `validate_content` command loads every JSON file and reports errors before
deployment.
