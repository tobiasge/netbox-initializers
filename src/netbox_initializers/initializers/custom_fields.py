from extras.models import CustomField

from . import BaseInitializer, register_initializer


def get_class_for_class_path(class_path):
    import importlib

    from django.contrib.contenttypes.models import ContentType

    module_name, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    clazz = getattr(module, class_name)
    return ContentType.objects.get_for_model(clazz)


class CustomFieldInitializer(BaseInitializer):
    data_file_name = "custom_fields.yml"

    def load_data(self):
        customfields = self.load_yaml()
        if customfields is None:
            return
        for cf_name, cf_details in customfields.items():
            custom_field, created = CustomField.objects.get_or_create(name=cf_name)

            if created:
                if cf_details.get("default", False):
                    custom_field.default = cf_details["default"]

                if cf_details.get("description", False):
                    custom_field.description = cf_details["description"]

                if cf_details.get("label", False):
                    custom_field.label = cf_details["label"]

                for object_type in cf_details.get("on_objects", []):
                    custom_field.content_types.add(get_class_for_class_path(object_type))

                if cf_details.get("required", False):
                    custom_field.required = cf_details["required"]

                if cf_details.get("type", False):
                    custom_field.type = cf_details["type"]

                if cf_details.get("filter_logic", False):
                    custom_field.filter_logic = cf_details["filter_logic"]

                if cf_details.get("weight", -1) >= 0:
                    custom_field.weight = cf_details["weight"]

                # object_type should only be applied when type is object, multiobject
                if cf_details.get("object_type"):
                    if cf_details.get("type") not in (
                        "object",
                        "multiobject",
                    ):
                        print(
                            f"⚠️ Unable to create Custom Field '{cf_name}': object_type is "
                            + "supported only for object and multiobject types"
                        )
                        custom_field.delete()
                        continue
                    custom_field.object_type = get_class_for_class_path(cf_details["object_type"])

                # validation_regex should only be applied when type is text, longtext, url
                if cf_details.get("validation_regex"):
                    if cf_details.get("type") not in (
                        "text",
                        "longtext",
                        "url",
                    ):
                        print(
                            f"⚠️ Unable to create Custom Field '{cf_name}': validation_regex is "
                            + "supported only for text, longtext and, url types"
                        )
                        custom_field.delete()
                        continue
                    custom_field.validation_regex = cf_details["validation_regex"]

                # validation_minimum should only be applied when type is integer
                if cf_details.get("validation_minimum"):
                    if cf_details.get("type") not in ("integer",):
                        print(
                            f"⚠️ Unable to create Custom Field '{cf_name}': validation_minimum is "
                            + "supported only for integer type"
                        )
                        custom_field.delete()
                        continue
                    custom_field.validation_minimum = cf_details["validation_minimum"]

                # validation_maximum should only be applied when type is integer
                if cf_details.get("validation_maximum"):
                    if cf_details.get("type") not in ("integer",):
                        print(
                            f"⚠️ Unable to create Custom Field '{cf_name}': validation_maximum is "
                            + "supported only for integer type"
                        )
                        custom_field.delete()
                        continue
                    custom_field.validation_maximum = cf_details["validation_maximum"]

                # choices should only be applied when type is select, multiselect
                if cf_details.get("choices"):
                    if cf_details.get("type") not in (
                        "select",
                        "multiselect",
                    ):
                        print(
                            f"⚠️ Unable to create Custom Field '{cf_name}': choices is supported only "
                            + "for select and multiselect types"
                        )
                        custom_field.delete()
                        continue
                    custom_field.choices = []

                    for choice_detail in cf_details.get("choices", []):
                        if isinstance(choice_detail, dict) and "value" in choice_detail:
                            # legacy mode
                            print(
                                f"⚠️ Please migrate the choice '{choice_detail['value']}' of '{cf_name}'"
                                + " to the new format, as 'weight' is no longer supported!"
                            )
                            custom_field.choices.append(choice_detail["value"])
                        else:
                            custom_field.choices.append(choice_detail)

                custom_field.save()

                print("🔧 Created custom field", cf_name)


register_initializer("custom_fields", CustomFieldInitializer)
