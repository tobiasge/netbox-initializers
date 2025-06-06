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

            # Get model from Contenttype
            scope_type = params.pop("parent_type", None)
            if not scope_type:
                print(
                    f"Services '{params['name']}': parent_type is missing from Services"
                )
            app_label, model = str(scope_type).split(".")
            parent_model = ContentType.objects.get(app_label=app_label, model=model).model_class()
            #parent_model = ContentType.objects.filter(app_label=app_label, model=model).first()
            parent = parent_model.objects.get(name=params.pop("parent_name"))

            params["parent_object_type"] = ContentType.objects.get_for_model(parent)
            params["parent_object_id"] = parent.id

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            service, created = Service.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("🧰 Created Service", service.name)

            self.set_tags(service, tags)


register_initializer("services", ServiceInitializer)
