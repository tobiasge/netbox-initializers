from ipam.models import RIR, Aggregate
from netaddr import IPNetwork
from tenancy.models import Tenant

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["prefix", "rir"]
REQUIRED_ASSOCS = {"rir": (RIR, "name")}
OPTIONAL_ASSOCS = {
    "tenant": (Tenant, "name"),
}


class AggregateInitializer(BaseInitializer):
    data_file_name = "aggregates.yml"

    def load_data(self):
        aggregates = self.load_yaml()
        if aggregates is None:
            return
        for params in aggregates:
            custom_field_data = self.pop_custom_fields(params)

            params["prefix"] = IPNetwork(params["prefix"])

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
            aggregate, created = Aggregate.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                print("🗞️ Created Aggregate", aggregate.prefix)

            self.set_custom_fields_values(aggregate, custom_field_data)


register_initializer("aggregates", AggregateInitializer)
