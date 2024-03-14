from dcim.models import SiteGroup

from . import BaseInitializer, register_initializer

OPTIONAL_ASSOCS = {"parent": (SiteGroup, "name")}


class SiteGroupInitializer(BaseInitializer):
    data_file_name = "site_groups.yml"

    def load_data(self):
        site_groups = self.load_yaml()
        if site_groups is None:
            return
        for params in site_groups:
            tags = params.pop("tags", None)

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}

                    params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params)
            site_group, created = SiteGroup.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                print("🌐 Created Site Group", site_group.name)

            self.set_tags(site_group, tags)


register_initializer("site_groups", SiteGroupInitializer)
