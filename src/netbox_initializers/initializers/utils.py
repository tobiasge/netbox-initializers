from collections.abc import Collection, Mapping

from django.contrib.contenttypes.models import ContentType


def get_scope_details(scope: Mapping[str, object], allowed_termination_types: Collection[str]):
    try:
        scope_type = ContentType.objects.get(app_label__in=["dcim", "circuits"], model=scope["type"])
        if scope["type"] not in allowed_termination_types:
            raise ValueError(f"{scope['type']} scope type is not permitted on {scope_type.app_label}")
    except ContentType.DoesNotExist:
        raise ValueError(f"⚠️ Invalid scope type: {scope['type']}")

    scope_id = scope_type.model_class().objects.get(name=scope["name"]).id
    return scope_type, scope_id
