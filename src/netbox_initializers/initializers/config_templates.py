from django.contrib.contenttypes.models import ContentType
from extras.models import ConfigTemplate

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["name", "description", "template_code", "environment_params"]


def get_content_type_id(hook_name, content_type):
    try:
        return ContentType.objects.get(model=content_type).id
    except ContentType.DoesNotExist as ex:
        print("⚠️ Webhook '{0}': The object_type '{1}' is unknown.".format(hook_name, content_type))
        raise ex


class ConfigTemplateInitializer(BaseInitializer):
    data_file_name = "config_templates.yml"

    def load_data(self):
        config_templates = self.load_yaml()
        if config_templates is None:
            return
        for template in config_templates:
            matching_params, defaults = self.split_params(template)
            config_template, created = ConfigTemplate.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                config_template.save()
                print("🪝 Created Config Template {0}".format(config_template.name))


register_initializer("config_templates", ConfigTemplateInitializer)
