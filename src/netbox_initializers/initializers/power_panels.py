from dcim.models import Location, PowerPanel, Site

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["name", "site"]
REQUIRED_ASSOCS = {"site": (Site, "name")}
OPTIONAL_ASSOCS = {"location": (Location, "name")}


class PowerPanelInitializer(BaseInitializer):
    data_file_name = "power_panels.yml"

    def load_data(self):
        power_panels = self.load_yaml()
        if power_panels is None:
            return
        for params in power_panels:
            custom_field_data = self.pop_custom_fields(params)

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
            power_panel, created = PowerPanel.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                print("⚡ Created Power Panel", power_panel.site, power_panel.name)

            self.set_custom_fields_values(power_panel, custom_field_data)


register_initializer("power_panels", PowerPanelInitializer)
