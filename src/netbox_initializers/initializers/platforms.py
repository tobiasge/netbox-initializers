from dcim.models import Manufacturer, Platform
from extras.models import ConfigTemplate

from . import BaseInitializer, register_initializer

OPTIONAL_ASSOCS = {
    "manufacturer": (Manufacturer, "name"),
    "config_template": (ConfigTemplate, "name"),
}


class PlatformInitializer(BaseInitializer):
    data_file_name = "platforms.yml"

    def load_data(self):
        platforms = self.load_yaml()
        if platforms is None:
            return
        for params in platforms:
            tags = params.pop("tags", None)

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}

                    params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params)
            platform, created = Platform.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("💾 Created platform", platform.name)

            self.set_tags(platform, tags)


register_initializer("platforms", PlatformInitializer)
