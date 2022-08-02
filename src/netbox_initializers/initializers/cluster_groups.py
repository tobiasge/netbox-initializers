from virtualization.models import ClusterGroup

from . import BaseInitializer, register_initializer


class ClusterGroupInitializer(BaseInitializer):
    data_file_name = "cluster_groups.yml"

    def load_data(self):
        cluster_groups = self.load_yaml()
        if cluster_groups is None:
            return
        for params in cluster_groups:
            matching_params, defaults = self.split_params(params)
            cluster_group, created = ClusterGroup.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                print("🗄️ Created Cluster Group", cluster_group.name)


register_initializer("cluster_groups", ClusterGroupInitializer)
