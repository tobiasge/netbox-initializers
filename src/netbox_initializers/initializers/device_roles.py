from dcim.models import DeviceRole
from django.core.exceptions import ObjectDoesNotExist
from netbox.choices import ColorChoices

from netbox_initializers.initializers.base import BaseInitializer, register_initializer


class DeviceRoleInitializer(BaseInitializer):
    data_file_name = "device_roles.yml"

    def load_data(self):
        device_roles = self.load_yaml()
        if device_roles is None:
            return

        for params in device_roles:
            tags = params.pop("tags", None)

            # Resolve parent role (accept slug or name; try slug first, then name)
            if "parent" in params and params["parent"] is not None:
                parent_value = params.pop("parent")

                parent_obj = None
                try:
                    parent_obj = DeviceRole.objects.get(slug=parent_value)
                except ObjectDoesNotExist:
                    try:
                        parent_obj = DeviceRole.objects.get(name=parent_value)
                    except ObjectDoesNotExist:
                        raise ValueError(
                            f"DeviceRole parent '{parent_value}' not found by slug or name"
                        )

                if parent_obj:
                    params["parent"] = parent_obj

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

            self.set_tags(device_role, tags)


register_initializer("device_roles", DeviceRoleInitializer)
