from collections.abc import Mapping
from typing import ClassVar

from dcim.models import SiteGroup

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class SiteGroupInitializer(BaseModelInitializer):
    data_file_name = "site_groups.yml"
    model = SiteGroup
    verbose_name = "Site Group"
    emoji = "🌐"
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"parent": (SiteGroup, "name")}


register_initializer("site_groups", SiteGroupInitializer)
