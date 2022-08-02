from dcim.models import Device, DeviceRole, DeviceType, Location, Platform, Rack, Site
from tenancy.models import Tenant
from virtualization.models import Cluster

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["device_type", "name", "site"]
REQUIRED_ASSOCS = {
    "device_role": (DeviceRole, "name"),
    "device_type": (DeviceType, "model"),
    "site": (Site, "name"),
}
OPTIONAL_ASSOCS = {
    "tenant": (Tenant, "name"),
    "platform": (Platform, "name"),
    "rack": (Rack, "name"),
    "cluster": (Cluster, "name"),
    "location": (Location, "name"),
}


class DeviceInitializer(BaseInitializer):
    data_file_name = "devices.yml"

    def load_data(self):
        devices = self.load_yaml()
        if devices is None:
            return
        for params in devices:
            custom_field_data = self.pop_custom_fields(params)

            # primary ips are handled later in `380_primary_ips.py`
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
            device, created = Device.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("🖥️  Created device", device.name)

            self.set_custom_fields_values(device, custom_field_data)


register_initializer("devices", DeviceInitializer)
