from dcim import models as dcim
from extras.models import ConfigContext
from tenancy import models as tenancy
from virtualization import models as virtualization

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["name"]
OPTIONAL_MANY_ASSOCS = {
    "regions": (dcim.Region, "name"),
    "site_groups": (dcim.SiteGroup, "name"),
    "sites": (dcim.Site, "name"),
    "locations": (dcim.Location, "name"),
    "device_types": (dcim.DeviceType, "model"),
    "roles": (dcim.DeviceRole, "name"),
    "platforms": (dcim.Platform, "name"),
    "cluster_types": (virtualization.ClusterType, "name"),
    "cluster_groups": (virtualization.ClusterGroup, "name"),
    "clusters": (virtualization.Cluster, "name"),
    "tenant_groups": (tenancy.TenantGroup, "name"),
    "tenants": (tenancy.Tenant, "name"),
}


class ConfigContextInitializer(BaseInitializer):
    data_file_name = "config_contexts.yml"

    def load_data(self):
        contexts = self.load_yaml()
        if contexts is None:
            return
        for params in contexts:
            tags = params.pop("tags", None)

            # siphon off params that represent many to many relationships
            many_assocs = {}
            for many_assoc in OPTIONAL_MANY_ASSOCS.keys():
                if many_assoc in params:
                    many_assocs[many_assoc] = params.pop(many_assoc)

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            context, created = ConfigContext.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            # process the many to many relationships
            for assoc_field, assocs in many_assocs.items():
                model, field = OPTIONAL_MANY_ASSOCS[assoc_field]
                for assoc in assocs:
                    query = {field: assoc}
                    getattr(context, assoc_field).add(model.objects.get(**query))

            if created:
                print("🖥️  Created config context", context.name)

            self.set_tags(context, tags)


register_initializer("config_contexts", ConfigContextInitializer)
