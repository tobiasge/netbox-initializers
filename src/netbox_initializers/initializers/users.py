from django.utils.crypto import get_random_string
from users.models import Token, User

from netbox_initializers.initializers.base import BaseInitializer, register_initializer


class UserInitializer(BaseInitializer):
    data_file_name = "users.yml"

    def load_data(self):
        users = self.load_yaml()
        if users is None:
            return

        for username, user_details in users.items():
            token_data = user_details.pop("token", Token.generate_key())
            password = user_details.pop("password", get_random_string(length=25))
            user, created = User.objects.get_or_create(username=username, defaults=user_details)
            if created:
                user.set_password(password)
                user.save()
                if token_data and "key" in token_data and "value" in token_data:
                    Token.objects.create(
                        user=user, key=token_data["key"], token=token_data["value"]
                    )
                print("👤 Created user", username)


register_initializer("users", UserInitializer)
