from virtualization.models import ClusterType

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class ClusterTypesInitializer(BaseModelInitializer):
    data_file_name = "cluster_types.yml"
    model = ClusterType
    verbose_name = "Cluster Type"
    emoji = "🧰"


register_initializer("cluster_types", ClusterTypesInitializer)
