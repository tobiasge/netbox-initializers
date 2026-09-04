from collections.abc import Mapping
from typing import ClassVar

from ipam.models import RIR, Aggregate
from netaddr import IPNetwork
from tenancy.models import Tenant

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class AggregateInitializer(BaseModelInitializer):
    data_file_name = "aggregates.yml"
    model = Aggregate
    name_field = "prefix"
    verbose_name = "Aggregate"
    emoji = "🗞️"
    match_params = ("prefix", "rir")
    required_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"rir": (RIR, "name")}
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {
        "tenant": (Tenant, "name"),
    }

    def prepare_params(self, params: dict[str, object]) -> dict[str, object] | None:
        params["prefix"] = IPNetwork(str(params["prefix"]))
        return params


register_initializer("aggregates", AggregateInitializer)
