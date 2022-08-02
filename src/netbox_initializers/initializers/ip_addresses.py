from dcim.models import Device, Interface
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from ipam.models import VRF, IPAddress
from netaddr import IPNetwork
from tenancy.models import Tenant
from virtualization.models import VirtualMachine, VMInterface

from . import BaseInitializer, InitializationError, register_initializer

MATCH_PARAMS = ["address", "vrf"]
OPTIONAL_ASSOCS = {
    "tenant": (Tenant, "name"),
    "vrf": (VRF, "name"),
    "interface": (Interface, "name"),
}

VM_INTERFACE_CT = ContentType.objects.filter(
    Q(app_label="virtualization", model="vminterface")
).first()
INTERFACE_CT = ContentType.objects.filter(Q(app_label="dcim", model="interface")).first()


class IPAddressInitializer(BaseInitializer):
    data_file_name = "ip_addresses.yml"

    def load_data(self):
        ip_addresses = self.load_yaml()
        if ip_addresses is None:
            return
        for params in ip_addresses:
            custom_field_data = self.pop_custom_fields(params)

            vm = params.pop("virtual_machine", None)
            device = params.pop("device", None)
            params["address"] = IPNetwork(params["address"])

            if vm and device:
                raise InitializationError(
                    "IP Address can only specify one of the following: virtual_machine or device."
                )

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    if assoc == "interface":
                        if vm:
                            vm_id = VirtualMachine.objects.get(name=vm).id
                            query = {"name": params.pop(assoc), "virtual_machine_id": vm_id}
                            params["assigned_object_type"] = VM_INTERFACE_CT
                            params["assigned_object_id"] = VMInterface.objects.get(**query).id
                        elif device:
                            dev_id = Device.objects.get(name=device).id
                            query = {"name": params.pop(assoc), "device_id": dev_id}
                            params["assigned_object_type"] = INTERFACE_CT
                            params["assigned_object_id"] = Interface.objects.get(**query).id
                    else:
                        query = {field: params.pop(assoc)}

                        params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            ip_address, created = IPAddress.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                print("🧬 Created IP Address", ip_address.address)

            self.set_custom_fields_values(ip_address, custom_field_data)


register_initializer("ip_addresses", IPAddressInitializer)
