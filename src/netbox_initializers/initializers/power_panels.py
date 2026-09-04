from collections.abc import Mapping
from typing import ClassVar

from dcim.models import Location, PowerPanel, Site

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class PowerPanelInitializer(BaseModelInitializer):
    data_file_name = "power_panels.yml"
    model = PowerPanel
    match_params = ("name", "site")
    required_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"site": (Site, "name")}
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"location": (Location, "name")}

    def print_created(self, entity) -> None:
        self.log(f"⚡ Created Power Panel {entity.site} {entity.name}")


register_initializer("power_panels", PowerPanelInitializer)
