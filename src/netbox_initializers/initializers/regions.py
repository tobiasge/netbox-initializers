from collections.abc import Mapping
from typing import ClassVar

from dcim.models import Region

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class RegionInitializer(BaseModelInitializer):
    data_file_name = "regions.yml"
    model = Region
    verbose_name = "region"
    emoji = "🌐"
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"parent": (Region, "name")}


register_initializer("regions", RegionInitializer)
