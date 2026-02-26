from django.core.management.base import BaseCommand
from portfolio_app.models import Skill

class Command(BaseCommand):
    help = 'Populate the database with sample skills'

    def handle(self, *args, **options):
        sample_skills = [
            # Programming Languages
            {'name': 'Python',       'category': 'programming', 'proficiency': 98, 'icon': '🐍', 'display_order': 1},
            {'name': 'C++',          'category': 'programming', 'proficiency': 95, 'icon': '⚙️', 'display_order': 2},
            {'name': 'SQL',          'category': 'database', 'proficiency': 85, 'icon': '🗃️', 'display_order': 3},
            {'name': 'Swift',        'category': 'programming', 'proficiency': 60, 'icon': '🧪', 'display_order': 4},
            {'name': 'JavaScript',   'category': 'programming', 'proficiency': 50, 'icon': '📜', 'display_order': 5},
            {'name': 'HTML',         'category': 'programming',      'proficiency': 90, 'icon': '🌐', 'display_order': 6},
            {'name': 'CSS',          'category': 'programming',     'proficiency': 50, 'icon': '🎨', 'display_order': 7},
            
            # Frameworks & Libraries
            {'name': 'Django',       'category': 'framework',   'proficiency': 88, 'icon': '🎸', 'display_order': 8},
            {'name': 'Pandas',       'category': 'framework',   'proficiency': 85, 'icon': '🐼', 'display_order': 9},
            {'name': 'TensorFlow',   'category': 'framework',   'proficiency': 82, 'icon': '🧠', 'display_order': 10},
            {'name': 'React',        'category': 'framework',   'proficiency': 65, 'icon': '⚛️', 'display_order': 11},
            {'name': 'NumPy',        'category': 'framework',     'proficiency': 75, 'icon': '🔢', 'display_order': 12},
            {'name': 'Scikit-learn', 'category': 'framework',     'proficiency': 70, 'icon': '🤖', 'display_order': 13},
            {'name': 'Matplotlib',   'category': 'framework',     'proficiency': 65, 'icon': '📊', 'display_order': 14},
            {'name': 'Seaborn',      'category': 'framework',     'proficiency': 60, 'icon': '📈', 'display_order': 15},
  
            # Tools & Technologies
            {'name': 'Git',          'category': 'tool',            'proficiency': 88, 'icon': '📚', 'display_order': 16},
            {'name': 'MongoDB',      'category': 'database',        'proficiency': 72, 'icon': '🍃', 'display_order': 17},
            {'name': 'AWS',          'category': 'cloud',           'proficiency': 30, 'icon': '☁️', 'display_order': 18},
            {'name': 'PostgreSQL',   'category': 'database',        'proficiency': 80, 'icon': '🐘', 'display_order': 19},
            {'name': 'Oracle',       'category': 'database',        'proficiency': 40, 'icon': '🗄️', 'display_order': 20},
            {'name': 'Oracle-Services', 'category': 'cloud',        'proficiency': 20, 'icon': '🗄️', 'display_order': 21},


        ]
        for skill_data in sample_skills:
            skill, created = Skill.objects.get_or_create(
                name=skill_data['name'],
                defaults=skill_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created skill: {skill.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Skill already exists: {skill.name}')
                )