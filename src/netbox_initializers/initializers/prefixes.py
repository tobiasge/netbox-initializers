from dcim.models import Site
from ipam.models import VLAN, VRF, Prefix, Role
from netaddr import IPNetwork
from tenancy.models import Tenant, TenantGroup

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["prefix", "site", "vrf", "vlan"]
OPTIONAL_ASSOCS = {
    "site": (Site, "name"),
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

            params["prefix"] = IPNetwork(params["prefix"])

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


register_initializer("prefixes", PrefixInitializer)
