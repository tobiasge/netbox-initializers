from netbox.plugins import PluginConfig

from netbox_initializers.version import VERSION


class NetBoxInitializersConfig(PluginConfig):
    name = "netbox_initializers"
    verbose_name = "NetBox Initializers"
    description = "Load initial data into Netbox"
    version = VERSION
    base_url = "initializers"
    min_version = "4.4.0"
    max_version = "4.4.99"


config = NetBoxInitializersConfig
