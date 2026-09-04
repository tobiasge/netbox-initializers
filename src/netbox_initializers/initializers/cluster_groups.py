from virtualization.models import ClusterGroup

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class ClusterGroupInitializer(BaseModelInitializer):
    data_file_name = "cluster_groups.yml"
    model = ClusterGroup
    verbose_name = "Cluster Group"
    emoji = "🗄️"


register_initializer("cluster_groups", ClusterGroupInitializer)
