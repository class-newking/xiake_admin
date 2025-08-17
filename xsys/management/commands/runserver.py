from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'runserver command is disabled. Use python manage.py run instead.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.ERROR('runserver command is disabled. Use python manage.py run instead.'))
        return
