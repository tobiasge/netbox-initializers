from pathlib import Path
from typing import Tuple

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from extras.models import CustomField
from ruamel.yaml import YAML

INITIALIZER_ORDER = (
    "users",
    "groups",
    "object_permissions",
    "custom_fields",
    "custom_links",
    "tags",
    "webhooks",
    "tenant_groups",
    "tenants",
    "regions",
    "sites",
    "locations",
    "rack_roles",
    "racks",
    "power_panels",
    "power_feeds",
    "manufacturers",
    "device_roles",
    "device_types",
    "devices",
    "dcim_interfaces",
    "platforms",
    "route_targets",
    "vrfs",
    "rirs",
    "asns",
    "aggregates",
    "prefix_vlan_roles",
    "cluster_types",
    "cluster_groups",
    "clusters",
    "vlan_groups",
    "vlans",
    "virtual_machines",
    "virtualization_interfaces",
    "prefixes",
    "ip_addresses",
    "primary_ips",
    "services",
    "providers",
    "circuit_types",
    "circuits",
    "cables",
    "contact_groups",
    "contact_roles",
    "contacts",
)

INITIALIZER_REGISTRY = dict()


class BaseInitializer:
    # File name for import; Musst be set in subclass
    data_file_name = None

    def __init__(self, data_file_path: str) -> None:
        self.data_file_path = data_file_path

    def load_data(self):
        # Must be implemented by specific subclass
        pass

    def load_yaml(self):
        yf = Path(f"{self.data_file_path}/{self.data_file_name}")
        if not yf.is_file():
            return None
        with yf.open("r") as stream:
            yaml = YAML(typ="safe")
            return yaml.load(stream)

    def pop_custom_fields(params):
        if "custom_field_data" in params:
            return params.pop("custom_field_data")
        elif "custom_fields" in params:
            print("⚠️ Please rename 'custom_fields' to 'custom_field_data'!")
            return params.pop("custom_fields")

        return None

    def set_custom_fields_values(entity, custom_field_data):
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
                ct = ContentType.objects.get_for_model(entity)
                if ct not in cf.content_types.all():
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

    def split_params(self, params: dict, unique_params: list = None) -> Tuple[dict, dict]:
        """Split params dict into dict with matching params and a dict with default values"""

        if unique_params is None:
            unique_params = ["name", "slug"]

        matching_params = {}
        for unique_param in unique_params:
            param = params.pop(unique_param, None)
            if param:
                matching_params[unique_param] = param
        return matching_params, params


def register_initializer(name: str, initializer: BaseInitializer):
    INITIALIZER_REGISTRY[name] = initializer


# All initializers must be imported here, to be registered
from .asns import ASNInitializer
from .cluster_types import ClusterTypesInitializer
from .groups import GroupInitializer
from .rirs import RIRInitializer
from .services import ServiceInitializer
from .users import UserInitializer
