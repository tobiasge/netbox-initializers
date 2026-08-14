"""Verify NetBox initializer data via the REST API.

The script iterates over every initializer YAML file, and for each object it
defines, queries the NetBox REST API to confirm the object was created. The
expected values are read directly from the YAML files, so there are no
hard-coded test values to keep in sync.
"""

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import yaml

BASE_URL = "http://localhost:8080/api"
YAML_DIR = Path("/etc/netbox/initializer-data")

# NetBox v2 API tokens are transmitted as "nbt_<key>.<plaintext>"
TOKEN_PREFIX = "nbt_"

# A single entry in the CHECKS table below.
type Check = dict[str, Any]
type JSON = dict[str, Any]


def load_yaml(name: str) -> Any:
    """Load and parse an initializer YAML file, returning None if absent."""
    path = YAML_DIR / name
    if not path.exists():
        return None
    with open(path) as fh:
        return yaml.safe_load(fh)


def build_token() -> str | None:
    """Assemble the API token for the first superuser defined in users.yml."""
    users = load_yaml("users.yml")
    if not users:
        return None
    for details in users.values():
        if details.get("is_superuser"):
            token_data = details.get("token", {})
            key = token_data.get("key")
            value = token_data.get("value")
            if key and value:
                return f"{TOKEN_PREFIX}{key}.{value}"
    return None


TOKEN = build_token()
if not TOKEN:
    print("❌ Could not find a superuser token in users.yml")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Token {TOKEN}",
    "Accept": "application/json",
}


def api_get(endpoint: str, params: dict[str, Any] | None = None) -> JSON | None:
    """Make a GET request to the NetBox API.

    ``endpoint`` may be a path (e.g. ``/dcim/sites/``) or an absolute URL as
    returned by the API in nested object references.
    """
    url = endpoint if endpoint.startswith("http") else f"{BASE_URL}{endpoint}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code} on GET {url}: {e.reason}")
        return None
    except Exception as e:  # noqa: BLE001
        print(f"❌ Error on GET {url}: {e}")
        return None


def choice_value(choice: Any) -> Any:
    """Return the value of a choice, which may be a [value, label] pair."""
    return choice[0] if isinstance(choice, (list, tuple)) else choice


