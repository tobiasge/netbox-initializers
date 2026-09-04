import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netbox.settings")
os.environ.setdefault("NETBOX_CONFIGURATION", "netbox.configuration_testing")

django.setup()
