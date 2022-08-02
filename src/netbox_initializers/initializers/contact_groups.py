from tenancy.models import ContactGroup

from . import BaseInitializer, register_initializer

OPTIONAL_ASSOCS = {"parent": (ContactGroup, "name")}


class ContactGroupInitializer(BaseInitializer):
    data_file_name = "contact_groups.yml"

    def load_data(self):
        contact_groups = self.load_yaml()
        if contact_groups is None:
            return
        for params in contact_groups:
            custom_field_data = self.pop_custom_fields(params)

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}

                    params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params)
            contact_group, created = ContactGroup.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                print("🔳 Created Contact Group", contact_group.name)

            self.set_custom_fields_values(contact_group, custom_field_data)


register_initializer("contact_groups", ContactGroupInitializer)