# Mapping of each initializer YAML file to how its objects can be located via
# the REST API.
#   endpoint: REST API list endpoint
#   structure: "list" (list of objects) or "dict" (objects keyed by identifier)
#   filters:   for "list", the object fields used to build the lookup query
#   key_filter: for "dict", the query field the mapping key maps to
CHECKS: list[Check] = [
    {"file": "aggregates.yml", "endpoint": "/ipam/aggregates/", "structure": "list", "filters": ["prefix"]},
    {"file": "asns.yml", "endpoint": "/ipam/asns/", "structure": "list", "filters": ["asn"]},
    {"file": "circuit_types.yml", "endpoint": "/circuits/circuit-types/", "structure": "list", "filters": ["slug"]},
    {"file": "circuits.yml", "endpoint": "/circuits/circuits/", "structure": "list", "filters": ["cid"]},
    {
        "file": "cluster_groups.yml",
        "endpoint": "/virtualization/cluster-groups/",
        "structure": "list",
        "filters": ["slug"],
    },
    {
        "file": "cluster_types.yml",
        "endpoint": "/virtualization/cluster-types/",
        "structure": "list",
        "filters": ["slug"],
    },
    {"file": "clusters.yml", "endpoint": "/virtualization/clusters/", "structure": "list", "filters": ["name"]},
    {"file": "config_contexts.yml", "endpoint": "/extras/config-contexts/", "structure": "list", "filters": ["name"]},
    {"file": "config_templates.yml", "endpoint": "/extras/config-templates/", "structure": "list", "filters": ["name"]},
    {"file": "contact_groups.yml", "endpoint": "/tenancy/contact-groups/", "structure": "list", "filters": ["slug"]},
    {"file": "contact_roles.yml", "endpoint": "/tenancy/contact-roles/", "structure": "list", "filters": ["slug"]},
    {"file": "contacts.yml", "endpoint": "/tenancy/contacts/", "structure": "list", "filters": ["name"]},
    {"file": "custom_fields.yml", "endpoint": "/extras/custom-fields/", "structure": "dict", "key_filter": "name"},
    {"file": "custom_links.yml", "endpoint": "/extras/custom-links/", "structure": "list", "filters": ["name"]},
    {"file": "device_roles.yml", "endpoint": "/dcim/device-roles/", "structure": "list", "filters": ["slug"]},
    {"file": "device_types.yml", "endpoint": "/dcim/device-types/", "structure": "list", "filters": ["slug"]},
    {"file": "devices.yml", "endpoint": "/dcim/devices/", "structure": "list", "filters": ["name"]},
    {"file": "groups.yml", "endpoint": "/users/groups/", "structure": "dict", "key_filter": "name"},
    {"file": "interfaces.yml", "endpoint": "/dcim/interfaces/", "structure": "list", "filters": ["device", "name"]},
    {"file": "ip_addresses.yml", "endpoint": "/ipam/ip-addresses/", "structure": "list", "filters": ["address"]},
    {"file": "locations.yml", "endpoint": "/dcim/locations/", "structure": "list", "filters": ["slug"]},
    {"file": "macs.yml", "endpoint": "/dcim/mac-addresses/", "structure": "list", "filters": ["mac_address"]},
    {"file": "manufacturers.yml", "endpoint": "/dcim/manufacturers/", "structure": "list", "filters": ["slug"]},
    {"file": "object_permissions.yml", "endpoint": "/users/permissions/", "structure": "dict", "key_filter": "name"},
    {"file": "platforms.yml", "endpoint": "/dcim/platforms/", "structure": "list", "filters": ["slug"]},
    {"file": "power_feeds.yml", "endpoint": "/dcim/power-feeds/", "structure": "list", "filters": ["name"]},
    {"file": "power_panels.yml", "endpoint": "/dcim/power-panels/", "structure": "list", "filters": ["name"]},
    {"file": "prefix_vlan_roles.yml", "endpoint": "/ipam/roles/", "structure": "list", "filters": ["slug"]},
    {"file": "prefixes.yml", "endpoint": "/ipam/prefixes/", "structure": "list", "filters": ["prefix"]},
    {"file": "providers.yml", "endpoint": "/circuits/providers/", "structure": "list", "filters": ["slug"]},
    {"file": "rack_roles.yml", "endpoint": "/dcim/rack-roles/", "structure": "list", "filters": ["slug"]},
    {"file": "rack_types.yml", "endpoint": "/dcim/rack-types/", "structure": "list", "filters": ["slug"]},
    {"file": "racks.yml", "endpoint": "/dcim/racks/", "structure": "list", "filters": ["name"]},
    {"file": "regions.yml", "endpoint": "/dcim/regions/", "structure": "list", "filters": ["slug"]},
    {"file": "rirs.yml", "endpoint": "/ipam/rirs/", "structure": "list", "filters": ["slug"]},
    {"file": "route_targets.yml", "endpoint": "/ipam/route-targets/", "structure": "list", "filters": ["name"]},
    {"file": "service_templates.yml", "endpoint": "/ipam/service-templates/", "structure": "list", "filters": ["name"]},
    {"file": "services.yml", "endpoint": "/ipam/services/", "structure": "list", "filters": ["name"]},
    {"file": "site_groups.yml", "endpoint": "/dcim/site-groups/", "structure": "list", "filters": ["slug"]},
    {"file": "sites.yml", "endpoint": "/dcim/sites/", "structure": "list", "filters": ["slug"]},
    {"file": "tags.yml", "endpoint": "/extras/tags/", "structure": "list", "filters": ["slug"]},
    {"file": "tenant_groups.yml", "endpoint": "/tenancy/tenant-groups/", "structure": "list", "filters": ["slug"]},
    {"file": "tenants.yml", "endpoint": "/tenancy/tenants/", "structure": "list", "filters": ["slug"]},
    {"file": "users.yml", "endpoint": "/users/users/", "structure": "dict", "key_filter": "username"},
    {
        "file": "virtual_machines.yml",
        "endpoint": "/virtualization/virtual-machines/",
        "structure": "list",
        "filters": ["name"],
    },
    {
        "file": "virtualization_interfaces.yml",
        "endpoint": "/virtualization/interfaces/",
        "structure": "list",
        "filters": ["virtual_machine", "name"],
    },
    {"file": "vlan_groups.yml", "endpoint": "/ipam/vlan-groups/", "structure": "list", "filters": ["slug"]},
    {"file": "vlans.yml", "endpoint": "/ipam/vlans/", "structure": "list", "filters": ["vid"]},
    {"file": "vrfs.yml", "endpoint": "/ipam/vrfs/", "structure": "list", "filters": ["name"]},
    {"file": "webhooks.yml", "endpoint": "/extras/webhooks/", "structure": "list", "filters": ["name"]},
    # Cables have no simple natural key; verify the expected number were created.
    {"file": "cables.yml", "endpoint": "/dcim/cables/", "structure": "count"},
]


