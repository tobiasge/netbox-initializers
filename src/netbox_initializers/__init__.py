from netbox.plugins import PluginConfig


class NetBoxInitializersConfig(PluginConfig):
    name = "netbox_initializers"
    verbose_name = "NetBox Initializers"
    description = "Load initial data into Netbox"
    version = "4.0.0"
    base_url = "initializers"
    min_version = "4.0-beta1"
    max_version = "4.1.99"


config = NetBoxInitializersConfig
