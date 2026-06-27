# Frontend Guide

## Frontend Approach

The frontend is built with Django templates, Tailwind utility classes, small
vanilla JavaScript helpers, and AOS scroll animations.

The portfolio is server-rendered:

```text
Request -> Django view -> content_loader.py / database model -> template -> HTML
```

Portfolio pages use file-backed JSON content. Contact and resume features still
use database-backed Django models.

## Why No React?

This project is content-focused. Django templates are enough because the app does
not need heavy client-side state management. The frontend stays simpler, easier
to deploy, and easier to explain.

## Template Structure

```text
portfolio_app/templates/
  base.html
  index.html
  about.html
  skills.html
  projects.html
  project_detail.html
  certifications.html
  achievements.html
  education.html
  contact.html
```

`base.html` contains the shared layout, navbar, scripts, messages, and reusable
template blocks. Page templates extend it and fill `{% block content %}`.

## Page Data Sources

| Page | Source |
| --- | --- |
| Home | Featured content from JSON files |
| Skills | `content/skills.json` |
| Projects | `content/projects.json` |
| Project Detail | `content/projects.json` by slug |
| Certifications | `content/certifications.json` |
| Achievements | `content/achievements.json` |
| Education | `content/education.json` |
| Contact | Django form + `ContactMessage` model |
| Resume Download | `Resume` model, then static fallback |

## How Filters Work

The filter dropdowns update URL query parameters with JavaScript.

Examples:

```text
/projects/?type=ml&status=completed
/certifications/?type=online&level=beginner
/achievements/?category=hackathon
```

The Django view reads `request.GET`, filters the loaded JSON objects in Python,
and sends the result to the template.

## Skills Animation

The skills page uses an `IntersectionObserver` to animate progress bars when
they enter the viewport. This keeps the page light and avoids a larger frontend
framework.

## Static Assets

Static files live in:

```text
django-portfolio/static/
```

File-backed content can reference static assets with paths relative to that
folder:

```json
"featured_image": "images/projects/example.png"
```

The content loader converts that into:

```text
/static/images/projects/example.png
```

## Useful Commands

```bash
python manage.py validate_content
python manage.py runserver
python manage.py test
```

## Explanation For Interviews

The frontend is a Django template frontend. It uses a shared `base.html`, page
templates for each section, Tailwind classes for styling, and small JavaScript
helpers for filters and animations. The actual portfolio content is loaded from
JSON files through `content_loader.py`, which lets the templates render dynamic
cards and detail pages without needing portfolio database tables.
