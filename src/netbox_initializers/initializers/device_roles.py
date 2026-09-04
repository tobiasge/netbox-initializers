from dcim.models import DeviceRole
from django.core.exceptions import ObjectDoesNotExist
from netbox.choices import ColorChoices

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class DeviceRoleInitializer(BaseModelInitializer):
    data_file_name = "device_roles.yml"
    model = DeviceRole
    verbose_name = "device role"
    emoji = "🎨"

    def prepare_params(self, params: dict[str, object]) -> dict[str, object] | None:
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
                    raise ValueError(f"DeviceRole parent '{parent_value}' not found by slug or name")

            if parent_obj:
                params["parent"] = parent_obj

        if "color" in params:
            color = params["color"]

            for color_tpl in ColorChoices:
                if color in color_tpl:
                    params["color"] = color_tpl[0]
                    break

        return params


register_initializer("device_roles", DeviceRoleInitializer)
