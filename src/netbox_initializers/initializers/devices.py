from collections.abc import Mapping
from typing import ClassVar

from dcim.models import Device, DeviceRole, DeviceType, Location, Platform, Rack, Site
from extras.models import ConfigTemplate
from tenancy.models import Tenant
from virtualization.models import Cluster

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class DeviceInitializer(BaseModelInitializer):
    data_file_name = "devices.yml"
    model = Device
    verbose_name = "device"
    emoji = "🖥️"
    match_params = ("device_type", "name", "site")
    required_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {
        "role": (DeviceRole, "name"),
        "device_type": (DeviceType, "model"),
        "site": (Site, "name"),
    }
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {
        "cluster": (Cluster, "name"),
        "config_template": (ConfigTemplate, "name"),
        "location": (Location, "name"),
        "platform": (Platform, "name"),
        "rack": (Rack, "name"),
        "tenant": (Tenant, "name"),
    }

    def prepare_params(self, params: dict[str, object]) -> dict[str, object] | None:
        # primary ips are handled later in the primary_ips initializer
        params.pop("primary_ip4", None)
        params.pop("primary_ip6", None)
        params.pop("primary_ip4_vrf", None)
        params.pop("primary_ip6_vrf", None)
        return params


register_initializer("devices", DeviceInitializer)
