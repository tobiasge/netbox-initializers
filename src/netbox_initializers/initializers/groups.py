from users.models import Group, User

from netbox_initializers.initializers.base import BaseInitializer, register_initializer


class GroupInitializer(BaseInitializer):
    data_file_name = "groups.yml"

    def load_data(self):
        groups = self.load_yaml()
        if groups is None:
            return

        for groupname, group_details in groups.items():
            group, created = Group.objects.get_or_create(name=groupname)
            if created:
                self.log(f"👥 Created group {groupname}")
            for username in group_details.get("users", []):
                user = User.objects.filter(username=username).first()
                if user:
                    group.users.add(user)
                    self.log(f" 👤 Assigned user {username} to group {group.name}")
                else:
                    self.log_warning(f"⚠️ User '{username}' not found for group '{group.name}'")


register_initializer("groups", GroupInitializer)
