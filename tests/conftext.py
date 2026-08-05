"""Fixtures: a MTDx62-MB over modbus-connection's in-memory mock backend.

The mock backend and its fixtures ship with ``modbus-connection``. They are
imported explicitly below so the test suite does not depend on pytest entry-point
autoloading. There is no real server, socket, or backend here — just an
address-keyed store loaded with device register values.
"""

from __future__ import annotations

import pytest
from modbus_connection.mock import MockModbusUnit
from modbus_connection.pytest_plugin import (
    mock_modbus_connection,
    mock_modbus_unit,
)

from mtdx62_mb import MTDx62_MB

# run: PYTHONPATH=src:/config/dev/modbus-connection/src python -m pytest

# Raw register words keyed by their (protocol) address; decoded view inline.

INPUT: dict[int, int] = {
    0: 1,  # person_status -> True
    1: 1000,  # illumination -> 100 Lux
    2: 100,  # target_distance -> 1.0 m
    3: 1,  # device_status -> SELF_TEST_SUCCESS
    4: 0x0001,  # app_version -> 1.1.4
    5: 0x0104,
    6: 0x0000,  # radar_version -> 0.0.0
    7: 0x0000,
}

HOLDING: dict[int, int] = {
    0: 600,  # detection_distance -> 6 m
    1: 60,  # detection_shielding_distance -> 0.6 m
    2: 5,  # entry_confirmation_delay -> 0.05 s
    3: 15,  # departure_disappearance_delay -> 15 s
    4: 7,  # trigger_sensitivity -> 7
    5: 7,  # maintain_sensitivity -> 7
    6: 60,  # entry_indentation_distance -> 0.6 m
    7: 1,  # device_id -> 1
    8: 9600,  # baud_rate -> 9600 bps
    9: 0,  # parity_type -> NO_PARITY
    10: 2,  # data_report_mode -> REPORT_OFF
    11: 0,  # light_threshold -> 0 Lux
    12: 600,  # data_report_interval -> 600 s
    13: 2,  # device_mac -> 2
}


@pytest.fixture
def mock_device(mock_modbus_unit: MockModbusUnit) -> MTDx62_MB:
    """A MTDx62-MB over the mock unit, preloaded with device values."""
    mock_modbus_unit.input.update(INPUT)
    mock_modbus_unit.holding.update(HOLDING)
    return MTDx62_MB(mock_modbus_unit)
