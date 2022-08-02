from dcim.models import Location, Rack, RackRole, Site
from tenancy.models import Tenant

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["name", "site"]
REQUIRED_ASSOCS = {"site": (Site, "name")}
OPTIONAL_ASSOCS = {
    "role": (RackRole, "name"),
    "tenant": (Tenant, "name"),
    "location": (Location, "name"),
}


class RackInitializer(BaseInitializer):
    data_file_name = "racks.yml"

    def load_data(self):
        racks = self.load_yaml()
        if racks is None:
            return
        for params in racks:
            custom_field_data = self.pop_custom_fields(params)

            for assoc, details in REQUIRED_ASSOCS.items():
                model, field = details
                query = {field: params.pop(assoc)}

                params[assoc] = model.objects.get(**query)

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}

                    params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            rack, created = Rack.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("🔳 Created rack", rack.site, rack.name)

            self.set_custom_fields_values(rack, custom_field_data)


register_initializer("racks", RackInitializer)
