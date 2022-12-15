from circuits.models import Provider
from ipam.models import ASN

from . import BaseInitializer, register_initializer


class ProviderInitializer(BaseInitializer):
    data_file_name = "providers.yml"

    def load_data(self):
        providers = self.load_yaml()
        if providers is None:
            return
        for params in providers:
            custom_field_data = self.pop_custom_fields(params)

            asn_number = params.pop("asn")
            asn = ASN.objects.filter(asn=asn_number).first()
            if asn is None:
                print(
                    "⚠️ Unable to create Provider '{0}': The ASN '{1}' is unknown".format(
                        params.get("name"), asn_number
                    )
                )
                continue

            matching_params, defaults = self.split_params(params)
            provider, created = Provider.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                provider.asns.add(asn)
                provider.save()
                print("📡 Created provider", provider.name)

            self.set_custom_fields_values(provider, custom_field_data)


register_initializer("providers", ProviderInitializer)
