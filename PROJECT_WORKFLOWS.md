# Django Portfolio Project Workflows

Quick workflow reference for explaining the current project architecture.

## 1. Overall Architecture

```mermaid
flowchart TB
    User["Browser user"] --> Vercel["Vercel deployment"]
    Vercel --> Entry["api/wsgi.py"]
    Entry --> WSGI["core.wsgi.application"]
    WSGI --> URLs["Django URL resolver"]
    URLs --> Views["portfolio_app.views"]
    Views --> Loader["content_loader.py"]
    Loader --> Files["content/*.json"]
    Views --> ORM["Django ORM"]
    ORM --> DB["Database: admin, contact messages, resumes"]
    Views --> Templates["Django templates"]
    Templates --> Static["static CSS, images, resume fallback"]
    Templates --> User
```

## 2. Content Strategy

```mermaid
flowchart LR
    Files["JSON content files"] --> Loader["content_loader.py"]
    Loader --> Objects["Template-friendly objects"]
    Objects --> Views["Views"]
    Views --> Templates["Projects, certifications, achievements, education, skills"]

    Contact["Contact form"] --> ContactModel["ContactMessage model"]
    Resume["Resume upload"] --> ResumeModel["Resume model"]
    Admin["Django admin"] --> ContactModel
    Admin --> ResumeModel
```

## 3. Database Boundary

```mermaid
erDiagram
    CONTACTMESSAGE {
        int id
        string name
        string email
        string subject
        text message
        string reply_status
        string email_status
        bool is_read
    }

    RESUME {
        int id
        string title
        file file
        string version
        bool is_active
    }
```

The removed portfolio tables are no longer active application models. Migration
`0010_remove_database_backed_portfolio_content.py` keeps older databases
upgradeable by removing those old tables safely.

## 4. Request Response Lifecycle

```mermaid
sequenceDiagram
    participant B as Browser
    participant U as URLConf
    participant V as View
    participant L as Content Loader
    participant F as JSON Files
    participant T as Template

    B->>U: GET /projects/
    U->>V: projects(request)
    V->>L: list_projects(type, status)
    L->>F: read content/projects.json
    F-->>L: structured data
    L-->>V: ProjectContent objects
    V->>T: render projects.html
    T-->>B: HTML response
```

## 5. URL Routing Map

```mermaid
flowchart LR
    Browser["Incoming URL"] --> Core["core.urls"]
    Core --> Admin["/admin/"]
    Core --> Include["portfolio_app.urls"]

    Include --> Home["/"]
    Include --> About["/about/"]
    Include --> Skills["/skills/"]
    Include --> Projects["/projects/"]
    Include --> Detail["/projects/<slug>/"]
    Include --> Certs["/certifications/"]
    Include --> Achievements["/achievements/"]
    Include --> Education["/education/"]
    Include --> Contact["/contact/"]
    Include --> Resume["/download-resume/"]
```

## 6. Page Workflows

```mermaid
flowchart TB
    Home["home()"] --> AllFiles["Load featured projects, certs, achievements, education"]
    Skills["skills()"] --> SkillFile["Load and group skills.json"]
    Projects["projects()"] --> ProjectFilter["Load projects.json and apply type/status filters"]
    Detail["project_detail()"] --> ProjectSlug["Find project by slug and related projects"]
    Certs["certifications()"] --> CertFilter["Load certifications.json and apply type/level filters"]
    Achievements["achievements()"] --> AchFilter["Load achievements.json and apply category filter"]
    Education["education()"] --> EducationStats["Load education.json and calculate stats"]
```

## 7. Contact Form Workflow

```mermaid
flowchart TB
    Get["GET /contact/"] --> EmptyForm["Render empty ContactForm"]
    Post["POST /contact/"] --> Validate["Validate form and honeypot"]
    Validate --> RateLimit{"Rate limit passed?"}
    RateLimit -- no --> Error["Show error"]
    RateLimit -- yes --> Save["Create ContactMessage"]
    Save --> Email["Try owner and confirmation emails"]
    Email --> Status["Mark sent or failed"]
    Status --> Redirect["Redirect with success message"]
```

## 8. Resume Download Workflow

```mermaid
flowchart TB
    Request["GET /download-resume/"] --> Active["Find active Resume record"]
    Active --> HasFile{"Uploaded PDF exists?"}
    HasFile -- yes --> Uploaded["Return uploaded PDF"]
    HasFile -- no --> StaticPdf{"static/resume.pdf exists?"}
    StaticPdf -- yes --> Static["Return static resume.pdf"]
    StaticPdf -- no --> Text["Return text fallback"]
```

## 9. Local Setup Workflow

```mermaid
flowchart TB
    Clone["Clone project"] --> Env["Create .env with DEBUG=True"]
    Env --> Install["Install requirements"]
    Install --> Migrate["python manage.py migrate"]
    Migrate --> Validate["python manage.py validate_content"]
    Validate --> Run["python manage.py runserver"]
```

## 10. Interview Pitch

This is a Django portfolio with a file-based content system. Static portfolio
sections are loaded from JSON files, so the project avoids unnecessary database
tables for content that changes with code. The database is still used where it
adds value: contact messages, admin authentication, and resume uploads.
