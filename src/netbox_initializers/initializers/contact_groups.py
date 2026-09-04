from collections.abc import Mapping
from typing import ClassVar

from tenancy.models import ContactGroup

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class ContactGroupInitializer(BaseModelInitializer):
    data_file_name = "contact_groups.yml"
    model = ContactGroup
    verbose_name = "Contact Group"
    emoji = "🔳"
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"parent": (ContactGroup, "name")}


register_initializer("contact_groups", ContactGroupInitializer)
