from dcim.models import Site
from tenancy.models import Tenant
from virtualization.models import Cluster, ClusterGroup, ClusterType

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["name", "type"]
REQUIRED_ASSOCS = {"type": (ClusterType, "name")}
OPTIONAL_ASSOCS = {
    "site": (Site, "name"),
    "group": (ClusterGroup, "name"),
    "tenant": (Tenant, "name"),
}


class ClusterInitializer(BaseInitializer):
    data_file_name = "clusters.yml"

    def load_data(self):
        clusters = self.load_yaml()
        if clusters is None:
            return
        for params in clusters:
            custom_field_data = self.pop_custom_fields(params)

            for assoc, details in REQUIRED_ASSOCS.items():
                model, field = details
                query = {field: params.pop(assoc)}

                params[assoc] = model.objects.get(**query)

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}

                    params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            cluster, created = Cluster.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("🗄️ Created cluster", cluster.name)

            self.set_custom_fields_values(cluster, custom_field_data)


register_initializer("clusters", ClusterInitializer)
