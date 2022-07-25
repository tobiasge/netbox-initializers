import os
import shutil

from django.core.management.base import BaseCommand, CommandError

import netbox_initializers.initializers


class Command(BaseCommand):
    help = "Copy initializer example files to user specified directory"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            action="store",
            dest="path",
            help="Path where the examples should be placed",
            required=True,
        )

    def handle(self, *args, **options):
        target_path = options["path"]
        if not target_path:
            raise CommandError("Path cannot be empty.")

        if not os.path.isdir(target_path):
            raise CommandError("Path must be a directory.")

        intializer_base_path = os.path.dirname(netbox_initializers.initializers.__file__)
        intializer_path = f"{intializer_base_path}/yaml"
        warnings = 0
        with os.scandir(intializer_path) as yaml_files:
            for file in yaml_files:
                if not file.name.endswith("yml"):
                    continue
                dst_file = f"{target_path}/{file.name}"
                if os.path.isfile(dst_file):
                    self.stdout.write(
                        self.style.WARNING(
                            f"Warning: Destination file exists for {file.name}. File will not be copied."
                        )
                    )
                    warnings += 1
                    continue
                shutil.copyfile(file, dst_file)
        self.stdout.write(
            self.style.SUCCESS(
                f"Copied initializer examples to '{target_path}' with {warnings} warnings."
            )
        )
