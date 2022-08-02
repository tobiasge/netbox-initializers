from ipam.models import RouteTarget
from tenancy.models import Tenant

from . import BaseInitializer, register_initializer

OPTIONAL_ASSOCS = {"tenant": (Tenant, "name")}


class RouteTargetInitializer(BaseInitializer):
    data_file_name = "route_targets.yml"

    def load_data(self):
        route_targets = self.load_yaml()
        if route_targets is None:
            return
        for params in route_targets:
            custom_field_data = self.pop_custom_fields(params)

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}

                    params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params)
            route_target, created = RouteTarget.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                print("🎯 Created Route Target", route_target.name)

            self.set_custom_fields_values(route_target, custom_field_data)


register_initializer("route_targets", RouteTargetInitializer)
