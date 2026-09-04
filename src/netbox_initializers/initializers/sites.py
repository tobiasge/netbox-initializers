from collections.abc import Mapping
from typing import ClassVar

from dcim.models import Region, Site, SiteGroup
from ipam.models import ASN
from tenancy.models import Tenant

from netbox_initializers.initializers.base import BaseModelInitializer, Writer, register_initializer


class SiteInitializer(BaseModelInitializer):
    data_file_name = "sites.yml"
    model = Site
    verbose_name = "site"
    emoji = "📍"
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {
        "region": (Region, "name"),
        "group": (SiteGroup, "name"),
        "tenant": (Tenant, "name"),
    }

    def __init__(
        self,
        data_file_path: str,
        stdout: Writer | None = None,
        stderr: Writer | None = None,
        verbosity: int = 1,
    ) -> None:
        super().__init__(data_file_path, stdout=stdout, stderr=stderr, verbosity=verbosity)
        self._asns_found: list[ASN] = []

    def prepare_params(self, params: dict[str, object]) -> dict[str, object] | None:
        site_name = params.get("name")
        self._asns_found = []
        asns = params.get("asns")
        if isinstance(asns, list):
            for asn in asns:
                found = ASN.objects.filter(asn=asn).first()
                if found:
                    self._asns_found.append(found)

            if len(asns) != len(self._asns_found):
                self.log_warning(f"⚠️ Unable to create Site '{site_name}': all ASNs could not be found")
                return None

            del params["asns"]
        return params

    def post_create(self, entity, params: dict[str, object], created: bool) -> None:
        if self._asns_found:
            for asn in self._asns_found:
                entity.asns.add(asn)
                self.log(f" 🔢 Assigned ASN {asn} to site {entity.name}")
            entity.save()


register_initializer("sites", SiteInitializer)
