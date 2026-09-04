from extras.models import Webhook

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class WebhookInitializer(BaseModelInitializer):
    data_file_name = "webhooks.yml"
    model = Webhook
    verbose_name = "Webhook"
    emoji = "🪝"


register_initializer("webhooks", WebhookInitializer)
