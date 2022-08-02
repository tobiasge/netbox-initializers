from extras.models import Tag
from utilities.choices import ColorChoices

from . import BaseInitializer, register_initializer


class TagInitializer(BaseInitializer):
    data_file_name = "tags.yml"

    def load_data(self):
        tags = self.load_yaml()
        if tags is None:
            return
        for params in tags:
            if "color" in params:
                color = params.pop("color")

                for color_tpl in ColorChoices:
                    if color in color_tpl:
                        params["color"] = color_tpl[0]

            matching_params, defaults = self.split_params(params)
            tag, created = Tag.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("🎨 Created Tag", tag.name)


register_initializer("tags", TagInitializer)
