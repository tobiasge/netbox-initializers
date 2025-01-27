from dcim.models import MACAddress

from netbox_initializers.initializers.base import BaseInitializer, register_initializer


class MACAddressInitializer(BaseInitializer):
    data_file_name = "macs.yml"

    def load_data(self):
        macs = self.load_yaml()
        if macs is None:
            return

        for mac in macs:
            tags = mac.pop("tags", None)
            macaddress, created = MACAddress.objects.get_or_create(**mac)

            if created:
                print("🗺️ Created MAC Address", macaddress.mac_address)

            self.set_tags(macaddress, tags)


register_initializer("macs", MACAddressInitializer)
