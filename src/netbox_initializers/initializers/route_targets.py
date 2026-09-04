from collections.abc import Mapping
from typing import ClassVar

from ipam.models import RouteTarget
from tenancy.models import Tenant

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class RouteTargetInitializer(BaseModelInitializer):
    data_file_name = "route_targets.yml"
    model = RouteTarget
    verbose_name = "Route Target"
    emoji = "🎯"
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"tenant": (Tenant, "name")}


register_initializer("route_targets", RouteTargetInitializer)
