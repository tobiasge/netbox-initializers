from collections.abc import Mapping
from typing import ClassVar

from tenancy.models import Tenant, TenantGroup

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class TenantInitializer(BaseModelInitializer):
    data_file_name = "tenants.yml"
    model = Tenant
    verbose_name = "Tenant"
    emoji = "👩‍💻"
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"group": (TenantGroup, "name")}


register_initializer("tenants", TenantInitializer)
