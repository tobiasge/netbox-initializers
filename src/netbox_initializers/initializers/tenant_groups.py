from tenancy.models import TenantGroup

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class TenantGroupInitializer(BaseModelInitializer):
    data_file_name = "tenant_groups.yml"
    model = TenantGroup
    verbose_name = "Tenant Group"
    emoji = "🔳"


register_initializer("tenant_groups", TenantGroupInitializer)
