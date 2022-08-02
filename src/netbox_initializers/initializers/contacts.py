from tenancy.models import Contact, ContactGroup

from . import BaseInitializer, register_initializer

OPTIONAL_ASSOCS = {"group": (ContactGroup, "name")}


class ContactInitializer(BaseInitializer):
    data_file_name = "contacts.yml"

    def load_data(self):
        contacts = self.load_yaml()
        if contacts is None:
            return
        for params in contacts:
            custom_field_data = self.pop_custom_fields(params)

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}

                    params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params)
            contact, created = Contact.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("👩‍💻 Created Contact", contact.name)

            self.set_custom_fields_values(contact, custom_field_data)


register_initializer("contacts", ContactInitializer)
