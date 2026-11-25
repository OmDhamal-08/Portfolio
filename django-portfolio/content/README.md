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


## Project case studies

Every field below is optional. When present, the project page shows it as a
case-study section.

```json
"role": "Solo developer",
"problem": "Why the project exists.",
"solution": "What you built, in one paragraph.",
"architecture": ["Step 1 of the request/data flow", "Step 2"],
"challenges": [{"challenge": "What went wrong", "fix": "How you solved it"}],
"results": ["Outcome or metric"],
"learnings": ["What you learned"],
"next_steps": ["What you would build next"]
```

## Now page

`now.json` powers `/now/` and the "Currently learning" block on the home page.
Update `updated`, `focus`, `learning` (each with `level`: beginner / intermediate / advanced,
and `progress` 0-100) and `goals` (strings or `{"title", "note"}`) whenever your focus changes.

## Caching

Parsed JSON is stored in Django's cache. The cache key includes each file's
modification time, so edits appear immediately without clearing the cache.
Set `CONTENT_CACHE_TIMEOUT` (seconds) to change how long entries live.
