from circuits.models import Provider

from . import BaseInitializer, register_initializer


class ProviderInitializer(BaseInitializer):
    data_file_name = "providers.yml"

    def load_data(self):
        providers = self.load_yaml()
        if providers is None:
            return
        for params in providers:
            custom_field_data = self.pop_custom_fields(params)

            matching_params, defaults = self.split_params(params)
            provider, created = Provider.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("📡 Created provider", provider.name)

            self.set_custom_fields_values(provider, custom_field_data)


register_initializer("providers", ProviderInitializer)
