from virtualization.models import VirtualMachine, VMInterface

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["name", "virtual_machine"]
REQUIRED_ASSOCS = {"virtual_machine": (VirtualMachine, "name")}


class VMInterfaceInitializer(BaseInitializer):
    data_file_name = "virtualization_interfaces.yml"

    def load_data(self):
        interfaces = self.load_yaml()
        if interfaces is None:
            return
        for params in interfaces:
            custom_field_data = self.pop_custom_fields(params)

            for assoc, details in REQUIRED_ASSOCS.items():
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


register_initializer("virtualization_interfaces", VMInterfaceInitializer)
