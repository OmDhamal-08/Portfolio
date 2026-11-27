# Om Dhamal - Developer Portfolio

A personal portfolio built with **Django**, showing my projects as short case
studies, my learning journey, and what I'm working on right now.

**Live site:** https://portfolio-five-nu-11.vercel.app/

![Django](https://img.shields.io/badge/Django-5.1-092E20?logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![HTMX](https://img.shields.io/badge/HTMX-2.0-3366CC)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-06B6D4?logo=tailwindcss&logoColor=white)
![GSAP](https://img.shields.io/badge/GSAP-3.12-88CE02?logo=greensock&logoColor=black)
![Vercel](https://img.shields.io/badge/Deployed_on-Vercel-000000?logo=vercel&logoColor=white)

---

## Features

**For visitors**
- **Project case studies.** Each project explains the problem, the solution, the architecture flow, the challenges and how I fixed them, the results, and what I learned.
- **Live project search.** Search and filter by keyword, type, status or technology; results update as you type, without reloading the page.
- **Now page** (`/now/`). What I'm currently learning (four areas, each with a Beginner / Intermediate level and progress bar) and my goals: internship, full-time role, freelance work and my own startup.
- **Journey pages.** Timelines for education and achievements, plus a certifications page with verify links.
- **Easy contact.** A contact form that emails me directly (and sends the visitor a copy), a one-click "Copy email" button, a "Write in Gmail" link (plus a mailto link for other email apps), and social links. If sending ever fails, the visitor's text is kept and pre-filled Gmail and mailto links are offered instead.
- **One-click resume.** View the PDF in the browser or download it straight away, with no server code involved.
- **Clean light design.** White and light-gray sections with a single navy accent; flat colors, no gradients or glow effects.
- **Subtle animations.** A short opening name reveal (once per visit, skippable, off for reduced motion), a staggered hero reveal, sections that fade up as you scroll, numbers that count up, progress bars that fill, a scrolling skills ticker, and small hover lifts on cards and buttons.
- **Accessible and responsive.** Works from 360px phones to desktops, meets WCAG AA text contrast, has visible keyboard focus outlines and a skip link, and shows simple fades instead of motion for visitors who ask for reduced motion.
- **Light and dark themes.** Follows the visitor's system setting, with a toggle in the nav that remembers their choice.
- **Smooth page transitions.** Pages cross-fade while the nav stays put (View Transitions API; other browsers navigate normally).
- **Experience section** on the home and About pages, from `content/experience.json`.
- **Live coding stats.** LeetCode solved count, GitHub contributions and repos, and Codeforces rating, loaded after the page renders and cached for a day.
- **Shareable and searchable.** A 1200x630 link-preview image, canonical URLs, `sitemap.xml`, `robots.txt` and schema.org Person data for Google.

**Under the hood**
- No database: portfolio content lives in JSON files and contact messages are delivered by email.
- Content is cached with Django's cache framework, with automatic invalidation when a file changes.
- HTMX partial rendering: the same view returns a full page or just the results grid.
- Content validation command and 38 automated tests.
- Production-ready settings: environment-based secrets, HTTPS, secure cookies, HSTS, WhiteNoise.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django 5.1 |
| Frontend | Django templates, Tailwind CSS, Alpine.js |
| Interactivity | HTMX (live search), Alpine.js (menus, tabs, form state) |
| Animation | GSAP + ScrollTrigger, Lenis (smooth scrolling) |
| Data | JSON content files (no database) |
| Caching | Django cache (local memory, or Redis when `REDIS_URL` is set) |
| Static files | WhiteNoise (also serves the resume PDF) |
| Email | Django email over SMTP (e.g. Gmail) |
| Hosting | Vercel (serverless Python) |
| External data | LeetCode GraphQL, GitHub REST, Codeforces API (cached daily) |

---

## Design

The whole site uses one small palette, defined as CSS variables at the top of
`static/css/site.css`. Tailwind's color names point at these variables, so no
other colors can be used by accident.

| Variable | Color | Used for |
|---|---|---|
| `--bg` | `#FFFFFF` | Page background, cards |
| `--surface` | `#F5F6F8` | Alternate sections, tags, footer |
| `--border` | `#E4E7EB` | Borders, dividers, progress-bar track |
| `--text` | `#0F172A` | Headings and main text |
| `--text-muted` | `#5B6472` | Paragraphs, labels, dates |
| `--accent` | `#1E3A8A` | Navy: buttons, links, active nav, bars, timeline dots |
| `--accent-soft` | `#E8EDF8` | Tech tag and badge backgrounds |
| `--success` | `#16A34A` | Only the "Open to work" dot |

Rules: flat colors only (no gradients or glows), navy used sparingly, and all
text meets WCAG AA contrast. `--text-light` (`#8A92A0`) is kept for non-text
details because it is too light for readable text.

Fonts: **Inter** for everything, **JetBrains Mono** for tech tags.

The dark theme redefines the same variables under `:root[data-theme="dark"]`
(deep navy-charcoal background, light-blue accent), so components need no
dark-specific styles. A tiny script in `<head>` applies the theme before the
first paint, so there is no flash of the wrong theme.

---

## Architecture

```text
Browser
  -> Vercel -> api/wsgi.py
  -> Django URL routing (portfolio_app/urls.py)
  -> View (portfolio_app/views.py)
       -> content_loader.py -> Django cache -> content/*.json
       -> Contact form -> email (SMTP)
  -> Template
       -> full page for normal requests
       -> partial template for HTMX requests (HX-Request header)
  -> HTML response (static files served by WhiteNoise)
```

### Why file-based content?

Portfolio content (projects, skills, certifications) changes rarely and benefits
from version control. Keeping it in JSON files means:

- Updating the site is one file edit and a `git push`; there's no admin panel or migration.
- The content history is visible in Git.
- There is no database to host, pay for or keep awake. Contact messages arrive
  by email, and the resume is a static PDF.

### Why no database?

An earlier version stored contact messages and resume uploads in Postgres.
On serverless hosting, uploaded files don't survive a redeploy, and a paused
free database took the resume download down with it. Email already delivers
every message, so the database added risk without adding value.

### How the caching works

`content_loader._read_json()` stores each parsed file in Django's cache. The
cache key includes the file's **modification time**:

```text
portfolio-content:projects.json:<mtime>
```

When a file is edited its modification time changes, so the next request uses a
new key and reads the fresh content. Stale data is never served, and the cache
never has to be cleared by hand.

### How the live search works

The search form has HTMX attributes. While the visitor types (with a 300 ms
pause), HTMX sends a GET request with an `HX-Request: true` header. The
`projects` view sees that header and returns only
`partials/project_results.html` instead of the whole page. HTMX swaps that into
the page and updates the URL, so filtered results can be shared or bookmarked.
The response sets `Vary: HX-Request` so caches keep the two versions apart.
Without JavaScript, the form still works as a normal GET form.

---

## Project Structure

```text
.
|-- api/
|   |-- requirements.txt         # Same as the root file, for Vercel
|   `-- wsgi.py                    # Vercel entry point
|-- django-portfolio/
|   |-- content/                   # All portfolio content (edit these)
|   |   |-- projects.json          # Projects + case-study fields
|   |   |-- now.json               # "Now / Currently learning" section
|   |   |-- experience.json        # Jobs, internships and freelance work
|   |   |-- skills.json
|   |   |-- certifications.json
|   |   |-- achievements.json
|   |   |-- education.json
|   |   `-- README.md              # Content field reference
|   |-- core/                      # Django settings and URLs
|   |-- portfolio_app/
|   |   |-- content_loader.py      # Reads, validates and caches JSON content
|   |   |-- coding_stats.py        # LeetCode / GitHub / Codeforces numbers, cached daily
|   |   |-- sitemaps.py            # sitemap.xml for pages and projects
|   |   |-- context_processors.py  # Social links / contact info for templates
|   |   |-- views.py
|   |   |-- forms.py               # Contact form + honeypot
|   |   |-- templatetags/          # rich_text and get_item filters
|   |   |-- templates/
|   |   |   |-- base.html
|   |   |   `-- partials/          # project card, HTMX results, page header, icons, socials
|   |   |-- management/commands/validate_content.py
|   |   `-- tests.py
|   |-- static/
|   |   |-- css/site.css           # Color variables (white + navy) and components
|   |   |-- js/site.js             # Animations, smooth scroll, HTMX hooks
|   |   |-- images/
|   |   |   `-- og-card.png        # 1200x630 link-preview image
|   |   |-- certificates/          # Certificate PDFs linked from the site
|   |   `-- resume.pdf             # Served directly by WhiteNoise
|   `-- manage.py
|-- requirements.txt
`-- vercel.json
```

---

## Getting Started

### 1. Clone and create a virtual environment

```powershell
git clone https://github.com/OmDhamal-08/Portfolio.git
cd Portfolio
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Add local settings

Create `django-portfolio/.env`:

```env
DEBUG=True
SECRET_KEY=local-dev-secret
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

With the console email backend, contact-form emails are printed in the terminal instead of being sent.

### 3. Set up and run

```powershell
cd django-portfolio
python manage.py validate_content
python manage.py runserver
```

Open http://127.0.0.1:8000/

### Updating your resume or photo

- **Resume:** replace `django-portfolio/static/resume.pdf` (keep the name) and push.
- **Photo:** replace `django-portfolio/static/images/profile.jpg` (square, about 600x600) and push.

---

## Updating Content

All content lives in `django-portfolio/content/`. Edit the JSON, then run:

```powershell
python manage.py validate_content
python manage.py test
```

### Adding a project case study

Every case-study field is optional. Fields you fill in appear as sections on the project page.

```json
{
  "title": "My Project",
  "slug": "my-project",
  "short_description": "One-line summary for the card.",
  "description": "Longer overview. Lines starting with '- ' become bullet points.",
  "project_type": "web",
  "status": "completed",
  "technologies": ["Django", "Python"],
  "github_link": "https://github.com/...",
  "live_demo": "",
  "featured_image": "images/projects/my-project.png",
  "start_date": "2026-01-01",
  "end_date": "2026-02-01",
  "featured": true,

  "role": "Solo developer",
  "problem": "Why this project exists.",
  "solution": "What I built.",
  "architecture": ["Step 1 of the flow", "Step 2"],
  "challenges": [{ "challenge": "What went wrong", "fix": "How I solved it" }],
  "results": ["Outcome"],
  "learnings": ["What I learned"],
  "next_steps": ["What I'd build next"]
}
```

`project_type` can be: `web`, `ml`, `mobile`, `automation`, `ai`, `data` or `other`.
`status` can be: `completed`, `in_progress` or `planned`.

Image paths are relative to `django-portfolio/static/`.

### Updating the Now page

Edit `content/now.json`: change `updated`, `focus`, the `learning` items (each
with a `level` of beginner, intermediate or advanced and a `progress` value from 0 to 100) and `goals`
(plain strings or `{"title": ..., "note": ...}`).

See [`django-portfolio/content/README.md`](django-portfolio/content/README.md) for the full field reference.

---

## Testing

```powershell
cd django-portfolio
python manage.py test portfolio_app
```

The 38 tests cover:
- Content loading, validation and slug lookup
- Every page renders with the expected content
- Case-study fields and validation of bad entries
- The Now page and the home page "Currently learning" block
- Project search by keyword and technology
- HTMX requests return only the partial, with the `Vary` header
- Caching: a second load does not read the file again, and editing the file invalidates the cache
- Resume buttons link straight to the PDF, and the old `/download-resume/` URL redirects to it
- The contact form emails me and the visitor, and a failed send keeps the text and offers a mailto link
- Experience loading and display, live coding stats (cached, with fallback when a service is down)
- Link-preview tags, sitemap.xml, robots.txt and the structured data

Other useful checks:

```powershell
python manage.py check
```

---

## Deployment (Vercel)

- `vercel.json` routes every request to `api/wsgi.py`.
- `api/wsgi.py` loads the Django project from `django-portfolio/`.
- WhiteNoise serves the static files.

Set these in **Vercel -> Project Settings -> Environment Variables**:

| Variable | Required | Notes |
|---|---|---|
| `DEBUG` | yes | `False` in production |
| `SECRET_KEY` | yes | A long random string (generate one with the command below) |
| `CONTACT_EMAIL` | optional | Where contact form messages are sent (default `dhamalomm@gmail.com`) |
| `DEFAULT_FROM_EMAIL` | yes | Sender address |
| `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` | yes, for email | SMTP login, e.g. your Gmail address and a Gmail app password |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS` | optional | Defaults: `smtp.gmail.com`, `587`, `True` |
| `CUSTOM_DOMAIN` | optional | Adds the domain to allowed hosts and CSRF trusted origins |
| `ALLOWED_HOSTS` | optional | Extra hosts, comma-separated |
| `REDIS_URL` | optional | Use Redis instead of the in-memory cache |
| `CONTENT_CACHE_TIMEOUT` | optional | Content cache lifetime in seconds (default `3600`) |

Generate a secret key:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Interview Notes

**In one sentence:** a hybrid Django portfolio where static content is
file-based and cached, contact messages go by email with no database, and HTMX adds
single-page-app-style search without a JavaScript framework.

Talking points:
1. **Choosing storage by need.** Content goes in version-controlled JSON; contact messages go by email; the resume is a static file. I removed the database once it added risk (a paused free database broke the resume download) without adding value.
2. **Cache invalidation.** The modification time in the cache key means fresh data without ever clearing the cache by hand.
3. **Progressive enhancement.** HTMX search falls back to a normal form; animations respect reduced-motion settings.
4. **Validation and testing.** A `validate_content` command catches bad JSON before deploying, and 38 tests cover pages, search, caching, the resume links and the contact form.
5. **Production security.** Secrets come from environment variables, with HTTPS redirect, secure cookies, HSTS, a contact-form honeypot and rate limiting. The contact form never claims a message was sent when it wasn't.

---

## Contact

- **Email:** dhamalomm@gmail.com
- **LinkedIn:** [om-dhamal](https://www.linkedin.com/in/om-dhamal-411545295/)
- **GitHub:** [OmDhamal-08](https://github.com/OmDhamal-08)
- **LeetCode:** [omdhamal77](https://leetcode.com/u/omdhamal77/)
