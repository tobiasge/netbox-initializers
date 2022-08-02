from tenancy.models import Tenant, TenantGroup

from . import BaseInitializer, register_initializer

OPTIONAL_ASSOCS = {"group": (TenantGroup, "name")}


class TenantInitializer(BaseInitializer):
    data_file_name = "tenants.yml"

    def load_data(self):
        tenants = self.load_yaml()
        if tenants is None:
            return
        for params in tenants:
            custom_field_data = self.pop_custom_fields(params)

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}

                    params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params)
            tenant, created = Tenant.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("👩‍💻 Created Tenant", tenant.name)

            self.set_custom_fields_values(tenant, custom_field_data)


register_initializer("tenants", TenantInitializer)
