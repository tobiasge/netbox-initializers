from collections.abc import Mapping
from typing import ClassVar

from dcim.models import Site
from tenancy.models import Tenant
from virtualization.models import Cluster, ClusterGroup, ClusterType

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class ClusterInitializer(BaseModelInitializer):
    data_file_name = "clusters.yml"
    model = Cluster
    verbose_name = "cluster"
    emoji = "🗄️"
    match_params = ("name", "type")
    required_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"type": (ClusterType, "name")}
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {
        "scope": (Site, "name"),
        "group": (ClusterGroup, "name"),
        "tenant": (Tenant, "name"),
    }


register_initializer("clusters", ClusterInitializer)
