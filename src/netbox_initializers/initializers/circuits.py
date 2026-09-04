from collections.abc import Mapping
from typing import ClassVar

from circuits.models import Circuit, CircuitType, Provider
from tenancy.models import Tenant

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class CircuitInitializer(BaseModelInitializer):
    data_file_name = "circuits.yml"
    model = Circuit
    name_field = "cid"
    verbose_name = "Circuit"
    emoji = "⚡"
    match_params = ("cid", "provider", "type")
    required_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {
        "provider": (Provider, "name"),
        "type": (CircuitType, "name"),
    }
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {
        "tenant": (Tenant, "name"),
    }


register_initializer("circuits", CircuitInitializer)
