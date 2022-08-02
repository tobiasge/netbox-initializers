from dcim.models import Region

from . import BaseInitializer, register_initializer

OPTIONAL_ASSOCS = {"parent": (Region, "name")}


class RegionInitializer(BaseInitializer):
    data_file_name = "regions.yml"

    def load_data(self):
        regions = self.load_yaml()
        if regions is None:
            return
        for params in regions:

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}

                    params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params)
            region, created = Region.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("🌐 Created region", region.name)


register_initializer("regions", RegionInitializer)
