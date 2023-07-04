from dcim.models import Region, Site
from ipam.models import ASN
from tenancy.models import Tenant

from . import BaseInitializer, register_initializer

OPTIONAL_ASSOCS = {"region": (Region, "name"), "tenant": (Tenant, "name")}


class SiteInitializer(BaseInitializer):
    data_file_name = "sites.yml"

    def load_data(self):
        sites = self.load_yaml()
        if sites is None:
            return
        for params in sites:
            custom_field_data = self.pop_custom_fields(params)

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}

                    params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params)

            asnFounds = []
            if defaults.get("asns", 0):
                for asn in defaults["asns"]:
                    found = ASN.objects.filter(asn=asn).first()
                    if found:
                        asnFounds += [found]

                if len(defaults["asns"]) != len(asnFounds):
                    print(
                        "⚠️ Unable to create Site '{0}': all ASNs could not be found".format(
                            params.get("name")
                        )
                    )

                # asns will be assosciated below
                del defaults["asns"]

            site, created = Site.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("📍 Created site", site.name)

            self.set_custom_fields_values(site, custom_field_data)

            for asn in asnFounds:
                site.asns.add(asn)
                print(" 👤 Assigned asn %s to site %s" % (asn, site.name))

            site.save()


register_initializer("sites", SiteInitializer)
