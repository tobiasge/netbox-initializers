from ipam.models import ServiceTemplate

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class ServiceTemplateInitializer(BaseModelInitializer):
    data_file_name = "service_templates.yml"
    model = ServiceTemplate
    verbose_name = "Service Template"
    emoji = "🧰"
    match_params = ("name",)


register_initializer("service_templates", ServiceTemplateInitializer)
