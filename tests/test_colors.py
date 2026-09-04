from netbox.choices import ColorChoices

from netbox_initializers.initializers.rack_roles import RackRoleInitializer
from netbox_initializers.initializers.tags import TagInitializer


class TestColorChoices:
    def test_color_name_converted_to_hex(self) -> None:
        initializer = RackRoleInitializer("")
        # "Dark red" is mapped to "aa1409" in ColorChoices
        params: dict[str, object] = {"name": "Server", "color": "Dark Red"}
        result = initializer.prepare_params(params)

        assert result is not None
        assert result["color"] == "aa1409"

    def test_color_hex_matching_choice_remains_hex(self) -> None:
        initializer = RackRoleInitializer("")
        params: dict[str, object] = {"name": "Switch", "color": "aa1409"}
        result = initializer.prepare_params(params)

        assert result is not None
        assert result["color"] == "aa1409"

    def test_custom_hex_preserved(self) -> None:
        initializer = RackRoleInitializer("")
        # A custom hex code not present in standard ColorChoices
        params: dict[str, object] = {"name": "Custom", "color": "123456"}
        result = initializer.prepare_params(params)

        assert result is not None
        assert result["color"] == "123456"

    def test_params_without_color(self) -> None:
        initializer = RackRoleInitializer("")
        params: dict[str, object] = {"name": "NoColor"}
        result = initializer.prepare_params(params)

        assert result is not None
        assert "color" not in result
        assert result["name"] == "NoColor"

    def test_all_color_choices_can_be_resolved(self) -> None:
        initializer = RackRoleInitializer("")
        for hex_code, color_name in ColorChoices.CHOICES:
            params: dict[str, object] = {"name": "Test", "color": color_name}
            result = initializer.prepare_params(params)
            assert result is not None
            assert result["color"] == hex_code

    def test_tag_initializer_color_and_object_types(self) -> None:
        initializer = TagInitializer("")
        params: dict[str, object] = {
            "name": "Production",
            "color": "Dark Red",
            "object_types": [{"app": "dcim", "model": "device"}],
        }
        result = initializer.prepare_params(params)

        assert result is not None
        assert result["color"] == "aa1409"
        assert "object_types" not in result
        assert initializer._object_types == [{"app": "dcim", "model": "device"}]  # pyright: ignore[reportPrivateUsage]
