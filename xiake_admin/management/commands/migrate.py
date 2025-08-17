from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Disabled command. Use syncdb instead.'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.ERROR(
                'migrate command is disabled. Use python manage.py syncdb instead.'
            )
        )