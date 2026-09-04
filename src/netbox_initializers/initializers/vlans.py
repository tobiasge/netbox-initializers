from collections.abc import Mapping
from typing import ClassVar

from dcim.models import Site
from ipam.models import VLAN, Role, VLANGroup
from tenancy.models import Tenant, TenantGroup

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class VLANInitializer(BaseModelInitializer):
    data_file_name = "vlans.yml"
    model = VLAN
    verbose_name = "VLAN"
    emoji = "🏠"
    match_params = ("name", "vid")
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {
        "site": (Site, "name"),
        "tenant": (Tenant, "name"),
        "tenant_group": (TenantGroup, "name"),
        "group": (VLANGroup, "name"),
        "role": (Role, "name"),
    }


register_initializer("vlans", VLANInitializer)
