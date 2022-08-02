from dcim.models import PowerFeed, PowerPanel, Rack

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["name", "power_panel"]
OPTIONAL_ASSOCS = {"rack": (Rack, "name")}
REQUIRED_ASSOCS = {"power_panel": (PowerPanel, "name")}


class PowerFeedInitializer(BaseInitializer):
    data_file_name = "power_feeds.yml"

    def load_data(self):
        power_feeds = self.load_yaml()
        if power_feeds is None:
            return
        for params in power_feeds:
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
            power_feed, created = PowerFeed.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                print("⚡ Created Power Feed", power_feed.name)

            self.set_custom_fields_values(power_feed, custom_field_data)


register_initializer("power_feeds", PowerFeedInitializer)