class Verifier:
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0

    def ok(self, message: str) -> None:
        self.passed += 1
        print(f"✅ {message}")

    def fail(self, message: str) -> None:
        self.failed += 1
        print(f"❌ {message}")

    def object_exists(self, endpoint: str, filters: dict[str, Any]) -> bool:
        data = api_get(endpoint, filters)
        return bool(data and data.get("results"))

    def verify_custom_field_choices(self, cf: JSON, details: JSON, label: str) -> None:
        """For select/multiselect fields, confirm the choice set matches the YAML."""
        expected = details.get("choice_set")
        if not expected or not cf.get("choice_set"):
            return
        choice_data = api_get(cf["choice_set"]["url"])
        if not choice_data:
            self.fail(f"{label}: choice set could not be retrieved")
            return
        actual = {choice_value(c) for c in choice_data.get("extra_choices", [])}
        wanted = {choice_value(c) for c in expected}
        if actual != wanted:
            self.fail(f"{label}: choices {sorted(actual)} != expected {sorted(wanted)}")
        else:
            self.ok(f"{label}: choice set verified")

    def run_check(self, check: Check) -> None:
        data = load_yaml(check["file"])
        if not data:
            return
        obj = check["file"].removesuffix(".yml")

        match check["structure"]:
            case "count":
                self._check_count(check, obj, data)
            case "dict":
                self._check_dict(check, obj, data)
            case "list":
                self._check_list(check, obj, data)

    def _check_count(self, check: Check, obj: str, data: list) -> None:
        resp = api_get(check["endpoint"], {"limit": 1})
        count = resp.get("count") if resp else None
        if count is not None and count >= len(data):
            self.ok(f"{obj}: {count} object(s) present (>= {len(data)} defined)")
        else:
            self.fail(f"{obj}: expected >= {len(data)} objects, API reports {count}")

    def _check_dict(self, check: Check, obj: str, data: dict) -> None:
        endpoint = check["endpoint"]
        key_filter = check["key_filter"]
        for key, details in data.items():
            label = f"{obj} '{key}'"
            result = api_get(endpoint, {key_filter: key})
            if result and result.get("results"):
                self.ok(f"{label} verified")
                if obj == "custom_fields":
                    self.verify_custom_field_choices(result["results"][0], details, label)
            else:
                self.fail(f"{label} not found")

    def _check_list(self, check: Check, obj: str, data: list) -> None:
        for item in data:
            filters = {f: item[f] for f in check["filters"] if item.get(f) is not None}
            if not filters:
                continue
            label_value = filters.get(check["filters"][-1], next(iter(filters.values())))
            label = f"{obj} '{label_value}'"
            if self.object_exists(check["endpoint"], filters):
                self.ok(f"{label} verified")
            else:
                self.fail(f"{label} not found")

    def run(self) -> int:
        print("🔍 Verifying NetBox initializer data via API")
        print(f"   Base URL: {BASE_URL}")
        print(f"   Loading config from: {YAML_DIR}\n")

        for check in CHECKS:
            self.run_check(check)

        total = self.passed + self.failed
        print(f"\n📊 Verification Results: {self.passed}/{total} checks passed")
        if self.failed == 0:
            print("✨ All verifications passed!")
            return 0
        print(f"⚠️  {self.failed} verification(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(Verifier().run())
