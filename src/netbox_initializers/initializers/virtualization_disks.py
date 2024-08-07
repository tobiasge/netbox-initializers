from virtualization.models import VirtualDisk, VirtualMachine

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["name", "virtual_machine"]
REQUIRED_ASSOCS = {"virtual_machine": (VirtualMachine, "name")}


class VMDiskInitializer(BaseInitializer):
    data_file_name = "virtualization_disks.yml"

    def load_data(self):
        disks = self.load_yaml()
        if disks is None:
            return
        for params in disks:
            custom_field_data = self.pop_custom_fields(params)
            tags = params.pop("tags", None)

            for assoc, details in REQUIRED_ASSOCS.items():
                model, field = details
                query = {field: params.pop(assoc)}

                params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            disk, created = VirtualDisk.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("💽 Created Disk", disk.name, disk.virtual_machine.name)

            self.set_custom_fields_values(disk, custom_field_data)
            self.set_tags(disk, tags)


register_initializer("virtualization_disks", VMDiskInitializer)
