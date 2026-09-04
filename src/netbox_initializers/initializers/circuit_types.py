from circuits.models import CircuitType

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class CircuitTypeInitializer(BaseModelInitializer):
    data_file_name = "circuit_types.yml"
    model = CircuitType
    verbose_name = "Circuit Type"
    emoji = "⚡"


register_initializer("circuit_types", CircuitTypeInitializer)
