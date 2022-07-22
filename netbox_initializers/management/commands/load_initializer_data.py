from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load data from YAML files into Netbox"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path", action='store', dest='path',
            help="Path of the initial data YAMLs"
        )

    def handle(self, *args, **options):
        pass
