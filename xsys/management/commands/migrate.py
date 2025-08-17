from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Disabled command. Use syncdb instead.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.ERROR("Migration is completely disabled. Please use syncdb command instead."))
        return
