from dcim.models import Manufacturer

from . import BaseInitializer, register_initializer


class ManufacturerInitializer(BaseInitializer):
    data_file_name = "manufacturers.yml"

    def load_data(self):
        manufacturers = self.load_yaml()
        if manufacturers is None:
            return
        for params in manufacturers:
            matching_params, defaults = self.split_params(params)
            manufacturer, created = Manufacturer.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                print("🏭 Created Manufacturer", manufacturer.name)


register_initializer("manufacturers", ManufacturerInitializer)
