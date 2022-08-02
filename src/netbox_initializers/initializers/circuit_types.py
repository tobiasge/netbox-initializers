from circuits.models import CircuitType

from . import BaseInitializer, register_initializer


class CircuitTypeInitializer(BaseInitializer):
    data_file_name = "circuit_types.yml"

    def load_data(self):
        circuit_types = self.load_yaml()
        if circuit_types is None:
            return
        for params in circuit_types:
            custom_field_data = self.pop_custom_fields(params)

            matching_params, defaults = self.split_params(params)
            circuit_type, created = CircuitType.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                print("⚡ Created Circuit Type", circuit_type.name)

            self.set_custom_fields_values(circuit_type, custom_field_data)


register_initializer("circuit_types", CircuitTypeInitializer)
