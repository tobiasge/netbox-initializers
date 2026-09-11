from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import ClassVar, Protocol, TypeVar

from core.models import ObjectType
from dcim.models import MACAddress
from django.core.exceptions import ObjectDoesNotExist
from extras.models import CustomField, Tag
from ruamel.yaml import YAML

_T = TypeVar("_T")


class Writer(Protocol):
    def write(self, s: str, /) -> object: ...


_Writer = Writer


class InitializationError(Exception):
    pass


class BaseInitializer:
    # File name for import; Must be set in subclass
    data_file_name = ""

    def __init__(
        self,
        data_file_path: str,
        stdout: _Writer | None = None,
        stderr: _Writer | None = None,
        verbosity: int = 1,
    ) -> None:
        self.data_file_path = data_file_path
        self.stdout = stdout
        self.stderr = stderr
        self.verbosity = verbosity

    def log(self, message: str, level: int = 1) -> None:
        """Write message if verbosity >= level."""
        if self.verbosity >= level:
            if self.stdout and hasattr(self.stdout, "write"):
                self.stdout.write(message)
            else:
                print(message)

    def log_warning(self, message: str) -> None:
        """Write warning message if verbosity >= 1."""
        if self.verbosity >= 1:
            if self.stderr and hasattr(self.stderr, "write"):
                self.stderr.write(message)
            elif self.stdout and hasattr(self.stdout, "write"):
                self.stdout.write(message)
            else:
                print(message)

    def log_debug(self, message: str) -> None:
        """Write debug message if verbosity >= 2."""
        self.log(message, level=2)

    def load_data(self):
        # Must be implemented by specific subclass
        pass

    def load_yaml(self, data_file_name=None):
        yf = Path(self.data_file_path) / (data_file_name or self.data_file_name)
        if not yf.is_file():
            return None
        with yf.open("r") as stream:
            yaml = YAML(typ="safe")
            return yaml.load(stream)

    def pop_custom_fields(self, params):
        if "custom_field_data" in params:
            return params.pop("custom_field_data")
        elif "custom_fields" in params:
            self.log_warning("⚠️ Please rename 'custom_fields' to 'custom_field_data'!")
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
                if not cf.object_types.filter(pk=ct.pk).exists():
                    self.log_warning(
                        f"⚠️ Custom field {key} is not enabled for {entity}'s model! "
                        "Please check the 'on_objects' for that custom field in custom_fields.yml"
                    )
                elif key not in entity.custom_field_data:
                    entity.custom_field_data[key] = value
                    save = True

        if missing_cfs:
            raise InitializationError(
                f"⚠️ Custom field(s) '{missing_cfs}' requested for {entity} but not found in Netbox! "
                "Please check the custom_fields.yml"
            )

        if save:
            entity.save()

    def set_tags(self, entity, tags):
        if not tags:
            return

        if not hasattr(entity, "tags"):
            raise InitializationError(f"⚠️ Tags cannot be applied to {entity}'s model")

        ct = ObjectType.objects.get_for_model(entity)

        save = False
        for tag in Tag.objects.filter(name__in=tags):
            restricted_cts = tag.object_types.all()
            if restricted_cts and ct not in restricted_cts:
                raise InitializationError(f"⚠️ Tag {tag} cannot be applied to {entity}'s model")

            entity.tags.add(tag)
            save = True

        if save:
            entity.save()

    def set_mac_addresses(self, entity, mac_addresses):
        if not mac_addresses:
            return

        if not hasattr(entity, "mac_addresses"):
            raise InitializationError(f"⚠️ MAC Address cannot be applied to {entity}'s model")

        save = False

        for mac in mac_addresses:
            mac_address = MACAddress.objects.create(mac_address=mac, description=f"{entity} MAC Address")
            entity.mac_addresses.add(mac_address)
            save = True

        if save:
            entity.save()

    def split_params(
        self, params: dict[str, _T], unique_params: Sequence[str] | None = None
    ) -> tuple[dict[str, _T], dict[str, _T]]:
        """Split params dict into dict with matching params and a dict with default values"""

        if unique_params is None:
            unique_params = ["name", "slug"]

        matching_params: dict[str, _T] = {}
        for unique_param in unique_params:
            if unique_param in params:
                matching_params[unique_param] = params.pop(unique_param)
        return matching_params, params


class BaseModelInitializer(BaseInitializer):
    """Declarative base initializer for standard NetBox models.

    Subclasses specify model, match_params, required_assocs, optional_assocs,
    and can optionally override prepare_params(), post_create(), or print_created().
    """

    model: type | None = None
    name_field: str = "name"
    match_params: Sequence[str] | None = None
    required_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {}
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {}
    emoji: str = "✨"
    verbose_name: str | None = None

    def get_verbose_name(self) -> str:
        if self.verbose_name:
            return self.verbose_name
        if self.model and hasattr(self.model, "_meta"):
            return self.model._meta.verbose_name.title()
        return "Object"

    def print_created(self, entity) -> None:
        display_name = getattr(entity, self.name_field, str(entity))
        self.log(f"{self.emoji} Created {self.get_verbose_name()} {display_name}")

    def prepare_params(self, params: dict[str, object]) -> dict[str, object] | None:
        """Hook to validate or modify params before assoc resolution and creation.

        Return None to skip this item.
        """
        return params

    def post_create(self, entity, params: dict[str, object], created: bool) -> None:
        """Hook called after entity is created/retrieved, tags and custom fields applied."""

    def load_data(self):
        if self.model is None:
            raise NotImplementedError(f"{self.__class__.__name__} must define 'model'")

        items = self.load_yaml()
        if items is None:
            return

        for item in items:
            params = self.prepare_params(item)
            if params is None:
                continue

            custom_field_data = self.pop_custom_fields(params)
            tags = params.pop("tags", None)
            mac_addresses = params.pop("mac_addresses", None)

            if self.required_assocs:
                for assoc, details in self.required_assocs.items():
                    model, field = details
                    query = {field: params.pop(assoc)}
                    params[assoc] = model.objects.get(**query)

            if self.optional_assocs:
                for assoc, details in self.optional_assocs.items():
                    if assoc in params:
                        model, field = details
                        query = {field: params.pop(assoc)}
                        params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params, self.match_params)
            entity, created = self.model.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                self.print_created(entity)

            self.set_custom_fields_values(entity, custom_field_data)
            self.set_tags(entity, tags)
            self.set_mac_addresses(entity, mac_addresses)
            self.post_create(entity, params, created)


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
    "macs",
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


INITIALIZER_REGISTRY = {}


def register_initializer(name: str, initializer):
    INITIALIZER_REGISTRY[name] = initializer
