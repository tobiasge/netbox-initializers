from collections.abc import Mapping
from typing import ClassVar

from dcim.models import Manufacturer, RackType

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class RackTypeInitializer(BaseModelInitializer):
    data_file_name = "rack_types.yml"
    model = RackType
    name_field = "model"
    verbose_name = "rack type"
    emoji = "🔳"
    match_params = ("slug",)
    required_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"manufacturer": (Manufacturer, "slug")}


register_initializer("rack_types", RackTypeInitializer)
