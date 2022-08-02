from dcim.models import DeviceRole, Platform
from tenancy.models import Tenant
from virtualization.models import Cluster, VirtualMachine

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["cluster", "name"]
REQUIRED_ASSOCS = {"cluster": (Cluster, "name")}
OPTIONAL_ASSOCS = {
    "tenant": (Tenant, "name"),
    "platform": (Platform, "name"),
    "role": (DeviceRole, "name"),
}


class VirtualMachineInitializer(BaseInitializer):
    data_file_name = "virtual_machines.yml"

    def load_data(self):
        virtual_machines = self.load_yaml()
        if virtual_machines is None:
            return
        for params in virtual_machines:
            custom_field_data = self.pop_custom_fields(params)

            # primary ips are handled later in `270_primary_ips.py`
            params.pop("primary_ip4", None)
            params.pop("primary_ip6", None)

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
            virtual_machine, created = VirtualMachine.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                print("🖥️ Created virtual machine", virtual_machine.name)

            self.set_custom_fields_values(virtual_machine, custom_field_data)


register_initializer("virtual_machines", VirtualMachineInitializer)
