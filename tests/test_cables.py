from types import SimpleNamespace
from typing import final, override
from unittest.mock import MagicMock, patch

from dcim.models import (
    ConsolePort,
    ConsoleServerPort,
    FrontPort,
    Interface,
    PowerFeed,
    PowerOutlet,
    PowerPort,
    RearPort,
)

from netbox_initializers.initializers.cables import check_termination_types, get_cable_name


@final
class DummyTermination:
    name: str
    device: str
    circuit: object
    power_panel_id: int

    def __init__(
        self,
        name: str,
        device: str | None = None,
        circuit: object | None = None,
        power_panel_id: int | None = None,
    ) -> None:
        self.name = name
        if device is not None:
            self.device = device
        if circuit is not None:
            self.circuit = circuit
        if power_panel_id is not None:
            self.power_panel_id = power_panel_id

    @override
    def __str__(self) -> str:
        return self.name


class TestCheckTerminationTypes:
    def test_same_power_terminations_rejected(self) -> None:
        valid, msg = check_termination_types(PowerPort, PowerPort)
        assert not valid
        assert "Can't connect the same power terminations together" in msg

    def test_power_outlet_with_power_feed_rejected(self) -> None:
        valid, msg = check_termination_types(PowerOutlet, PowerFeed)
        assert not valid
        assert "PowerOutlet can't be connected with PowerFeed" in msg

    def test_power_port_with_power_outlet_valid(self) -> None:
        valid, msg = check_termination_types(PowerPort, PowerOutlet)
        assert valid
        assert msg == ""

    def test_power_port_with_power_feed_valid(self) -> None:
        valid, msg = check_termination_types(PowerPort, PowerFeed)
        assert valid
        assert msg == ""

    def test_power_mixed_with_data_port_rejected(self) -> None:
        valid, msg = check_termination_types(PowerPort, Interface)
        assert not valid
        assert "Can't mix power terminations with port terminations" in msg

    def test_front_port_with_any_valid(self) -> None:
        valid, msg = check_termination_types(FrontPort, RearPort)
        assert valid
        assert msg == ""

        valid, msg = check_termination_types(Interface, FrontPort)
        assert valid
        assert msg == ""

    def test_console_port_restrictions(self) -> None:
        valid, msg = check_termination_types(ConsolePort, ConsolePort)
        assert not valid
        assert "ConsolePorts can only be connected to ConsoleServerPorts" in msg

        valid, msg = check_termination_types(ConsolePort, Interface)
        assert not valid
        assert "ConsolePorts can only be connected to ConsoleServerPorts" in msg

        valid, msg = check_termination_types(ConsolePort, ConsoleServerPort)
        assert valid
        assert msg == ""

    def test_interface_to_interface_valid(self) -> None:
        valid, msg = check_termination_types(Interface, Interface)
        assert valid
        assert msg == ""

    def test_with_model_class_attribute(self) -> None:
        mock_ct_a = SimpleNamespace(model_class=lambda: Interface)
        mock_ct_b = SimpleNamespace(model_class=lambda: Interface)

        valid, msg = check_termination_types(mock_ct_a, mock_ct_b)
        assert valid
        assert msg == ""


class TestGetCableName:
    def test_device_interfaces(self) -> None:
        term_a = DummyTermination("GigabitEthernet0/1", device="switch-1")
        term_b = DummyTermination("eth0", device="server-1")

        name = get_cable_name((term_a, None), (term_b, None))
        assert name == "switch-1 GigabitEthernet0/1 <---> eth0 server-1"

    def test_circuits(self) -> None:
        circuit_a = SimpleNamespace(cid="CIR-100")
        circuit_b = SimpleNamespace(cid="CIR-200")
        term_a = DummyTermination("A", circuit=circuit_a)
        term_b = DummyTermination("Z", circuit=circuit_b)

        name = get_cable_name((term_a, None), (term_b, None))
        assert name == "CIR-100 A <---> Z CIR-200"

    @patch("netbox_initializers.initializers.cables.PowerPanel.objects.get")
    def test_power_panels(self, mock_panel_get: MagicMock) -> None:
        mock_panel_get.return_value = "Panel-1"
        term_a = DummyTermination("Feed-A", power_panel_id=42)
        term_b = DummyTermination("Input-1", device="pdu-1")

        name = get_cable_name((term_a, None), (term_b, None))
        assert name == "Panel-1 Feed-A <---> Input-1 pdu-1"
