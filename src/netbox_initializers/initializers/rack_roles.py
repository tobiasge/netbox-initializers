from dcim.models import RackRole
from utilities.choices import ColorChoices

from . import BaseInitializer, register_initializer


class RackRoleInitializer(BaseInitializer):
    data_file_name = "rack_roles.yml"

    def load_data(self):
        rack_roles = self.load_yaml()
        if rack_roles is None:
            return
        for params in rack_roles:
            if "color" in params:
                color = params.pop("color")

                for color_tpl in ColorChoices:
                    if color in color_tpl:
                        params["color"] = color_tpl[0]

            matching_params, defaults = self.split_params(params)
            rack_role, created = RackRole.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                print("🎨 Created rack role", rack_role.name)


register_initializer("rack_roles", RackRoleInitializer)
