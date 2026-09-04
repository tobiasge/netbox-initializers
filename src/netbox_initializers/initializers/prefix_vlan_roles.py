from ipam.models import Role

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class RoleInitializer(BaseModelInitializer):
    data_file_name = "prefix_vlan_roles.yml"
    model = Role
    verbose_name = "Prefix/VLAN Role"
    emoji = "⛹️‍"


register_initializer("prefix_vlan_roles", RoleInitializer)
