from collections.abc import Mapping
from typing import ClassVar

from dcim.models import MACAddress
from virtualization.models import VirtualMachine, VMInterface

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class VMInterfaceInitializer(BaseModelInitializer):
    data_file_name = "virtualization_interfaces.yml"
    model = VMInterface
    match_params = ("name", "virtual_machine")
    required_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"virtual_machine": (VirtualMachine, "name")}
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"primary_mac_address": (MACAddress, "mac_address")}

    def print_created(self, entity) -> None:
        self.log(f"🧷 Created interface {entity.name} {entity.virtual_machine.name}")


register_initializer("virtualization_interfaces", VMInterfaceInitializer)
