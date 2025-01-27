from dcim.constants import LOCATION_SCOPE_TYPES
from ipam.models import VLAN, VRF, Prefix, Role
from netaddr import IPNetwork
from tenancy.models import Tenant, TenantGroup

from netbox_initializers.initializers.base import BaseInitializer, register_initializer
from netbox_initializers.initializers.utils import get_scope_details

MATCH_PARAMS = ["prefix", "scope", "vrf", "vlan"]
OPTIONAL_ASSOCS = {
    "tenant": (Tenant, "name"),
    "tenant_group": (TenantGroup, "name"),
    "vlan": (VLAN, "name"),
    "role": (Role, "name"),
    "vrf": (VRF, "name"),
}


class PrefixInitializer(BaseInitializer):
    data_file_name = "prefixes.yml"

    def load_data(self):
        prefixes = self.load_yaml()
        if prefixes is None:
            return
        for params in prefixes:
            custom_field_data = self.pop_custom_fields(params)
            tags = params.pop("tags", None)

            params["prefix"] = IPNetwork(params["prefix"])

            if scope := params.pop("scope"):
                params["scope_type"], params["scope_id"] = get_scope_details(scope, LOCATION_SCOPE_TYPES)

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}
                    params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            prefix, created = Prefix.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("📌 Created Prefix", prefix.prefix)

            self.set_custom_fields_values(prefix, custom_field_data)
            self.set_tags(prefix, tags)


register_initializer("prefixes", PrefixInitializer)
