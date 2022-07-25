from ipam.models import ASN, RIR
from tenancy.models import Tenant

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["asn", "rir"]
REQUIRED_ASSOCS = {"rir": (RIR, "name")}
OPTIONAL_ASSOCS = {"tenant": (Tenant, "name")}


class ASNInitializer(BaseInitializer):
    data_file_name = "asns.yml"

    def load_data(self):
        asns = self.load_yaml()
        if asns is None:
            return
        for params in asns:
            for assoc, details in REQUIRED_ASSOCS.items():
                model, field = details
                query = {field: params.pop(assoc)}

                params[assoc] = model.objects.get(**query)

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}

                    params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            asn, created = ASN.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print(f"🔡 Created ASN {asn.asn}")


register_initializer("asns", ASNInitializer)
