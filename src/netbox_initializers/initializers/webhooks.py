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
            obj_types = hook.pop("object_types")

            try:
                obj_type_ids = [get_content_type_id(hook["name"], obj) for obj in obj_types]
            except ContentType.DoesNotExist:
                continue

            matching_params, defaults = self.split_params(hook)
            webhook, created = Webhook.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                webhook.content_types.set(obj_type_ids)
                webhook.save()

                print("🪝 Created Webhook {0}".format(webhook.name))


register_initializer("webhooks", WebhookInitializer)
