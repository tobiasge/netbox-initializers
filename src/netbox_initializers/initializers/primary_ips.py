from dcim.models import Device
from ipam.models import IPAddress
from virtualization.models import VirtualMachine

from . import BaseInitializer, register_initializer

OPTIONAL_ASSOCS = {
    "primary_ip4": (IPAddress, "address"),
    "primary_ip6": (IPAddress, "address"),
}


def link_primary_ip(assets, asset_model):
    for params in assets:
        primary_ip_fields = set(params) & {"primary_ip4", "primary_ip6"}
        if not primary_ip_fields:
            continue

        for assoc, details in OPTIONAL_ASSOCS.items():
            if assoc in params:
                model, field = details
                query = {field: params.pop(assoc)}

                try:
                    params[assoc] = model.objects.get(**query)
                except model.DoesNotExist:
                    primary_ip_fields -= {assoc}
                    print(f"⚠️ IP Address '{query[field]}' not found")

        asset = asset_model.objects.get(name=params["name"])
        for field in primary_ip_fields:
            if getattr(asset, field) != params[field]:
                setattr(asset, field, params[field])
                print(f"🔗 Define primary IP '{params[field].address}' on '{asset.name}'")
        asset.save()


class PrimaryIPInitializer(BaseInitializer):
    def load_data(self):
        devices = self.load_yaml(data_file_name="devices.yml")
        virtual_machines = self.load_yaml(data_file_name="virtual_machines.yml")

        if devices is None and virtual_machines is None:
            return
        if devices is not None:
            link_primary_ip(devices, Device)
        if virtual_machines is not None:
            link_primary_ip(virtual_machines, VirtualMachine)


register_initializer("primary_ips", PrimaryIPInitializer)
