from ipam.models import RIR

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class RIRInitializer(BaseModelInitializer):
    data_file_name = "rirs.yml"
    model = RIR
    verbose_name = "RIR"
    emoji = "🗺️"


register_initializer("rirs", RIRInitializer)
