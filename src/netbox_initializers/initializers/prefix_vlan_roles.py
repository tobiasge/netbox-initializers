from ipam.models import Role

from . import BaseInitializer, register_initializer


class RoleInitializer(BaseInitializer):
    data_file_name = "prefix_vlan_roles.yml"

    def load_data(self):
        roles = self.load_yaml()
        if roles is None:
            return
        for params in roles:
            matching_params, defaults = self.split_params(params)
            role, created = Role.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("⛹️‍ Created Prefix/VLAN Role", role.name)


register_initializer("prefix_vlan_roles", RoleInitializer)
