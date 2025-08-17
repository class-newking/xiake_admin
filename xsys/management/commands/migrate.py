from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Custom migrate command with restrictions'

    def handle(self, *args, **options):
        self.stdout.write(self.style.ERROR("Migration is completely disabled. Please use syncdb command instead."))
        return
