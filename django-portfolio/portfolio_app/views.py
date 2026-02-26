from django.shortcuts import get_object_or_404, redirect, render
from django.http import FileResponse
import os
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from .forms import ContactForm
from .models import Skill, Project, Certification, Achievement, Education

def education(request):
    # Get all active education records, ordered by display order and start date
    education_list = Education.objects.filter(is_active=True).order_by('display_order', '-start_date')
    
    # Separate by featured and non-featured
    featured_education = education_list.filter(featured=True)
    
    # Calculate statistics for the template
    total_education = education_list.count()
    total_degrees = education_list.filter(degree__in=['bachelor', 'master', 'phd']).count()
    currently_studying = education_list.filter(currently_studying=True).count()
    featured_count = featured_education.count()
    
    context = {
        'education_list': education_list,
        'featured_education': featured_education,
        'degree_choices': Education.DEGREE_CHOICES,
        'total_education': total_education,
        'total_degrees': total_degrees,
        'currently_studying': currently_studying,
        'featured_count': featured_count,
    }
    return render(request, 'education.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Prepare email content
            email_subject = f"Portfolio Contact: {subject}"
            email_message = f"""
Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
This message was sent from your portfolio contact form.
            """
            
            try:
                # Send email
                send_mail(
                    email_subject,
                    email_message,
                    email,  # From email
                    [settings.DEFAULT_FROM_EMAIL],  # To email (your email)
                    fail_silently=False,
                )
                
                # Send confirmation email to user
                confirmation_subject = "Thank you for contacting me!"
                confirmation_message = f"""
Hi {name},

Thank you for reaching out through my portfolio website. I have received your message and will get back to you as soon as possible.

Here's a copy of your message:
Subject: {subject}
Message: {message}

Best regards,
Your Name
                """
                
                send_mail(
                    confirmation_subject,
                    confirmation_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                
                messages.success(request, 'Your message has been sent successfully! I will get back to you soon.')
                return redirect('contact')
                
            except BadHeaderError:
                messages.error(request, 'Invalid header found. Please try again.')
            except Exception as e:
                messages.error(request, f'There was an error sending your message. Please try again later. Error: {str(e)}')
        
        else:
            messages.error(request, 'Please correct the errors below.')
    
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'contact.html', context)

def certifications(request):
    # Get filter parameters
    cert_type = request.GET.get('type', '')
    level = request.GET.get('level', '')
    
    # Get all active certifications
    certifications_list = Certification.objects.filter(is_active=True)
    
    # Apply filters
    if cert_type:
        certifications_list = certifications_list.filter(certification_type=cert_type)
    if level:
        certifications_list = certifications_list.filter(skill_level=level)
    
    # Get featured certifications
    featured_certifications = certifications_list.filter(featured=True)
    
    context = {
        'certifications': certifications_list,
        'featured_certifications': featured_certifications,
        'cert_types': Certification.TYPE_CHOICES,
        'level_choices': Certification.LEVEL_CHOICES,
        'current_type': cert_type,
        'current_level': level,
    }
    return render(request, 'certifications.html', context)

def achievements(request):
    # Get filter parameters
    category = request.GET.get('category', '')
    
    # Get all active achievements
    achievements_list = Achievement.objects.filter(is_active=True)
    
    # Apply filters
    if category:
        achievements_list = achievements_list.filter(category=category)
    
    # Get featured achievements
    featured_achievements = achievements_list.filter(featured=True)
    
    context = {
        'achievements': achievements_list,
        'featured_achievements': featured_achievements,
        'category_choices': Achievement.CATEGORY_CHOICES,
        'current_category': category,
    }
    return render(request, 'achievements.html', context)

def projects(request):
    # Get filter parameters
    project_type = request.GET.get('type', '')
    status = request.GET.get('status', '')
    
    # Get all active projects
    projects_list = Project.objects.filter(is_active=True)
    
    # Apply filters
    if project_type:
        projects_list = projects_list.filter(project_type=project_type)
    if status:
        projects_list = projects_list.filter(status=status)
    
    # Get featured projects
    featured_projects = projects_list.filter(featured=True)[:3]
    
    context = {
        'projects': projects_list,
        'featured_projects': featured_projects,
        'project_types': Project.PROJECT_TYPE_CHOICES,
        'status_choices': Project.STATUS_CHOICES,
        'current_type': project_type,
        'current_status': status,
    }
    
    return render(request, 'projects.html', context)
def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_active=True)
    
    # Get related projects (same type, excluding current)
    related_projects = Project.objects.filter(
        project_type=project.project_type,
        is_active=True
    ).exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'project_detail.html', context)

