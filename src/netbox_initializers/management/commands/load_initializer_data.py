import os
import traceback

from django.core.management.base import BaseCommand, CommandError

from netbox_initializers.initializers import INITIALIZER_ORDER, INITIALIZER_REGISTRY


class Command(BaseCommand):
    help = "Load data from YAML files into Netbox"
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument(
            "--path", action="store", dest="path", help="Path of the initial data YAMLs"
        )

    def handle(self, *args, **options):
        target_path = options["path"]
        if not target_path:
            raise CommandError("Path cannot be empty.")

        if not os.path.isdir(target_path):
            raise CommandError("Path must be a directory.")

        for initializer_name in INITIALIZER_ORDER:
            if initializer_name not in INITIALIZER_REGISTRY:
                self.stderr.write(
                    self.style.ERROR(f"Initializer for {initializer_name} not found!")
                )
                continue

            initializer = INITIALIZER_REGISTRY[initializer_name]
            initializer_instance = initializer(target_path)
            try:
                initializer_instance.load_data()
            except Exception as e:
                traceback.print_exception(e)
                raise CommandError(f"{initializer.__name__} failed.") from e
