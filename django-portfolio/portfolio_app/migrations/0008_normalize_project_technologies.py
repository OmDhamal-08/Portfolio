from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models
import django.db.models.deletion


def split_csv(value):
    return [item.strip() for item in str(value or '').split(',') if item.strip()]


def backfill_relations(apps, schema_editor):
    Technology = apps.get_model('portfolio_app', 'Technology')
    Project = apps.get_model('portfolio_app', 'Project')
    Achievement = apps.get_model('portfolio_app', 'Achievement')
    Certification = apps.get_model('portfolio_app', 'Certification')
    Skill = apps.get_model('portfolio_app', 'Skill')

    for project in Project.objects.all():
        technologies = [
            Technology.objects.get_or_create(name=name, defaults={'category': 'other'})[0]
            for name in split_csv(project.tech_stack)
        ]
        if technologies:
            project.technologies.set(technologies)

    for achievement in Achievement.objects.all():
        technologies = [
            Technology.objects.get_or_create(name=name, defaults={'category': 'other'})[0]
            for name in split_csv(achievement.technologies_used)
        ]
        if technologies:
            achievement.technologies.set(technologies)

    for certification in Certification.objects.all():
        skills = Skill.objects.filter(name__in=split_csv(certification.skills_covered))
        if skills:
            certification.skills.set(skills)


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_app', '0007_alter_project_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('category', models.CharField(choices=[('language', 'Programming Language'), ('framework', 'Framework / Library'), ('database', 'Database'), ('cloud', 'Cloud / Deployment'), ('tool', 'Tool'), ('other', 'Other')], default='other', max_length=20)),
                ('display_order', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Technologies',
                'ordering': ['display_order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='projects/screenshots/')),
                ('caption', models.CharField(blank=True, max_length=150)),
                ('display_order', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='portfolio_app.project')),
            ],
            options={
                'ordering': ['display_order', 'id'],
            },
        ),
        migrations.AddField(
            model_name='achievement',
            name='technologies',
            field=models.ManyToManyField(blank=True, related_name='achievements', to='portfolio_app.technology'),
        ),
        migrations.AddField(
            model_name='certification',
            name='skills',
            field=models.ManyToManyField(blank=True, related_name='certifications', to='portfolio_app.skill'),
        ),
        migrations.AddField(
            model_name='project',
            name='technologies',
            field=models.ManyToManyField(blank=True, related_name='projects', to='portfolio_app.technology'),
        ),
        migrations.AlterField(
            model_name='education',
            name='degree',
            field=models.CharField(choices=[('school', 'School'), ('high_school', 'High School'), ('diploma', 'Diploma'), ('bachelor', "Bachelor's Degree"), ('master', "Master's Degree"), ('phd', 'PhD'), ('certificate', 'Certificate'), ('online', 'Online Course')], default='bachelor', max_length=20),
        ),
        migrations.AlterField(
            model_name='skill',
            name='proficiency',
            field=models.IntegerField(default=50, help_text='Proficiency level from 1 to 100', validators=[MinValueValidator(1), MaxValueValidator(100)]),
        ),
        migrations.RunPython(backfill_relations, migrations.RunPython.noop),
    ]
