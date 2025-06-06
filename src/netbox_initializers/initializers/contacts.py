from tenancy.models import Contact, ContactGroup

from netbox_initializers.initializers.base import BaseInitializer, register_initializer

class ContactInitializer(BaseInitializer):
    data_file_name = "contacts.yml"

    def load_data(self):
        contacts = self.load_yaml()
        if contacts is None:
            return
        for params in contacts:
            custom_field_data = self.pop_custom_fields(params)
            tags = params.pop("tags", None)
            
            # Group foreign key on the Contact model is a many-to-many groups field
            groups = params.pop("groups", None)  # Extract the groups from params if they exist
            group_objects = []
            if groups:
                for group_name in groups:  # Iterate through the group names
                    try:
                        group_objects.append(ContactGroup.objects.get(name=group_name))
                    except ContactGroup.DoesNotExist:
                        raise ValueError(f"ContactGroup with name '{group_name}' does not exist.")

            matching_params, defaults = self.split_params(params)
            contact, created = Contact.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("👩‍💻 Created Contact", contact.name)

            # Add the groups to the contact if any were found
            if group_objects:
                contact.groups.set(group_objects)

            self.set_custom_fields_values(contact, custom_field_data)
            self.set_tags(contact, tags)


register_initializer("contacts", ContactInitializer)
