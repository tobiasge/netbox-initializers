from django.contrib.contenttypes.models import ContentType
from ipam.models import Service

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class ServiceInitializer(BaseModelInitializer):
    data_file_name = "services.yml"
    model = Service
    verbose_name = "Service"
    emoji = "🧰"
    match_params = ("name", "parent_object_type", "parent_object_id")

    def prepare_params(self, params: dict[str, object]) -> dict[str, object] | None:
        # Get model from Contenttype
        scope_type = params.pop("parent_type", None)
        if not scope_type:
            self.log_warning(f"⚠️ Services '{params['name']}': parent_type is missing from Services")
            return None
        app_label, model = str(scope_type).split(".")
        parent_model = ContentType.objects.get(app_label=app_label, model=model).model_class()
        parent = parent_model.objects.get(name=params.pop("parent_name"))

        params["parent_object_type"] = ContentType.objects.get_for_model(parent)
        params["parent_object_id"] = parent.id
        return params


register_initializer("services", ServiceInitializer)
