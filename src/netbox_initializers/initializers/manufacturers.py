from dcim.models import Manufacturer

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class ManufacturerInitializer(BaseModelInitializer):
    data_file_name = "manufacturers.yml"
    model = Manufacturer
    verbose_name = "Manufacturer"
    emoji = "🏭"


register_initializer("manufacturers", ManufacturerInitializer)
