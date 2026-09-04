from collections.abc import Mapping
from typing import ClassVar

from dcim.models import Location, Rack, RackRole, RackType, Site
from tenancy.models import Tenant

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class RackInitializer(BaseModelInitializer):
    data_file_name = "racks.yml"
    model = Rack
    match_params = ("name", "site")
    required_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"site": (Site, "name")}
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {
        "role": (RackRole, "name"),
        "tenant": (Tenant, "name"),
        "location": (Location, "name"),
        "rack_type": (RackType, "slug"),
    }

    def print_created(self, entity) -> None:
        self.log(f"🔳 Created rack {entity.site} {entity.name}")


register_initializer("racks", RackInitializer)
