from core.models import ObjectType
from extras.models import Tag
from netbox.choices import ColorChoices

from netbox_initializers.initializers.base import BaseModelInitializer, Writer, register_initializer


class TagInitializer(BaseModelInitializer):
    data_file_name = "tags.yml"
    model = Tag
    verbose_name = "Tag"
    emoji = "🎨"

    def __init__(
        self,
        data_file_path: str,
        stdout: Writer | None = None,
        stderr: Writer | None = None,
        verbosity: int = 1,
    ) -> None:
        super().__init__(data_file_path, stdout=stdout, stderr=stderr, verbosity=verbosity)
        self._object_types: list[dict[str, str]] | None = None

    def prepare_params(self, params: dict[str, object]) -> dict[str, object] | None:
        if "color" in params:
            color = params["color"]

            for color_tpl in ColorChoices:
                if color in color_tpl:
                    params["color"] = color_tpl[0]
                    break

        object_types = params.pop("object_types", None)
        self._object_types = object_types if isinstance(object_types, list) else None
        return params

    def post_create(self, entity, params: dict[str, object], created: bool) -> None:
        if created and self._object_types:
            for ot in self._object_types:
                ct = ObjectType.objects.get(
                    app_label=ot["app"],
                    model=ot["model"],
                )
                entity.object_types.add(ct)
                self.log(f"🎨 Restricted Tag {entity.name} to {ot['app']}.{ot['model']}")


register_initializer("tags", TagInitializer)
