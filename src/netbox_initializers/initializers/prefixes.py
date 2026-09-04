from collections.abc import Mapping
from typing import ClassVar

from dcim.constants import LOCATION_SCOPE_TYPES
from ipam.models import VLAN, VRF, Prefix, Role
from netaddr import IPNetwork
from tenancy.models import Tenant, TenantGroup

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer
from netbox_initializers.initializers.utils import get_scope_details


class PrefixInitializer(BaseModelInitializer):
    data_file_name = "prefixes.yml"
    model = Prefix
    name_field = "prefix"
    verbose_name = "Prefix"
    emoji = "📌"
    match_params = ("prefix", "scope_type", "scope_id", "vrf", "vlan")
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {
        "tenant": (Tenant, "name"),
        "tenant_group": (TenantGroup, "name"),
        "vlan": (VLAN, "name"),
        "role": (Role, "name"),
        "vrf": (VRF, "name"),
    }

    def prepare_params(self, params: dict[str, object]) -> dict[str, object] | None:
        params["prefix"] = IPNetwork(str(params["prefix"]))
        if (scope := params.pop("scope", None)) and isinstance(scope, dict):
            params["scope_type"], params["scope_id"] = get_scope_details(scope, LOCATION_SCOPE_TYPES)
        return params


register_initializer("prefixes", PrefixInitializer)
