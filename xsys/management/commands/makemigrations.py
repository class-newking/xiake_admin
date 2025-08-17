from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Disabled command. Use syncdb instead.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.ERROR('makemigrations command is disabled. Use python manage.py syncdb instead.'))
        return
