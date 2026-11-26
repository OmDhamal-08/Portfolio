import logging
from datetime import date
from urllib.parse import quote

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.utils.cache import patch_vary_headers

from . import content_loader as content
from .context_processors import CONTACT_EMAIL
from .forms import ContactForm


logger = logging.getLogger(__name__)


def get_client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def education(request):
    education_list = content.list_education()
    featured_education = [item for item in education_list if item.featured]
    total_education = len(education_list)
    total_degrees = sum(1 for item in education_list if item.degree in ['bachelor', 'master', 'phd'])
    currently_studying = sum(1 for item in education_list if item.currently_studying)
    featured_count = len(featured_education)
    
    context = {
        'education_list': education_list,
        'featured_education': featured_education,
        'degree_choices': content.EDUCATION_DEGREE_CHOICES,
        'total_education': total_education,
        'total_degrees': total_degrees,
        'currently_studying': currently_studying,
        'featured_count': featured_count,
    }
    return render(request, 'education.html', context)

def _mailto_link(subject='', body=''):
    """A mailto: link that opens the visitor's email app with the message filled in."""
    return f'mailto:{CONTACT_EMAIL}?subject={quote(subject)}&body={quote(body)}'


def _send_contact_emails(name, email, subject, message):
    """Email the message to me (reply goes straight to the visitor) and send them a copy."""
    EmailMessage(
        f'Portfolio contact: {subject}',
        f'Name: {name}\nEmail: {email}\nSubject: {subject}\n\n{message}\n\n'
        '---\nSent from the contact form on your portfolio. Reply to this email to answer.',
        settings.DEFAULT_FROM_EMAIL,
        [settings.CONTACT_EMAIL],
        reply_to=[email],
    ).send(fail_silently=False)

    try:
        EmailMessage(
            'Thanks for your message',
            f'Hi {name},\n\nThanks for reaching out through my portfolio. I have your message and will '
            f'reply soon.\n\nYour message:\n{subject}\n\n{message}\n\nBest regards,\nOm Dhamal',
            settings.DEFAULT_FROM_EMAIL,
            [email],
        ).send(fail_silently=False)
    except Exception:
        # The important email already reached me; a failed copy is not worth an error page.
        logger.exception('Could not send the confirmation copy to %s', email)


def contact(request):
    form = ContactForm(request.POST or None)
    send_failed = False

    if request.method == 'POST':
        rate_key = f"contact-form:{get_client_ip(request) or 'unknown'}"
        attempts = cache.get(rate_key, 0)

        if attempts >= 5:
            messages.error(request, 'Too many messages in a short time. Please try again in a few minutes.')
        elif form.is_valid():
            cache.set(rate_key, attempts + 1, 15 * 60)
            data = form.cleaned_data
            try:
                _send_contact_emails(data['name'], data['email'], data['subject'], data['message'])
            except Exception:
                # There is no database, so never pretend the message was saved.
                logger.exception('Contact form email failed for %s', data['email'])
                send_failed = True
            else:
                messages.success(request, 'Message sent! I will get back to you soon.')
                return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')

    mailto = _mailto_link()
    if send_failed:
        data = form.cleaned_data
        mailto = _mailto_link(data['subject'], f"{data['message']}\n\n- {data['name']}")

    return render(request, 'contact.html', {'form': form, 'send_failed': send_failed, 'mailto': mailto})


def certifications(request):
    cert_type = request.GET.get('type', '')
    level = request.GET.get('level', '')
    certifications_list = content.list_certifications(cert_type=cert_type, level=level)
    featured_certifications = [cert for cert in certifications_list if cert.featured]
    
    context = {
        'certifications': certifications_list,
        'featured_certifications': featured_certifications,
        # Only offer filters for types and levels that at least one certificate has
        'cert_types': content.list_used_certification_types(),
        'level_choices': content.list_used_certification_levels(),
        'current_type': cert_type,
        'current_level': level,
    }
    return render(request, 'certifications.html', context)

def achievements(request):
    category = request.GET.get('category', '')
    achievements_list = content.list_achievements(category=category)
    featured_achievements = [achievement for achievement in achievements_list if achievement.featured]
    
    context = {
        'achievements': achievements_list,
        'featured_achievements': featured_achievements,
        'category_choices': content.ACHIEVEMENT_CATEGORY_CHOICES,
        'current_category': category,
    }
    return render(request, 'achievements.html', context)

def projects(request):
    project_type = request.GET.get('type', '')
    status = request.GET.get('status', '')
    query = request.GET.get('q', '').strip()[:100]
    tech = request.GET.get('tech', '')
    projects_list = content.list_projects(project_type=project_type, status=status, query=query, tech=tech)

    context = {
        'projects': projects_list,
        'project_types': content.list_used_project_types(),
        'status_choices': content.PROJECT_STATUS_CHOICES,
        'tech_choices': content.list_project_technologies(limit=12),
        'current_type': project_type,
        'current_status': status,
        'current_query': query,
        'current_tech': tech,
        'total_projects': len(content.list_projects()),
        'has_filters': bool(project_type or status or query or tech),
    }

    # HTMX sends this header; return only the results grid so the page
    # updates without a full reload. Normal requests get the full page.
    if request.headers.get('HX-Request') == 'true':
        response = render(request, 'partials/project_results.html', context)
    else:
        response = render(request, 'projects.html', context)
    # Same URL returns two different bodies, so tell caches to keep them apart.
    patch_vary_headers(response, ['HX-Request'])
    return response


def project_detail(request, slug):
    project = content.get_project(slug)
    related_projects = content.get_related_projects(project)
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'project_detail.html', context)

