import json
from datetime import date, timedelta
from pathlib import Path

from django.conf import settings
from django.http import Http404
from django.utils import timezone
from django.utils.text import slugify


PROJECT_TYPE_CHOICES = [
    ('web', 'Web Application'),
    ('ml', 'Machine Learning'),
    ('mobile', 'Mobile App'),
    ('automation', 'Automation'),
    ('ai', 'AI Workflow'),
    ('data', 'Data Analysis'),
    ('other', 'Other'),
]

PROJECT_STATUS_CHOICES = [
    ('completed', 'Completed'),
    ('in_progress', 'In Progress'),
    ('planned', 'Planned'),
]

CERTIFICATION_TYPE_CHOICES = [
    ('foundational', 'Foundational Certification'),
    ('associate', 'Associate Certification'),
    ('technical', 'Technical Certification'),
    ('professional', 'Professional Certification'),
    ('university', 'University Course'),
    ('online', 'Online Course'),
    ('course_completion', 'Course Completion'),
]

CERTIFICATION_LEVEL_CHOICES = [
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
    ('expert', 'Expert'),
]

ACHIEVEMENT_CATEGORY_CHOICES = [
    ('hackathon', 'Hackathon'),
    ('competition', 'Competition'),
    ('award', 'Award'),
    ('publication', 'Publication'),
    ('volunteer', 'Volunteer Work'),
    ('leadership', 'Leadership'),
    ('other', 'Other'),
]

SKILL_CATEGORY_CHOICES = [
    ('programming', 'Programming Languages'),
    ('framework', 'Frameworks & Libraries'),
    ('tool', 'Tools & Technologies'),
    ('ml', 'AI/ML Tools'),
    ('database', 'Databases'),
    ('cloud', 'Cloud & DevOps'),
]

EDUCATION_DEGREE_CHOICES = [
    ('school', 'School'),
    ('high_school', 'High School'),
    ('diploma', 'Diploma'),
    ('bachelor', "Bachelor's Degree"),
    ('master', "Master's Degree"),
    ('phd', 'PhD'),
    ('certificate', 'Certificate'),
    ('online', 'Online Course'),
]


class ContentValidationError(ValueError):
    pass


class StaticAsset:
    def __init__(self, path):
        self.path = path
        self.url = _asset_url(path)

    def __str__(self):
        return self.url


class ContentItem:
    def __init__(self, **data):
        self.__dict__.update(data)


class ProjectContent(ContentItem):
    def get_project_type_display(self):
        return _choice_label(PROJECT_TYPE_CHOICES, self.project_type)

    def get_status_display(self):
        return _choice_label(PROJECT_STATUS_CHOICES, self.status)

    def get_tech_list(self):
        return list(getattr(self, 'technologies', []))

    def get_additional_images_list(self):
        return [_asset_url(path) for path in getattr(self, 'additional_images', []) if path]

    def get_project_duration(self):
        if self.start_date and self.end_date:
            return f"{self.start_date.strftime('%b %Y')} - {self.end_date.strftime('%b %Y')}"
        if self.start_date:
            return f"Started {self.start_date.strftime('%b %Y')}"
        return 'Duration not specified'


class CertificationContent(ContentItem):
    def get_certification_type_display(self):
        return _choice_label(CERTIFICATION_TYPE_CHOICES, self.certification_type)

    def get_skill_level_display(self):
        return _choice_label(CERTIFICATION_LEVEL_CHOICES, self.skill_level)

    def get_skills_list(self):
        return list(getattr(self, 'skills', []))

    def is_expired(self):
        return bool(self.expiration_date and self.expiration_date < timezone.now().date())

    def is_expiring_soon(self):
        if not self.expiration_date:
            return False
        return self.expiration_date <= timezone.now().date() + timedelta(days=90)


class AchievementContent(ContentItem):
    def get_category_display(self):
        return _choice_label(ACHIEVEMENT_CATEGORY_CHOICES, self.category)

    def get_technologies_list(self):
        return list(getattr(self, 'technologies', []))

    def get_icon(self):
        icons = {
            'hackathon': '\U0001f4bb',
            'competition': '\U0001f3c6',
            'award': '\U0001f396\ufe0f',
            'publication': '\U0001f4c4',
            'volunteer': '\U0001f91d',
            'leadership': '\U0001f465',
            'other': '\u2728',
        }
        return icons.get(self.category, '\u2728')


