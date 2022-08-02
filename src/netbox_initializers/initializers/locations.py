from dcim.models import Location, Site

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["name", "slug", "site"]
REQUIRED_ASSOCS = {"site": (Site, "name")}


class LocationInitializer(BaseInitializer):
    data_file_name = "locations.yml"

    def load_data(self):
        locations = self.load_yaml()
        if locations is None:
            return
        for params in locations:

            for assoc, details in REQUIRED_ASSOCS.items():
                model, field = details
                query = {field: params.pop(assoc)}
                params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            location, created = Location.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("🎨 Created location", location.name)


register_initializer("locations", LocationInitializer)
