from django.contrib.contenttypes.models import ContentType
from extras.models import CustomLink

from . import BaseInitializer, register_initializer


def get_content_type(content_type):
    try:
        return ContentType.objects.get(model=content_type)
    except ContentType.DoesNotExist:
        pass
    return None


class CustomLinkInitializer(BaseInitializer):
    data_file_name = "custom_links.yml"

    def load_data(self):
        custom_links = self.load_yaml()
        if custom_links is None:
            return
        for link in custom_links:
            content_type_name = link.pop("content_type")
            content_type = get_content_type(content_type_name)
            if content_type is None:
                print(
                    "⚠️ Unable to create Custom Link '{0}': The content_type '{1}' is unknown".format(
                        link.get("name"), content_type
                    )
                )
                continue

            matching_params, defaults = self.split_params(link)
            custom_link, created = CustomLink.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                custom_link.content_types.add(content_type)
                custom_link.save()
                print("🔗 Created Custom Link '{0}'".format(custom_link.name))


register_initializer("custom_links", CustomLinkInitializer)
