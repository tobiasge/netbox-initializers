from extras.plugins import PluginConfig


class NetBoxInitializersConfig(PluginConfig):
    name = "netbox_initializers"
    verbose_name = "NetBox Initializers"
    description = "Load initial data into Netbox"
    version = "3.5.1"
    base_url = "initializers"
    min_version = "3.5.0"
    max_version = "3.5.99"


config = NetBoxInitializersConfig
