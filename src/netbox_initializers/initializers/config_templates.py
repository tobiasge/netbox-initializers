from extras.models import ConfigTemplate

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class ConfigTemplateInitializer(BaseModelInitializer):
    data_file_name = "config_templates.yml"
    model = ConfigTemplate
    verbose_name = "Config Template"
    emoji = "📄"
    match_params = ("name",)


register_initializer("config_templates", ConfigTemplateInitializer)
