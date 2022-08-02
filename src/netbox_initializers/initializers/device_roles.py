from dcim.models import DeviceRole
from utilities.choices import ColorChoices

from . import BaseInitializer, register_initializer


class DeviceRoleInitializer(BaseInitializer):
    data_file_name = "device_roles.yml"

    def load_data(self):
        device_roles = self.load_yaml()
        if device_roles is None:
            return
        for params in device_roles:

            if "color" in params:
                color = params.pop("color")

                for color_tpl in ColorChoices:
                    if color in color_tpl:
                        params["color"] = color_tpl[0]

            matching_params, defaults = self.split_params(params)
            device_role, created = DeviceRole.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                print("🎨 Created device role", device_role.name)


register_initializer("device_roles", DeviceRoleInitializer)
