from tenancy.models import Contact, ContactGroup

from netbox_initializers.initializers.base import BaseModelInitializer, Writer, register_initializer


class ContactInitializer(BaseModelInitializer):
    data_file_name = "contacts.yml"
    model = Contact
    verbose_name = "Contact"
    emoji = "👩‍💻"

    def __init__(
        self,
        data_file_path: str,
        stdout: Writer | None = None,
        stderr: Writer | None = None,
        verbosity: int = 1,
    ) -> None:
        super().__init__(data_file_path, stdout=stdout, stderr=stderr, verbosity=verbosity)
        self._group_objects: list[ContactGroup] = []

    def prepare_params(self, params: dict[str, object]) -> dict[str, object] | None:
        groups = params.pop("groups", None)
        self._group_objects = []
        if isinstance(groups, list):
            for group_name in groups:
                try:
                    self._group_objects.append(ContactGroup.objects.get(name=group_name))
                except ContactGroup.DoesNotExist:
                    raise ValueError(f"ContactGroup with name '{group_name}' does not exist.")
        return params

    def post_create(self, entity, params: dict[str, object], created: bool) -> None:
        if self._group_objects:
            entity.groups.set(self._group_objects)


register_initializer("contacts", ContactInitializer)
