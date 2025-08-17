from django.core.management.commands.runserver import Command as RunserverCommand


class Command(RunserverCommand):
    help = 'Runs the development server (alias for runserver)'

    def handle(self, *args, **options):
        # 直接调用runserver的handle方法
        super().handle(*args, **options)