class EducationContent(ContentItem):
    def get_degree_display(self):
        return _choice_label(EDUCATION_DEGREE_CHOICES, self.degree)

    def get_duration(self):
        if self.currently_studying:
            return f"{self.start_date.strftime('%b %Y')} - Present"
        if self.end_date:
            return f"{self.start_date.strftime('%b %Y')} - {self.end_date.strftime('%b %Y')}"
        return self.start_date.strftime('%b %Y')

    def get_courses_list(self):
        return _list_value(getattr(self, 'courses', []))

    def get_achievements_list(self):
        return _list_value(getattr(self, 'achievements', []))

    def get_icon(self):
        icons = {
            'school': '\U0001f3eb',
            'high_school': '\U0001f3eb',
            'diploma': '\U0001f4dc',
            'bachelor': '\U0001f393',
            'master': '\U0001f4da',
            'phd': '\U0001f9d1\u200d\U0001f393',
            'certificate': '\U0001f4c4',
            'online': '\U0001f4bb',
        }
        return icons.get(self.degree, '\U0001f393')


class SkillContent(ContentItem):
    def proficiency_percentage(self):
        return f'{self.proficiency}%'


def list_projects(project_type='', status=''):
    projects = _active(load_projects())
    if project_type:
        projects = [project for project in projects if project.project_type == project_type]
    if status:
        projects = [project for project in projects if project.status == status]
    return projects


def get_project(slug):
    for project in _active(load_projects()):
        if project.slug == slug:
            return project
    raise Http404('Project not found')


def get_related_projects(project, limit=3):
    related = [
        item
        for item in _active(load_projects())
        if item.project_type == project.project_type and item.slug != project.slug
    ]
    return related[:limit]


def list_certifications(cert_type='', level=''):
    certifications = _active(load_certifications())
    if cert_type:
        certifications = [cert for cert in certifications if cert.certification_type == cert_type]
    if level:
        certifications = [cert for cert in certifications if cert.skill_level == level]
    return certifications


def list_achievements(category=''):
    achievements = _active(load_achievements())
    if category:
        achievements = [achievement for achievement in achievements if achievement.category == category]
    return achievements


def list_education():
    return _active(load_education())


def list_skills():
    return _active(load_skills())


def group_skills_by_category():
    grouped = {}
    for skill in list_skills():
        grouped.setdefault(skill.category, []).append(skill)
    return grouped


def load_projects():
    projects = []
    seen_slugs = set()
    for order, raw in enumerate(_read_json('projects.json'), start=1):
        slug = raw.get('slug') or slugify(raw.get('title', 'project'))
        if slug in seen_slugs:
            raise ContentValidationError(f'Duplicate project slug: {slug}')
        seen_slugs.add(slug)

        technologies = _list_value(raw.get('technologies') or raw.get('tech_stack'))
        project = ProjectContent(
            title=_required(raw, 'title', 'projects.json'),
            slug=slug,
            short_description=raw.get('short_description') or raw.get('description', '')[:300],
            description=raw.get('description', ''),
            project_type=raw.get('project_type', 'other'),
            status=raw.get('status', 'completed'),
            technologies=technologies,
            tech_stack=', '.join(technologies),
            github_link=raw.get('github_link') or '',
            live_demo=raw.get('live_demo') or '',
            documentation_link=raw.get('documentation_link') or '',
            featured_image=_asset(raw.get('featured_image')),
            additional_images=_list_value(raw.get('additional_images', [])),
            start_date=_date(raw.get('start_date')),
            end_date=_date(raw.get('end_date')),
            display_order=raw.get('display_order', order),
            featured=raw.get('featured', False),
            is_active=raw.get('is_active', True),
        )
        projects.append(project)
    return sorted(projects, key=lambda item: (item.display_order, item.title))


def load_certifications():
    certifications = []
    for order, raw in enumerate(_read_json('certifications.json'), start=1):
        certifications.append(CertificationContent(
            title=_required(raw, 'title', 'certifications.json'),
            issuing_organization=raw.get('issuing_organization', ''),
            issue_date=_date(raw.get('issue_date')),
            expiration_date=_date(raw.get('expiration_date')),
            credential_id=raw.get('credential_id') or '',
            credential_url=raw.get('credential_url') or '',
            certificate_image=_asset(raw.get('certificate_image')),
            certification_type=raw.get('certification_type', 'technical'),
            skill_level=raw.get('skill_level', 'intermediate'),
            description=raw.get('description', ''),
            skills=_list_value(raw.get('skills', [])),
            display_order=raw.get('display_order', order),
            featured=raw.get('featured', False),
            is_active=raw.get('is_active', True),
        ))
    return sorted(certifications, key=lambda item: (item.display_order, -_ordinal(item.issue_date)))


