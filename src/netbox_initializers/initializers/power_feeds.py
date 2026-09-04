from collections.abc import Mapping
from typing import ClassVar

from dcim.models import PowerFeed, PowerPanel, Rack

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class PowerFeedInitializer(BaseModelInitializer):
    data_file_name = "power_feeds.yml"
    model = PowerFeed
    verbose_name = "Power Feed"
    emoji = "⚡"
    match_params = ("name", "power_panel")
    required_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"power_panel": (PowerPanel, "name")}
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"rack": (Rack, "name")}


register_initializer("power_feeds", PowerFeedInitializer)
