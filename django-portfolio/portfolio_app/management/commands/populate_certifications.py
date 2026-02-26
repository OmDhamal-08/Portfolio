from django.core.management.base import BaseCommand
from portfolio_app.models import Certification
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Populate the database with sample certifications'

    def handle(self, *args, **options):
        sample_certifications = [
            {
                'title': 'OCI AI Foundations',
                'issuing_organization': 'Oracle University',
                'issue_date': datetime.now() - timedelta(days=180),
                'expiration_date': datetime.now() + timedelta(days=545),
                'credential_id': 'OCF-AI-002394',
                'credential_url': 'https://catalog-education.oracle.com/pls/certview/sharebadge?id=3243B976B5E41BD7894CB8FF3A22F7E5A751A0E3A8C82D8CFE16E249B78B2328',
                'certification_type': 'technical',  # Changed from 'Foundational' to 'technical'
                'skill_level': 'beginner',  # Changed from 'Beginner' to 'beginner'
                'description': 'Demonstrates foundational knowledge of Artificial Intelligence concepts, Machine Learning basics, and Oracle Cloud Infrastructure AI services.',
                'skills_covered': 'AI Basics, ML Concepts, OCI AI Services, Model Deployment, Data Handling',
                'featured': True,
                'display_order': 1,
            },
            {
                'title': 'OCI Generative AI',
                'issuing_organization': 'Oracle University',
                'issue_date': datetime.now() - timedelta(days=180),
                'expiration_date': datetime.now() + timedelta(days=545),
                'credential_id': 'OC-GENAI-004582',
                'credential_url': 'https://catalog-education.oracle.com/pls/certview/sharebadge?id=60EF2EF7A0410BBB352F6C81FA7D36E878223A1008B93A71BB9A790466022E39',
                'certification_type': 'technical',  # Changed from 'Associate' to 'technical'
                'skill_level': 'intermediate',  # Changed from 'Intermediate' to 'intermediate'
                'description': 'Demonstrates knowledge of Generative AI concepts, LLMs, prompt engineering, and the use of Oracle Cloud Infrastructure Generative AI services.',
                'skills_covered': 'LLMs, Generative AI, Prompt Engineering, Embeddings, OCI GenAI Services, AI Workflows',
                'featured': True,
                'display_order': 2,
            },
            {
                'title': 'Machine Learning Specialization',
                'issuing_organization': 'Coursera',
                'issue_date': datetime.now() - timedelta(days=300),
                'credential_url': 'https://www.coursera.org/account/accomplishments/verify/I8GPE78WHZ6D',
                'certification_type': 'online',  # Keep as 'online' (matches model)
                'skill_level': 'intermediate',  # Keep as 'intermediate' (matches model)
                'description': 'Comprehensive machine learning course covering supervised and unsupervised learning, deep learning, and practical applications.',
                'skills_covered': 'Python, TensorFlow, Scikit-learn, Neural Networks, Data Preprocessing',
                'featured': True,
                'display_order': 3,
            },
            {
                'title': 'Introduction to Back-End Development',
                'issuing_organization': 'Meta (via Coursera)',
                'issue_date': datetime.now() - timedelta(days=120),
                'expiration_date': None,
                'credential_id': 'META-BACKEND-INT-02349',
                'credential_url': 'https://www.coursera.org/account/accomplishments/verify/EN8XNVHXRUOB',
                'certification_type': 'online',  # Changed from 'Course Completion' to 'online'
                'skill_level': 'beginner',  # Changed from 'Beginner' to 'beginner'
                'description': 'Covers the fundamentals of back-end development, including server-side programming, databases, APIs, and the core principles of building scalable backend systems.',
                'skills_covered': 'HTTP, APIs, Databases, Server-Side Logic, Web Frameworks, Version Control',
                'featured': False,
                'display_order': 4,
            },
            {
                'title': 'Introduction to Databases for Back-End Development',
                'issuing_organization': 'Meta (via Coursera)',
                'issue_date': datetime.now() - timedelta(days=90),
                'expiration_date': None,
                'credential_id': 'META-DB-INTRO-04721',
                'credential_url': 'https://www.coursera.org/account/accomplishments/verify/0P2NDWQ41JZR',
                'certification_type': 'online',  # Changed from 'Course Completion' to 'online'
                'skill_level': 'beginner',  # Changed from 'Beginner' to 'beginner'
                'description': 'Covers the fundamentals of relational databases, SQL queries, data modeling, CRUD operations, and database integration for back-end systems.',
                'skills_covered': 'SQL, Relational Databases, ER Diagrams, CRUD Operations, Data Modeling, Backend Integration',
                'featured': False,
                'display_order': 5,
            },
            {
                'title': 'Crash Course on Python',
                'issuing_organization': 'Google (via Coursera)',
                'issue_date': datetime.now() - timedelta(days=150),
                'expiration_date': None,
                'credential_id': 'GOOGLE-PY-CC-09231',
                'credential_url': 'https://www.coursera.org/account/accomplishments/verify/T19UQQZDECUT',
                'certification_type': 'online',  # Changed from 'Course Completion' to 'online'
                'skill_level': 'beginner',  # Changed from 'Beginner' to 'beginner'
                'description': 'Provides a hands-on introduction to Python programming, covering variables, functions, loops, conditionals, data structures, error handling, and basic automation.',
                'skills_covered': 'Python, Functions, Loops, Conditionals, Data Structures, Automation, Problem Solving',
                'featured': False,
                'display_order': 6,
            }
        ]

        for cert_data in sample_certifications:
            cert, created = Certification.objects.get_or_create(
                title=cert_data['title'],
                issuing_organization=cert_data['issuing_organization'],
                defaults=cert_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created certification: {cert.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Certification already exists: {cert.title}')
                )