def load_achievements():
    achievements = []
    for order, raw in enumerate(_read_json('achievements.json'), start=1):
        achievements.append(AchievementContent(
            title=_required(raw, 'title', 'achievements.json'),
            category=raw.get('category', 'other'),
            organization=raw.get('organization', ''),
            date=_date(raw.get('date')),
            location=raw.get('location') or '',
            description=raw.get('description', ''),
            result=raw.get('result') or '',
            project_link=raw.get('project_link') or '',
            certificate_link=raw.get('certificate_link') or '',
            image=_asset(raw.get('image')),
            technologies=_list_value(raw.get('technologies', [])),
            display_order=raw.get('display_order', order),
            featured=raw.get('featured', False),
            is_active=raw.get('is_active', True),
        ))
    return sorted(achievements, key=lambda item: (item.display_order, -_ordinal(item.date)))


def load_education():
    education = []
    for order, raw in enumerate(_read_json('education.json'), start=1):
        education.append(EducationContent(
            degree=raw.get('degree', 'bachelor'),
            title=_required(raw, 'title', 'education.json'),
            institution=raw.get('institution', ''),
            location=raw.get('location', ''),
            start_date=_date(raw.get('start_date')),
            end_date=_date(raw.get('end_date')),
            currently_studying=raw.get('currently_studying', False),
            description=raw.get('description', ''),
            grade=raw.get('grade') or '',
            courses=_list_value(raw.get('courses', [])),
            achievements=_list_value(raw.get('achievements', [])),
            logo=_asset(raw.get('logo')),
            certificate=_asset(raw.get('certificate')),
            display_order=raw.get('display_order', order),
            featured=raw.get('featured', False),
            is_active=raw.get('is_active', True),
        ))
    return sorted(education, key=lambda item: (item.display_order, -_ordinal(item.start_date)))


def load_skills():
    skills = []
    for order, raw in enumerate(_read_json('skills.json'), start=1):
        skills.append(SkillContent(
            name=_required(raw, 'name', 'skills.json'),
            category=raw.get('category', 'tool'),
            proficiency=int(raw.get('proficiency', 50)),
            description=raw.get('description') or '',
            icon=raw.get('icon') or '',
            display_order=raw.get('display_order', order),
            is_active=raw.get('is_active', True),
        ))
    return sorted(skills, key=lambda item: (item.display_order, item.name))


def validate_content():
    loaders = [
        ('projects', load_projects),
        ('certifications', load_certifications),
        ('achievements', load_achievements),
        ('education', load_education),
        ('skills', load_skills),
    ]
    errors = []
    for label, loader in loaders:
        try:
            loader()
        except Exception as exc:
            errors.append(f'{label}: {exc}')
    return errors


def _read_json(filename):
    path = _content_root() / filename
    if not path.exists():
        raise ContentValidationError(f'Missing content file: {path}')
    return json.loads(path.read_text(encoding='utf-8-sig'))


def _content_root():
    return Path(settings.BASE_DIR) / 'content'


def _required(raw, key, filename):
    value = raw.get(key)
    if value in (None, ''):
        raise ContentValidationError(f'{filename} item is missing required field "{key}"')
    return value


def _active(items):
    return [item for item in items if getattr(item, 'is_active', True)]


def _choice_label(choices, value):
    return dict(choices).get(value, value)


def _date(value):
    if not value:
        return None
    if isinstance(value, date):
        return value
    return date.fromisoformat(value)


def _ordinal(value):
    return value.toordinal() if value else 0


def _list_value(value):
    if not value:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value).split(',') if item.strip()]


def _asset(path):
    if not path:
        return None
    return StaticAsset(path)


def _asset_url(path):
    if not path:
        return ''
    if str(path).startswith(('http://', 'https://', '/')):
        return str(path)
    return f"{settings.STATIC_URL}{str(path).lstrip('/')}"
