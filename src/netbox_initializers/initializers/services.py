from dcim.models import Device
from ipam.models import Service
from ipam.models import FHRPGroup
from virtualization.models import VirtualMachine
from django.contrib.contenttypes.models import ContentType

from netbox_initializers.initializers.base import BaseInitializer, register_initializer

MATCH_PARAMS = ["name", "parent_type", "parent_id"]
OPTIONAL_ASSOCS = {
    "device": Device,
    "virtual_machine": VirtualMachine,
    "fhrp_group": FHRPGroup,
}


class ServiceInitializer(BaseInitializer):
    data_file_name = "services.yml"

    def load_data(self):
        services = self.load_yaml()
        if services is None:
            return
        for params in services:
            tags = params.pop("tags", None)

            # Handle the required parent relationship
            parent = None
            for assoc, model in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    query = {"name": params.pop(assoc)}
                    parent = model.objects.get(**query)
                    break

            if parent:
                params["parent_type"] = ContentType.objects.get_for_model(parent)
                params["parent_id"] = parent.id
            else:
                raise ValueError("A parent (device, virtual_machine, or fhrp group) must be specified for the service.")

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            service, created = Service.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("🧰 Created Service", service.name)

            self.set_tags(service, tags)


register_initializer("services", ServiceInitializer)
