from collections.abc import Mapping
from typing import ClassVar

from dcim.models import Manufacturer, Platform
from extras.models import ConfigTemplate

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class PlatformInitializer(BaseModelInitializer):
    data_file_name = "platforms.yml"
    model = Platform
    verbose_name = "platform"
    emoji = "💾"
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {
        "manufacturer": (Manufacturer, "name"),
        "config_template": (ConfigTemplate, "name"),
    }


register_initializer("platforms", PlatformInitializer)
