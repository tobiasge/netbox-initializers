from users.models import NetBoxGroup, NetBoxUser

from . import BaseInitializer, register_initializer


class GroupInitializer(BaseInitializer):
    data_file_name = "groups.yml"

    def load_data(self):
        groups = self.load_yaml()
        if groups is None:
            return

        for groupname, group_details in groups.items():
            group, created = NetBoxGroup.objects.get_or_create(name=groupname)
            if created:
                print("👥 Created group", groupname)
            for username in group_details.get("users", []):
                user = NetBoxUser.objects.get(username=username)
                if user:
                    group.user_set.add(user)
                    print(" 👤 Assigned user %s to group %s" % (username, group.name))
            group.save()


register_initializer("groups", GroupInitializer)
