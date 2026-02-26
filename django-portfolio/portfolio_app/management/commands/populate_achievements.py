from django.core.management.base import BaseCommand
from portfolio_app.models import Achievement

class Command(BaseCommand):
    help = 'Populate the database with sample achievements'

    def handle(self, *args, **options):

        sample_achievements = [

            {
                'title': 'Fusion 2025 National Level Hackathon',
                'category': 'Hackathon',
                'organization': 'IIC E-Cell SKNCOE and SKN IEEE Student Branch',
                'date': '2025-10-09',
                'location': 'SKNCOE, Pune, India',
                'description': (
                    'Held on 9–10 October 2025. Certificate of participation awarded '
                    'for successfully participating in the Fusion 2025 National Level Hackathon.'
                ),
                'result': 'Participation',
                'certificate_link': 'https://drive.google.com/file/d/1hB5gg-kg4-yoTeQGEW1_0SWccTsR6uBc/view?usp=drive_link',
                'technologies_used': ['Problem Solving', 'Innovation', 'Team Collaboration'],
                'featured': True,
                'display_order': 1
            },

            {
                'title': 'AI-ML Virtual Internship',
                'category': 'Virtual Internship',
                'organization': 'EduSkills in collaboration with AICTE and Google Developers',
                'date': '2025-10-01',
                'location': 'Virtual / Online',
                'description': (
                    'Duration: October–December 2025. Successfully completed a 10-week '
                    'AI-ML Virtual Internship under the EduSkills program.'
                ),
                'result': 'Successfully Completed',
                'certificate_link': 'https://drive.google.com/file/d/1cdtelRl_wF22sKuqf3FbXPUSd0PbkzUh/view?usp=drive_link',
                'technologies_used': ['Artificial Intelligence', 'Machine Learning', 'Python'],
                'featured': True,
                'display_order': 2
            },

            {
                'title': 'Vortexa 2.0 – 12 Hour Hackathon',
                'category': 'Hackathon',
                'organization': 'Department of AI & DS, D. Y. Patil Institute of Technology',
                'date': '2025-09-24',
                'location': 'Pimpri, Pune, India',
                'description': (
                    'Held on 24–25 September 2025. Certificate of participation awarded '
                    'for participating in the 12-hour hackathon Vortexa 2.0.'
                ),
                'result': 'Participation',
                'certificate_link': 'https://drive.google.com/file/d/1gAcUrYZIU4hgw--8f6WmgsYim1KoCBvV/view?usp=drive_link',
                'technologies_used': ['Artificial Intelligence', 'Data Science', 'Team Collaboration'],
                'featured': True,
                'display_order': 3
            },

            {
                'title': '3-Day Workshop on Amazon Web Services (AWS)',
                'category': 'Workshop',
                'organization': 'Department of Computer Engineering, RSCOE',
                'date': '2024-12-26',
                'location': 'Tathawade, Pune, India',
                'description': (
                    'Held from 26–28 December 2024. Successfully completed a 3-day '
                    'workshop on Amazon Web Services (AWS).'
                ),
                'result': 'Successfully Completed',
                'certificate_link': 'https://drive.google.com/file/d/1hoOkaCsTDhVNo9o7YK_iSDjb39KBNNcI/view?usp=drive_link',
                'technologies_used': ['AWS', 'Cloud Computing'],
                'featured': False,
                'display_order': 4
            },

            {
                'title': 'CodeWolf 5.0 Competitive Coding Competition',
                'category': 'Coding Competition',
                'organization': 'Competitive Coding Club, RSCOE',
                'date': '2025-01-10',
                'location': 'RSCOE, Pune, India',
                'description': (
                    'Certificate of participation awarded for participating in the '
                    'CodeWolf 5.0 Competitive Coding Competition.'
                ),
                'result': 'Participation',
                'certificate_link': 'https://drive.google.com/file/d/1Iw3Z0xKgPaW53BcrT3TPr6kGtaXHvRkA/view?usp=drive_link',
                'technologies_used': ['Competitive Programming', 'DSA'],
                'featured': True,
                'display_order': 5
            },
        ]

        for achievement_data in sample_achievements:
            achievement, created = Achievement.objects.get_or_create(
                title=achievement_data['title'],
                organization=achievement_data['organization'],
                defaults=achievement_data
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created achievement: {achievement.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Achievement already exists: {achievement.title}')
                )