def home(request):
    projects = content.list_projects()
    certifications = content.list_certifications()
    achievements = content.list_achievements()
    education_items = content.list_education()

    featured_projects = [project for project in projects if project.featured][:2]
    featured_certifications = [cert for cert in certifications if cert.featured][:3]
    featured_achievements = [achievement for achievement in achievements if achievement.featured][:2]
    featured_education = [education for education in education_items if education.featured][:2]
    skills = content.list_skills()

    context = {
        'name': 'Om',
        'title': 'Computer Engineering Student | Django & FastAPI Developer | AI/ML Builder',
        'tagline': 'Building practical web and machine learning projects while learning strong backend fundamentals.',
        'featured_projects': featured_projects,
        'featured_certifications': featured_certifications,
        'featured_achievements': featured_achievements,
        'featured_education': featured_education,
        'now': content.load_now(),
        'journey': _journey_timeline(featured_education, featured_certifications, featured_achievements),
        'top_skills': [skill.name for skill in skills][:12],
        'quick_stats': [
            {'number': sum(1 for project in projects if project.status == 'completed'), 'label': 'Projects Completed'},
            {'number': len(certifications), 'label': 'Certifications'},
            {'number': len(achievements), 'label': 'Achievements'},
            {'number': len(education_items), 'label': 'Education'},
        ]
    }
    return render(request, 'index.html', context)

def _journey_timeline(education_items, certifications, achievements):
    """Merge featured milestones into one list, newest first, for the home timeline."""
    entries = []
    for item in education_items:
        entries.append({'date': item.start_date, 'date_label': item.get_duration(), 'kind': 'Education',
                        'title': item.title, 'subtitle': item.institution, 'url': 'education'})
    for item in certifications:
        entries.append({'date': item.issue_date, 'date_label': item.issue_date.strftime('%b %Y') if item.issue_date else '',
                        'kind': 'Certification', 'title': item.title, 'subtitle': item.issuing_organization,
                        'url': 'certifications'})
    for item in achievements:
        entries.append({'date': item.date, 'date_label': item.date.strftime('%b %Y') if item.date else '',
                        'kind': item.get_category_display(), 'title': item.title, 'subtitle': item.organization,
                        'url': 'achievements'})
    return sorted(entries, key=lambda entry: entry['date'] or date.min, reverse=True)


def now(request):
    return render(request, 'now.html', {'now': content.load_now()})


def about(request):
    skills_by_category = content.group_skills_by_category()
    skills_preview = {}
    categories_to_show = ['programming', 'framework', 'tool']
    
    for category in categories_to_show:
        skills_preview[category] = skills_by_category.get(category, [])[:3]
    
    context = {
        'personal_info': {
            'name': 'Om Dhamal',
            'title': 'Computer Engineering Student | Django & FastAPI Developer | AI/ML Builder',
            'location': 'Pune, India',
            'email': 'dhamalomm@gmail.com',
            'bio': 'I build backends, AI agents and machine learning projects, and I like making them work reliably, not just in a demo.',
            'detailed_bio': [
                'I study Computer Engineering at JSPM\'s RSCOE in Pune, but most of what I know comes from building things and breaking them outside the classroom.',
                'My work sits where backend development meets AI. I write APIs with Django and FastAPI, design the databases behind them, and lately spend most of my time on LLM apps: RAG pipelines, agents that call tools, and the checks that keep their answers honest.',
                'Machine learning is where it started. My EduSkills internship and projects like ZonePredict AI taught me that clean data and a fair baseline matter more than an impressive-looking score.',
                'I keep my problem solving sharp with C++ on LeetCode and Codeforces. Next, I want to join a team as an intern or engineer and ship real products, and one day build a startup of my own.',
            ]
        },
        'education': [
            {
                'degree': 'B.Tech in Computer Engineering',
                'institution': "JSPM's Rajarshi Shahu College of Engineering, Pune",
                'year': '2023-Present',
                'description': 'Regular B.Tech curriculum with subjects such as DSA, DBMS, Operating Systems and Computer Networks. CGPA: 9.15/10 (till 6th semester).',
                'icon': '🎓'
            },
            {
                'degree': 'HSC and SSC',
                'institution': "Chaitannya's International School, Baramati",
                'year': '2023',
                'description': 'HSC: 76.17% | SSC: 92.20%',
                'icon': '🏫'
            },
        ],
        'experience': [
            {
                'position': 'AI & Machine Learning Virtual Intern',
                'company': 'EduSkills',
                'year': 'Oct 2025 - Dec 2025',
                'description': 'Ten weeks of hands-on machine learning: from cleaning data to training and evaluating models. I finished more than five complete ML projects with Scikit-learn and TensorFlow.'
            },
        ],
        'skills_preview': skills_preview,
        'skills_categories': [
            {
                'name': 'Programming Languages',
                'skills': [skill.name for skill in skills_preview.get('programming', [])],
                'icon': '💻'
            },
            {
                'name': 'Frameworks & Libraries',
                'skills': [skill.name for skill in skills_preview.get('framework', [])],
                'icon': '🛠️'
            },
            {
                'name': 'Tools & Technologies',
                'skills': [skill.name for skill in skills_preview.get('tool', [])],
                'icon': '⚙️'
            }
        ]
    }
    return render(request, 'about.html', context)

def skills(request):
    context = {
        'skills_by_category': content.group_skills_by_category(),
        'categories': dict(content.SKILL_CATEGORY_CHOICES),
    }
    return render(request, 'skills.html', context)

def download_resume(request):
    """Old /download-resume/ links: send them to the PDF, which WhiteNoise serves directly."""
    return redirect(static('resume.pdf'), permanent=True)
