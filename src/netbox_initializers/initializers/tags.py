from core.models import ObjectType
from extras.models import Tag
from netbox.choices import ColorChoices

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

            object_types = params.pop("object_types", None)
            matching_params, defaults = self.split_params(params)
            tag, created = Tag.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("🎨 Created Tag", tag.name)

                if object_types:
                    for ot in object_types:
                        ct = ObjectType.objects.get(
                            app_label=ot["app"],
                            model=ot["model"],
                        )
                        tag.object_types.add(ct)
                        print(f"🎨 Restricted Tag {tag.name} to {ot['app']}.{ot['model']}")


register_initializer("tags", TagInitializer)
