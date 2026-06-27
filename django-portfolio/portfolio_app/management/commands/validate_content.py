from django.core.management.base import BaseCommand, CommandError

from portfolio_app.content_loader import validate_content


class Command(BaseCommand):
    help = 'Validate file-backed portfolio content.'

    def handle(self, *args, **options):
        errors = validate_content()
        if errors:
            for error in errors:
                self.stderr.write(self.style.ERROR(error))
            raise CommandError('Portfolio content validation failed.')

        self.stdout.write(self.style.SUCCESS('Portfolio content files are valid.'))
