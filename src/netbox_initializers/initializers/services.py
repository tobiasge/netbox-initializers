from dcim.models import Device
from ipam.models import Service
from virtualization.models import VirtualMachine

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["name", "device", "virtual_machine"]
OPTIONAL_ASSOCS = {
    "device": (Device, "name"),
    "virtual_machine": (VirtualMachine, "name"),
}


class ServiceInitializer(BaseInitializer):
    data_file_name = "services.yml"

    def load_data(self):
        services = self.load_yaml()
        if services is None:
            return
        for params in services:

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}
                    params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            service, created = Service.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("🧰 Created Service", service.name)


register_initializer("services", ServiceInitializer)
