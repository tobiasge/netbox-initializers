from circuits.models import Provider
from ipam.models import ASN

from netbox_initializers.initializers.base import BaseModelInitializer, Writer, register_initializer


class ProviderInitializer(BaseModelInitializer):
    data_file_name = "providers.yml"
    model = Provider
    verbose_name = "provider"
    emoji = "📡"

    def __init__(
        self,
        data_file_path: str,
        stdout: Writer | None = None,
        stderr: Writer | None = None,
        verbosity: int = 1,
    ) -> None:
        super().__init__(data_file_path, stdout=stdout, stderr=stderr, verbosity=verbosity)
        self._asn: ASN | None = None

    def prepare_params(self, params: dict[str, object]) -> dict[str, object] | None:
        asn_number = params.pop("asn", None)
        self._asn = None
        if asn_number is not None:
            self._asn = ASN.objects.filter(asn=asn_number).first()
            if self._asn is None:
                self.log_warning(
                    f"⚠️ Unable to create Provider '{params.get('name')}': The ASN '{asn_number}' is unknown"
                )
                return None
        return params

    def post_create(self, entity, params: dict[str, object], created: bool) -> None:
        if created and self._asn is not None:
            entity.asns.add(self._asn)


register_initializer("providers", ProviderInitializer)