def home(request):
    # Get featured projects from database
    featured_projects = Project.objects.filter(
        featured=True, 
        is_active=True
    ).order_by('display_order')[:2]
    
    # Get featured certifications and achievements
    featured_certifications = Certification.objects.filter(
        featured=True, 
        is_active=True
    ).order_by('display_order')[:3]
    
    featured_achievements = Achievement.objects.filter(
        featured=True, 
        is_active=True
    ).order_by('display_order')[:2]
    
    # Get featured education
    featured_education = Education.objects.filter(
        featured=True, 
        is_active=True
    ).order_by('display_order')[:2]

    # Calculate statistics
    project_count = Project.objects.filter(is_active=True).count()
    certification_count = Certification.objects.filter(is_active=True).count()
    achievement_count = Achievement.objects.filter(is_active=True).count()
    education_count = Education.objects.filter(is_active=True).count()

    context = {
        'name': 'Om',
        'title': 'Engineer • Developer • Innovator',
        'tagline': 'Creating intelligent systems, scalable solutions, and impactful digital experiences through innovation and technology.',
        'featured_projects': featured_projects,
        'featured_certifications': featured_certifications,
        'featured_achievements': featured_achievements,
        'featured_education': featured_education,
        'quick_stats': [
            {'number': project_count, 'label': 'Projects Completed'},
            {'number': certification_count, 'label': 'Certifications'},
            {'number': achievement_count, 'label': 'Achievements'},
            {'number': education_count, 'label': 'Education'},
        ]
    }
    return render(request, 'index.html', context)

def about(request):
    # Get skills for the about page (limited to 3 per category for preview)
    skills_preview = {}
    categories_to_show = ['programming', 'framework', 'tool']
    
    for category in categories_to_show:
        skills_preview[category] = Skill.objects.filter(
            category=category, 
            is_active=True
        ).order_by('display_order')[:3]
    
    context = {
        'personal_info': {
            'name': 'Om Dhamal',
            'title': 'Engineer • Developer • Innovator',
            'location': 'Pune, India',
            'email': 'dhamalom@gmail.com',
            'bio': 'I am a passionate developer with expertise in building scalable web applications and intelligent machine learning solutions. I love turning complex problems into simple, beautiful designs.',
            'detailed_bio': [

               'I am an enthusiastic and motivated Computer Science student currently pursuing my B.Tech in CSE. I\'m actively learning Machine Learning, Data Structures & Algorithms, and full-stack development, with a strong interest in building intelligent and efficient software solutions.',

                'I enjoy understanding how things work, breaking down complex ideas, and turning them into simple, practical implementations. My learning journey includes hands-on projects in Python, Django, and foundational machine learning, which help me continuously grow as a developer.',

                'Although I\'m early in my professional journey, I am passionate, consistent, and eager to take on real-world challenges. I love exploring new technologies, improving my problem-solving skills, and building projects that enhance my understanding.',

                'When I\'m not studying or coding, I enjoy experimenting with new tech tools, working on personal projects, and learning by building.'
            ]
        },
        'education': [
            {
                'degree': 'Bachelor of Technology in Computer Science',
                'institution': 'Rajashree Shahu College of Engineering (JSPM Tathawade)',
                'year': '2023–Present',
                'description': 'Pursuing B.Tech in Computer Science. Learning core CS subjects, machine learning, and software development. Actively involved in AI/ML projects and continuous self-learning. CGPA: 9.43 (ongoing).',
                'icon': '🎓'
            },
            {
                'degree': 'Machine Learning Specialization',
                'institution': 'Coursera — Andrew Ng',
                'year': '2024–Present',
                'description': 'Comprehensive specialization covering supervised learning, unsupervised learning, neural networks, TensorFlow, and model evaluation. Currently studying.',
                'icon': '🤖'
            }

        ],
        'experience': [
            {
            'position': 'Coming soon',
            'company': 'Currently pursuing B.Tech',
            'year': 'No experience right now',
            'description': 'I have attended workshops and other events, but I still do not have experience with any live projects'

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
    # Get all active skills grouped by category
    skills = Skill.objects.filter(is_active=True)
    
    # Organize skills by category for template
    skills_by_category = {}
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    context = {
        'skills_by_category': skills_by_category,
        'categories': dict(Skill.CATEGORY_CHOICES),
    }
    return render(request, 'skills.html', context)

# REMOVED DUPLICATE projects() FUNCTION FROM HERE

def blog(request):
    return render(request, 'blog.html')

# REMOVED DUPLICATE contact() FUNCTION FROM HERE

def download_resume(request):
    # Path to the resume PDF
    resume_path = os.path.join(settings.BASE_DIR, 'static', 'resume.pdf')
    
    # Check if file exists
    if os.path.exists(resume_path):
        return FileResponse(open(resume_path, 'rb'), as_attachment=True, filename='Om_Dhamal_Resume.pdf')
    else:
        # Fallback: Create a simple text resume
        resume_content = """OM DHAMAL - Resume
        (Your PDF resume will be available soon)"""
        
        response = HttpResponse(resume_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="Om_Dhamal_Resume.txt"'
        return response
