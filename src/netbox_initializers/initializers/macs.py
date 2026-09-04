from dcim.models import MACAddress

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class MACAddressInitializer(BaseModelInitializer):
    data_file_name = "macs.yml"
    model = MACAddress
    name_field = "mac_address"
    verbose_name = "MAC Address"
    emoji = "🗺️"
    match_params = ("mac_address",)


register_initializer("macs", MACAddressInitializer)
