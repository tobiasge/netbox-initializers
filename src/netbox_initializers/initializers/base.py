from pathlib import Path
from typing import Tuple

from core.models import ObjectType
from django.core.exceptions import ObjectDoesNotExist
from extras.models import CustomField, Tag
from ruamel.yaml import YAML


class BaseInitializer:
    # File name for import; Musst be set in subclass
    data_file_name = ""

    def __init__(self, data_file_path: str) -> None:
        self.data_file_path = data_file_path

    def load_data(self):
        # Must be implemented by specific subclass
        pass

    def load_yaml(self, data_file_name=None):
        if data_file_name:
            yf = Path(f"{self.data_file_path}/{data_file_name}")
        else:
            yf = Path(f"{self.data_file_path}/{self.data_file_name}")
        if not yf.is_file():
            return None
        with yf.open("r") as stream:
            yaml = YAML(typ="safe")
            return yaml.load(stream)

    def pop_custom_fields(self, params):
        if "custom_field_data" in params:
            return params.pop("custom_field_data")
        elif "custom_fields" in params:
            print("⚠️ Please rename 'custom_fields' to 'custom_field_data'!")
            return params.pop("custom_fields")

        return None

    def set_custom_fields_values(self, entity, custom_field_data):
        if not custom_field_data:
            return

        missing_cfs = []
        save = False
        for key, value in custom_field_data.items():
            try:
                cf = CustomField.objects.get(name=key)
            except ObjectDoesNotExist:
                missing_cfs.append(key)
            else:
                ct = ObjectType.objects.get_for_model(entity)
                if ct not in cf.object_types.all():
                    print(
                        f"⚠️ Custom field {key} is not enabled for {entity}'s model!"
                        "Please check the 'on_objects' for that custom field in custom_fields.yml"
                    )
                elif key not in entity.custom_field_data:
                    entity.custom_field_data[key] = value
                    save = True

        if missing_cfs:
            raise Exception(
                f"⚠️ Custom field(s) '{missing_cfs}' requested for {entity} but not found in Netbox!"
                "Please chceck the custom_fields.yml"
            )

        if save:
            entity.save()

    def set_tags(self, entity, tags):
        if not tags:
            return

        if not hasattr(entity, "tags"):
            raise Exception(f"⚠️ Tags cannot be applied to {entity}'s model")

        ct = ObjectType.objects.get_for_model(entity)

        save = False
        for tag in Tag.objects.filter(name__in=tags):
            restricted_cts = tag.object_types.all()
            if restricted_cts and ct not in restricted_cts:
                raise Exception(f"⚠️ Tag {tag} cannot be applied to {entity}'s model")

            entity.tags.add(tag)
            save = True

        if save:
            entity.save()

    def split_params(self, params: dict, unique_params: list = None) -> Tuple[dict, dict]:
        """Split params dict into dict with matching params and a dict with default values"""

        if unique_params is None:
            unique_params = ["name", "slug"]

        matching_params = {}
        for unique_param in unique_params:
            param = params.pop(unique_param, "__not_set__")
            if param != "__not_set__":
                matching_params[unique_param] = param
        return matching_params, params


class InitializationError(Exception):
    pass


INITIALIZER_ORDER = (
    "users",
    "groups",
    "object_permissions",
    "custom_fields",
    "custom_links",
    "tags",
    "config_templates",
    "webhooks",
    "tenant_groups",
    "tenants",
    "site_groups",
    "regions",
    "rirs",
    "asns",
    "sites",
    "locations",
    "manufacturers",
    "rack_roles",
    "rack_types",
    "racks",
    "power_panels",
    "power_feeds",
    "platforms",
    "device_roles",
    "device_types",
    "cluster_types",
    "cluster_groups",
    "clusters",
    "prefix_vlan_roles",
    "vlan_groups",
    "vlans",
    "devices",
    "interfaces",
    "route_targets",
    "vrfs",
    "aggregates",
    "virtual_machines",
    "virtualization_interfaces",
    "prefixes",
    "ip_addresses",
    "primary_ips",
    "services",
    "service_templates",
    "providers",
    "circuit_types",
    "circuits",
    "cables",
    "config_contexts",
    "contact_groups",
    "contact_roles",
    "contacts",
)


INITIALIZER_REGISTRY = dict()


def register_initializer(name: str, initializer):
    INITIALIZER_REGISTRY[name] = initializer
