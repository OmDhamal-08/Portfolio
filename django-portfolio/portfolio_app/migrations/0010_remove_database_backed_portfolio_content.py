from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_app', '0009_contactmessage_resume'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProjectImage',
        ),
        migrations.RemoveField(
            model_name='achievement',
            name='technologies',
        ),
        migrations.RemoveField(
            model_name='certification',
            name='skills',
        ),
        migrations.RemoveField(
            model_name='project',
            name='technologies',
        ),
        migrations.DeleteModel(
            name='Achievement',
        ),
        migrations.DeleteModel(
            name='Certification',
        ),
        migrations.DeleteModel(
            name='Education',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
        migrations.DeleteModel(
            name='Technology',
        ),
    ]
