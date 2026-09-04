from collections.abc import Mapping
from typing import ClassVar

from dcim.models import DeviceRole, Platform, Site
from tenancy.models import Tenant
from virtualization.models import Cluster, VirtualMachine

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class VirtualMachineInitializer(BaseModelInitializer):
    data_file_name = "virtual_machines.yml"
    model = VirtualMachine
    verbose_name = "virtual machine"
    emoji = "🖥️"
    match_params = ("cluster", "name")
    required_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"cluster": (Cluster, "name")}
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {
        "tenant": (Tenant, "name"),
        "site": (Site, "name"),
        "platform": (Platform, "name"),
        "role": (DeviceRole, "name"),
    }

    def prepare_params(self, params: dict[str, object]) -> dict[str, object] | None:
        # primary ips are handled later in the primary_ips initializer
        params.pop("primary_ip4", None)
        params.pop("primary_ip6", None)
        params.pop("primary_ip4_vrf", None)
        params.pop("primary_ip6_vrf", None)
        return params


register_initializer("virtual_machines", VirtualMachineInitializer)
