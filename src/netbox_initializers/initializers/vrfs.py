from ipam.models import VRF
from tenancy.models import Tenant

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["name", "rd"]
OPTIONAL_ASSOCS = {"tenant": (Tenant, "name")}


class VRFInitializer(BaseInitializer):
    data_file_name = "vrfs.yml"

    def load_data(self):
        vrfs = self.load_yaml()
        if vrfs is None:
            return
        for params in vrfs:
            custom_field_data = self.pop_custom_fields(params)

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}

                    params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            vrf, created = VRF.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("📦 Created VRF", vrf.name)

            self.set_custom_fields_values(vrf, custom_field_data)


register_initializer("vrfs", VRFInitializer)
