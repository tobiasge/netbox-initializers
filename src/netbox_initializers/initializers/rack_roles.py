from dcim.models import RackRole
from netbox.choices import ColorChoices

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class RackRoleInitializer(BaseModelInitializer):
    data_file_name = "rack_roles.yml"
    model = RackRole
    verbose_name = "rack role"
    emoji = "🎨"

    def prepare_params(self, params: dict[str, object]) -> dict[str, object] | None:
        if "color" in params:
            color = params["color"]

            for color_tpl in ColorChoices:
                if color in color_tpl:
                    params["color"] = color_tpl[0]
                    break

        return params


register_initializer("rack_roles", RackRoleInitializer)
