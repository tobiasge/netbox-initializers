from core.models import ObjectType
from users.models import Group, ObjectPermission, User

from netbox_initializers.initializers.base import BaseInitializer, register_initializer


class ObjectPermissionInitializer(BaseInitializer):
    data_file_name = "object_permissions.yml"

    def load_data(self):
        object_permissions = self.load_yaml()
        if object_permissions is None:
            return
        for permission_name, permission_details in object_permissions.items():
            object_permission, created = ObjectPermission.objects.get_or_create(
                name=permission_name,
                defaults={
                    "description": permission_details["description"],
                    "enabled": permission_details["enabled"],
                    "actions": permission_details["actions"],
                },
            )

            if "constraints" in permission_details:
                object_permission.constraints = permission_details["constraints"]

            if "object_types" in permission_details:
                object_types = permission_details["object_types"]

                if object_types == "all":
                    object_permission.object_types.set(ObjectType.objects.all())

                else:
                    for app_label, models in object_types.items():
                        if models == "all":
                            app_models = ObjectType.objects.filter(app_label=app_label)

                            for app_model in app_models:
                                object_permission.object_types.add(app_model.id)
                        else:
                            for model in models:
                                object_permission.object_types.add(
                                    ObjectType.objects.get(app_label=app_label, model=model)
                                )
            if created:
                self.log(f"🔓 Created object permission {object_permission.name}")

            if "groups" in permission_details:
                for groupname in permission_details["groups"]:
                    group = Group.objects.filter(name=groupname).first()

                    if group:
                        object_permission.groups.add(group)
                        self.log(f" 👥 Assigned group {groupname} object permission of {object_permission.name}")

            if "users" in permission_details:
                for username in permission_details["users"]:
                    user = User.objects.filter(username=username).first()

                    if user:
                        object_permission.users.add(user)
                        self.log(f" 👤 Assigned user {username} object permission of {object_permission.name}")

            object_permission.save()


register_initializer("object_permissions", ObjectPermissionInitializer)
