# Portfolio Content

Portfolio sections are loaded directly from these JSON files instead of from
database tables:

- `projects.json`
- `certifications.json`
- `achievements.json`
- `education.json`
- `skills.json`
- `now.json`

The project has no database. Contact messages are sent by email, and the
resume is the static file `static/resume.pdf`.

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

A certificate can link its PDF with `"certificate_file": "certificates/my-cert.pdf"`
(the file goes in `static/certificates/`). It shows as a "Certificate" link next to "Verify".


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

## Experience

`experience.json` powers the Experience section on the home and About pages.
Each entry: `role`, `company`, `employment_type` (`internship`, `full_time`,
`part_time`, `freelance` or `contract`), `location`, `start_date`, `end_date`
(leave `null` for a current role, shown as "Present"), `summary`, `highlights`,
`technologies` and an optional `certificate_link`.
