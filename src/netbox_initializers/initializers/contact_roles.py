from tenancy.models import ContactRole

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class ContactRoleInitializer(BaseModelInitializer):
    data_file_name = "contact_roles.yml"
    model = ContactRole
    verbose_name = "Contact Role"
    emoji = "🔳"


register_initializer("contact_roles", ContactRoleInitializer)
