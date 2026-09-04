from collections.abc import Mapping
from typing import ClassVar

from ipam.models import VRF
from tenancy.models import Tenant

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class VRFInitializer(BaseModelInitializer):
    data_file_name = "vrfs.yml"
    model = VRF
    verbose_name = "VRF"
    emoji = "📦"
    match_params = ("name", "rd")
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"tenant": (Tenant, "name")}


register_initializer("vrfs", VRFInitializer)
