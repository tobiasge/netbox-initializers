from dcim.models import Device
from ipam.models import Service
from ipam.models import FHRPGroup
from virtualization.models import VirtualMachine
from django.contrib.contenttypes.models import ContentType

from netbox_initializers.initializers.base import BaseInitializer, register_initializer

MATCH_PARAMS = ["name", "parent_object_type", "parent_object_id"]

class ServiceInitializer(BaseInitializer):
    data_file_name = "services.yml"

    def load_data(self):
        services = self.load_yaml()
        if services is None:
            return
        for params in services:
            tags = params.pop("tags", None)

            # Check for each parent type (device, virtual_machine, fhrp_group)
            if "device" in params:
                parent = Device.objects.get(name=params.pop("device"))
            elif "virtual_machine" in params:
                parent = VirtualMachine.objects.get(name=params.pop("virtual_machine"))
            elif "fhrp_group" in params:
                parent = FHRPGroup.objects.get(name=params.pop("fhrp_group"))
            else:
                raise ValueError(
                    "A parent (device, virtual_machine, or fhrp_group) must be specified for the service."
                )

            params["parent_object_type"] = ContentType.objects.get_for_model(parent)
            params["parent_object_id"] = parent.id

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            service, created = Service.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("🧰 Created Service", service.name)

            self.set_tags(service, tags)


register_initializer("services", ServiceInitializer)
