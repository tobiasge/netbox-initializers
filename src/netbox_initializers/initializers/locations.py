from collections.abc import Mapping
from typing import ClassVar

from dcim.models import Location, Site

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class LocationInitializer(BaseModelInitializer):
    data_file_name = "locations.yml"
    model = Location
    verbose_name = "location"
    emoji = "🎨"
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"site": (Site, "name"), "parent": (Location, "name")}


register_initializer("locations", LocationInitializer)
