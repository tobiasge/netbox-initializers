from core.models import ObjectType
from extras.models import CustomLink

from . import BaseInitializer, register_initializer


def get_content_type(content_type):
    try:
        return ObjectType.objects.get(model=content_type)
    except ObjectType.DoesNotExist:
        print(f"⚠️ The content_type '{content_type}' is unknown")
    return None


class CustomLinkInitializer(BaseInitializer):
    data_file_name = "custom_links.yml"

    def load_data(self):
        custom_links = self.load_yaml()
        if custom_links is None:
            return
        for link in custom_links:
            content_types = [get_content_type(x) for x in link.pop("content_type")]

            if None in content_types:
                print(
                    f"⚠️ Unable to create Custom Link '{ link.get('name') }' due to unknown content_type"
                )
                continue

            matching_params, defaults = self.split_params(link)
            custom_link, created = CustomLink.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                custom_link.object_types.set(content_types)
                custom_link.save()
                print(f"🔗 Created Custom Link '{custom_link.name}'")


register_initializer("custom_links", CustomLinkInitializer)
