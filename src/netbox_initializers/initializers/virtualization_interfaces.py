from dcim.models import MACAddress
from virtualization.models import VirtualMachine, VMInterface

from netbox_initializers.initializers.base import BaseInitializer, register_initializer

MATCH_PARAMS = ["name", "virtual_machine"]
REQUIRED_ASSOCS = {"virtual_machine": (VirtualMachine, "name")}
OPTIONAL_ASSOCS = {"primary_mac_address": (MACAddress, "mac_address")}


class VMInterfaceInitializer(BaseInitializer):
    data_file_name = "virtualization_interfaces.yml"

    def load_data(self):
        interfaces = self.load_yaml()
        if interfaces is None:
            return
        for params in interfaces:
            custom_field_data = self.pop_custom_fields(params)
            tags = params.pop("tags", None)
            mac_addresses = params.pop("mac_addresses", None)

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
            interface, created = VMInterface.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                print("🧷 Created interface", interface.name, interface.virtual_machine.name)

            self.set_custom_fields_values(interface, custom_field_data)
            self.set_tags(interface, tags)
            self.set_mac_addresses(interface, mac_addresses)


register_initializer("virtualization_interfaces", VMInterfaceInitializer)
