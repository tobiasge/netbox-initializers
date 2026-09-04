from collections.abc import Mapping
from typing import ClassVar

from ipam.models import ASN, RIR
from tenancy.models import Tenant

from netbox_initializers.initializers.base import BaseModelInitializer, register_initializer


class ASNInitializer(BaseModelInitializer):
    data_file_name = "asns.yml"
    model = ASN
    name_field = "asn"
    verbose_name = "ASN"
    emoji = "🔡"
    match_params = ("asn", "rir")
    required_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"rir": (RIR, "name")}
    optional_assocs: ClassVar[Mapping[str, tuple[type, str]]] = {"tenant": (Tenant, "name")}


register_initializer("asns", ASNInitializer)
