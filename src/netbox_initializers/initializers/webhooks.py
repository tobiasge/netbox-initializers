from django.contrib.contenttypes.models import ContentType
from extras.models import Webhook

from . import BaseInitializer, register_initializer


def get_content_type_id(hook_name, content_type):
    try:
        return ContentType.objects.get(model=content_type).id
    except ContentType.DoesNotExist as ex:
        print("⚠️ Webhook '{0}': The object_type '{1}' is unknown.".format(hook_name, content_type))
        raise ex


class WebhookInitializer(BaseInitializer):
    data_file_name = "webhooks.yml"

    def load_data(self):
        webhooks = self.load_yaml()
        if webhooks is None:
            return
        for hook in webhooks:
            tags = hook.pop("tags", None)
            matching_params, defaults = self.split_params(hook)
            webhook, created = Webhook.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("🪝 Created Webhook {0}".format(webhook.name))

            self.set_tags(webhook, tags)


register_initializer("webhooks", WebhookInitializer)
