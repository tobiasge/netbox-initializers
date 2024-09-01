from dcim.models import Manufacturer, RackType

from netbox_initializers.initializers.base import BaseInitializer, register_initializer

MATCH_PARAMS = ["slug"]
REQUIRED_ASSOCS = {"manufacturer": (Manufacturer, "slug")}


class RackTypeInitializer(BaseInitializer):
    data_file_name = "rack_types.yml"

    def load_data(self):
        rack_types = self.load_yaml()
        if rack_types is None:
            return
        for params in rack_types:

            for assoc, details in REQUIRED_ASSOCS.items():
                model, field = details
                query = {field: params.pop(assoc)}

                params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            rack_type, created = RackType.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                print("🔳 Created rack type", rack_type.model)


register_initializer("rack_types", RackTypeInitializer)
