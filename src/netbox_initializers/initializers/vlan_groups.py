from django.contrib.contenttypes.models import ContentType
from ipam.models import VLANGroup

from . import BaseInitializer, register_initializer

OPTIONAL_ASSOCS = {"scope": (None, "name")}


class VLANGroupInitializer(BaseInitializer):
    data_file_name = "vlan_groups.yml"

    def load_data(self):
        vlan_groups = self.load_yaml()
        if vlan_groups is None:
            return
        for params in vlan_groups:
            custom_field_data = self.pop_custom_fields(params)

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}
                    # Get model from Contenttype
                    scope_type = params.pop("scope_type", None)
                    if not scope_type:
                        print(
                            f"VLAN Group '{params['name']}': scope_type is missing from VLAN Group"
                        )
                        continue
                    app_label, model = str(scope_type).split(".")
                    ct = ContentType.objects.filter(app_label=app_label, model=model).first()
                    if not ct:
                        print(
                            f"VLAN Group '{params['name']}': ContentType for "
                            + f"app_label = '{app_label}' and model = '{model}' not found"
                        )
                        continue
                    params["scope_id"] = ct.model_class().objects.get(**query).id

            matching_params, defaults = self.split_params(params)
            vlan_group, created = VLANGroup.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                print("🏘️ Created VLAN Group", vlan_group.name)

            self.set_custom_fields_values(vlan_group, custom_field_data)


register_initializer("vlan_groups", VLANGroupInitializer)
