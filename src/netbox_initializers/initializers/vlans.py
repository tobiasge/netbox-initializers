from dcim.models import Site
from ipam.models import VLAN, Role, VLANGroup
from tenancy.models import Tenant, TenantGroup

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["name", "vid"]
OPTIONAL_ASSOCS = {
    "site": (Site, "name"),
    "tenant": (Tenant, "name"),
    "tenant_group": (TenantGroup, "name"),
    "group": (VLANGroup, "name"),
    "role": (Role, "name"),
}


class VLANInitializer(BaseInitializer):
    data_file_name = "vlans.yml"

    def load_data(self):
        vlans = self.load_yaml()
        if vlans is None:
            return
        for params in vlans:
            custom_field_data = self.pop_custom_fields(params)

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}

                    params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            vlan, created = VLAN.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("🏠 Created VLAN", vlan.name)

            self.set_custom_fields_values(vlan, custom_field_data)


register_initializer("vlans", VLANInitializer)
