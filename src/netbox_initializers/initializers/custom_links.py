from core.models import ObjectType
from django.core.exceptions import ObjectDoesNotExist
from extras.models import CustomLink

from netbox_initializers.initializers.base import BaseModelInitializer, Writer, register_initializer


def get_content_type(content_type: str) -> ObjectType | None:
    try:
        return ObjectType.objects.get(model=content_type)
    except ObjectDoesNotExist:
        pass
    return None


class CustomLinkInitializer(BaseModelInitializer):
    data_file_name = "custom_links.yml"
    model = CustomLink
    verbose_name = "Custom Link"
    emoji = "🔗"

    def __init__(
        self,
        data_file_path: str,
        stdout: Writer | None = None,
        stderr: Writer | None = None,
        verbosity: int = 1,
    ) -> None:
        super().__init__(data_file_path, stdout=stdout, stderr=stderr, verbosity=verbosity)
        self._content_type: ObjectType | None = None

    def print_created(self, entity) -> None:
        self.log(f"🔗 Created Custom Link '{entity.name}'")

    def prepare_params(self, params: dict[str, object]) -> dict[str, object] | None:
        content_type_name = params.pop("content_type")
        self._content_type = get_content_type(content_type_name)
        if self._content_type is None:
            self.log_warning(
                f"⚠️ Unable to create Custom Link '{params.get('name')}': "
                f"The content_type '{content_type_name}' is unknown"
            )
            return None
        return params

    def post_create(self, entity, params: dict[str, object], created: bool) -> None:
        if created and self._content_type:
            entity.object_types.add(self._content_type)


register_initializer("custom_links", CustomLinkInitializer)
