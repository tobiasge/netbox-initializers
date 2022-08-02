from circuits.models import Circuit, CircuitType, Provider
from tenancy.models import Tenant

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["cid", "provider", "type"]
REQUIRED_ASSOCS = {"provider": (Provider, "name"), "type": (CircuitType, "name")}
OPTIONAL_ASSOCS = {"tenant": (Tenant, "name")}


class CircuitInitializer(BaseInitializer):
    data_file_name = "circuits.yml"

    def load_data(self):
        circuits = self.load_yaml()
        if circuits is None:
            return
        for params in circuits:
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
            circuit, created = Circuit.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("⚡ Created Circuit", circuit.cid)

            self.set_custom_fields_values(circuit, custom_field_data)


register_initializer("circuits", CircuitInitializer)
