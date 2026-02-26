from django.core.management.base import BaseCommand
from portfolio_app.models import Education
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Populate the database with sample education data'

    def handle(self, *args, **options):
        sample_education = [
            {
                'degree': 'school',
                'title': 'Primary & Middle School',
                'institution': 'Maharashtra Education Society, Baramati',
                'location': 'Baramati, Maharashtra, India',
                'start_date': datetime(2008, 6, 1),   # LKG approx
                'end_date': datetime(2017, 5, 1),     # 7th standard
                'grade': None,
                'description': 'Completed foundational schooling from LKG to 7th standard with active participation in academics and co-curricular activities.',
                'courses': 'Mathematics, Science, English, Social Studies, Computer Basics',
                'achievements': '',
                'featured': False,
                'display_order': 1,
            },
            {
                'degree': 'school',
                'title': '8th Standard',
                'institution': 'Radha Shyam N. Aggrawal School & Junior College',
                'location': 'Baramati, Maharashtra, India',
                'start_date': datetime(2017, 6, 1),
                'end_date': datetime(2018, 5, 1),
                'grade': None,
                'description': 'Completed 8th standard before moving to a JEE-focused academy.',
                'courses': 'Mathematics, Science, English, Social Studies, Computer Science',
                'achievements': '',
                'featured': False,
                'display_order': 2,
            },
            {
                'degree': 'school',
                'title': 'High School (9th to 12th) – JEE Preparation Track',
                'institution': 'Chaitanya International School & Academy',
                'location': 'Baramati, Maharashtra, India',
                'start_date': datetime(2018, 6, 1),
                'end_date': datetime(2023, 5, 1),
                'grade': '10th: 92%, 12th: 76%',
                'description': 'Completed 9th to 12th with integrated JEE and CET preparation. Strong foundation in PCM with additional focus on competitive exams.',
                'courses': 'Physics, Chemistry, Mathematics, English, JEE Mains Coaching, MHT-CET Preparation',
                'achievements': 'MHT-CET: 96 Percentile, JEE Mains: 78 Percentile',
                'featured': True,
                'display_order': 3,
            },
            {
                'degree': 'bachelor',
                'title': 'Bachelor of Technology in Computer Science',
                'institution': 'Rajashree Shahu College of Engineering (JSPM Tathawade)',
                'location': 'Pune, Maharashtra, India',
                'start_date': datetime(2023, 8, 1),
                'currently_studying': True,
                'description': 'Pursuing B.Tech in Computer Science. Learning core computing subjects, machine learning, and software development. Strong involvement in AI/ML projects and self-learning.',
                'courses': 'Data Structures, Algorithms, DBMS, Machine Learning, AI, Operating Systems, Python, C++, Web Development',
                'achievements': 'CGPA: 9.43 (ongoing)',
                'featured': True,
                'display_order': 4,
            },
            {
                'degree': 'online',
                'title': 'Machine Learning Specialization',
                'institution': 'Coursera — Andrew Ng',
                'location': 'Online',
                'start_date': datetime(2024, 1, 1),
                'currently_studying': True,
                'description': 'Comprehensive course covering supervised learning, unsupervised learning, neural networks and ML deployment.',
                'courses': 'Supervised Learning, Unsupervised Learning, Neural Networks, TensorFlow, Model Evaluation',
                'achievements': 'Completed with excellent performance',
                'featured': False,
                'display_order': 5,
            },
        ]


        for edu_data in sample_education:
            edu, created = Education.objects.get_or_create(
                title=edu_data['title'],
                institution=edu_data['institution'],
                defaults=edu_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created education: {edu.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Education already exists: {edu.title}')
                )