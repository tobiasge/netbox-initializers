from django.contrib.contenttypes.models import ContentType
from ipam.models import VLANGroup

from netbox_initializers.initializers.base import BaseInitializer, register_initializer


class VLANGroupInitializer(BaseInitializer):
    data_file_name = "vlan_groups.yml"

    def load_data(self):
        vlan_groups = self.load_yaml()
        if vlan_groups is None:
            return
        for params in vlan_groups:
            custom_field_data = self.pop_custom_fields(params)
            tags = params.pop("tags", None)

            if "scope" in params:
                query = {"name": params.pop("scope")}
                scope_type = params.pop("scope_type", None)
                if not scope_type:
                    self.log_warning(f"⚠️ VLAN Group '{params.get('name')}': scope_type is missing from VLAN Group")
                    continue
                try:
                    app_label, model = str(scope_type).split(".")
                except ValueError:
                    self.log_warning(f"⚠️ VLAN Group '{params.get('name')}': invalid scope_type '{scope_type}'")
                    continue
                ct = ContentType.objects.filter(app_label=app_label, model=model).first()
                if not ct:
                    self.log_warning(
                        f"⚠️ VLAN Group '{params.get('name')}': ContentType for "
                        f"app_label = '{app_label}' and model = '{model}' not found"
                    )
                    continue
                try:
                    params["scope_id"] = ct.model_class().objects.get(**query).id
                except ct.model_class().DoesNotExist:
                    self.log_warning(f"⚠️ VLAN Group '{params.get('name')}': scope object '{query['name']}' not found")
                    continue
                params["scope_type"] = ct

            matching_params, defaults = self.split_params(params)
            vlan_group, created = VLANGroup.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                self.log(f"🏘️ Created VLAN Group {vlan_group.name}")

            self.set_custom_fields_values(vlan_group, custom_field_data)
            self.set_tags(vlan_group, tags)


register_initializer("vlan_groups", VLANGroupInitializer)
