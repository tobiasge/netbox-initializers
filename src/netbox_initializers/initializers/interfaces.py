from dcim.models import Device, Interface

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["device", "name"]
REQUIRED_ASSOCS = {"device": (Device, "name")}
RELATED_ASSOCS = {
    "bridge": (Interface, "name"),
    "lag": (Interface, "name"),
    "parent": (Interface, "name"),
}


class InterfaceInitializer(BaseInitializer):
    data_file_name = "interfaces.yml"

    def load_data(self):
        interfaces = self.load_yaml()
        if interfaces is None:
            return
        for params in interfaces:
            custom_field_data = self.pop_custom_fields(params)

            related_interfaces = {k: params.pop(k, None) for k in RELATED_ASSOCS}

            for assoc, details in REQUIRED_ASSOCS.items():
                model, field = details
                query = {field: params.pop(assoc)}

                params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            interface, created = Interface.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                print(f"🧷 Created interface {interface} on {interface.device}")

            self.set_custom_fields_values(interface, custom_field_data)

            for related_field, related_value in related_interfaces.items():
                if not related_value:
                    continue

                r_model, r_field = RELATED_ASSOCS[related_field]

                if related_field == "parent" and not interface.parent_id:
                    query = {r_field: related_value, "device": interface.device}
                    try:
                        related_obj = r_model.objects.get(**query)
                    except Interface.DoesNotExist:
                        print(
                            f"⚠️ Could not find parent interface with: {query} for interface {interface}"
                        )
                        raise

                    interface.parent_id = related_obj.id
                    interface.save()
                    print(
                        f"🧷 Attached interface {interface} on {interface.device} "
                        f"to parent {related_obj}"
                    )
                else:
                    query = {
                        r_field: related_value,
                        "device": interface.device,
                        "type": related_field,
                    }
                    related_obj, rel_obj_created = r_model.objects.get_or_create(**query)

                    if rel_obj_created:
                        setattr(interface, f"{related_field}_id", related_obj.id)
                        interface.save()
                        print(
                            f"🧷 Created {related_field} interface {interface} on {interface.device}"
                        )


register_initializer("interfaces", InterfaceInitializer)
