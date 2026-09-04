from unittest.mock import MagicMock

import pytest

from netbox_initializers.initializers.device_types import expand_templates


class TestExpandTemplates:
    def test_no_templates_returns_original_with_device_type(self) -> None:
        device_type = MagicMock()
        params: list[dict[str, object]] = [{"name": "GigabitEthernet0/0/1", "type": "1000base-t"}]

        result = expand_templates(params, device_type)

        assert len(result) == 1
        assert result[0]["name"] == "GigabitEthernet0/0/1"
        assert result[0]["device_type"] is device_type
        assert result[0]["type"] == "1000base-t"

    def test_range_template_expansion(self) -> None:
        device_type = MagicMock()
        params: list[dict[str, object]] = [{"name_template": "GigabitEthernet1/0/[1-4]", "type": "1000base-t"}]

        result = expand_templates(params, device_type)

        assert len(result) == 4
        names = [r["name"] for r in result]
        assert names == [
            "GigabitEthernet1/0/1",
            "GigabitEthernet1/0/2",
            "GigabitEthernet1/0/3",
            "GigabitEthernet1/0/4",
        ]
        for r in result:
            assert r["device_type"] is device_type
            assert r["type"] == "1000base-t"
            assert "name_template" not in r

    def test_list_template_expansion(self) -> None:
        device_type = MagicMock()
        params: list[dict[str, object]] = [{"name_template": "Slot0/[mgmt,console]", "type": "other"}]

        result = expand_templates(params, device_type)

        assert len(result) == 2
        names = [r["name"] for r in result]
        assert names == ["Slot0/mgmt", "Slot0/console"]

    def test_multiple_synchronized_templates(self) -> None:
        device_type = MagicMock()
        params: list[dict[str, object]] = [
            {
                "name_template": "Port[1-3]",
                "label_template": "Uplink [1-3]",
                "positions_template": "[1-3]",
            }
        ]

        result = expand_templates(params, device_type)

        assert len(result) == 3
        assert result[0]["name"] == "Port1"
        assert result[0]["label"] == "Uplink 1"
        assert result[0]["positions"] == "1"
        assert result[2]["name"] == "Port3"
        assert result[2]["label"] == "Uplink 3"
        assert result[2]["positions"] == "3"

    def test_mixed_plain_and_template_raises_value_error(self) -> None:
        device_type = MagicMock()
        params: list[dict[str, object]] = [
            {
                "name": "Fixed Port",
                "label_template": "Uplink [1-3]",
            }
        ]

        with pytest.raises(ValueError, match="Mix of plain and template keys"):
            _ = expand_templates(params, device_type)

    def test_mismatched_template_lengths_raises_value_error(self) -> None:
        device_type = MagicMock()
        params: list[dict[str, object]] = [
            {
                "name_template": "Port[1-4]",
                "label_template": "Uplink [1-2]",
            }
        ]

        with pytest.raises(ValueError, match="must be equal"):
            _ = expand_templates(params, device_type)
