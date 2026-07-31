"""The top-level MTDx62_MB device object."""

from __future__ import annotations
from enum import IntEnum

from modbus_connection import ModbusUnit
from modbus_connection.model import (
    Component,
    ComponentGroup,
    gauge,
    integer,
    uint32,
    discrete_input,
    enum,
)


class DeviceStatus(IntEnum):
    """Enumerates the possible statuses of an MTDx62-MB device."""

    SELF_CHECKING = 0
    """ Device program self checking in progress """

    SELF_TEST_SUCCESS = 1
    """ Device program self-test successful """

    SELF_TEST_FILED = 2
    """ Device program self-test failed """

    OTHER_FAULTS = 3
    """ Other faults """

    RADAR_MALFUNCTION = 4
    """ Radar module malfunction """

    RS485_FAILURE = 5
    """ RS485 communication failure """

    RADAR_AND_RS485_MALFUNCTION = 6
    """ Radar and RS485 both malfunction """


class ParityType(IntEnum):
    """Enumerates the possible parity types for Modbus communication."""

    NO_PARITY = 0
    ODD_PARITY = 1
    EVEN_PARITY = 2


class DataReportMode(IntEnum):
    """Enumerates the possible data report modes for the device."""

    REPORT_ON = 1
    """ Report data on """

    REPORT_OFF = 2
    """ Report data off """


def format_version(value: int | None) -> str | None:
    """Format raw version as string, e.g. 0x00010203 indicates version information is '1.2.3'."""

    if value is None:
        return None

    version_major = value >> 16 & 0xFF
    version_minor = value >> 8 & 0xFF
    version_revision = value & 0xFF
    return f"{version_major}.{version_minor}.{version_revision}"


class DeviceState(Component):
    """Device state component"""

    register_space = "input"

    person_status = discrete_input(0)
    illumination = gauge(1, 0.1, signed=False, unit="Lux")
    target_distance = gauge(2, 0.01, signed=False, unit="m")
    device_status = enum(3, DeviceStatus)

    app_version_raw = uint32(4)
    radar_version_raw = uint32(6)

    @property
    def app_version(self) -> str | None:
        return format_version(self.app_version_raw)

    @property
    def radar_version(self) -> str | None:
        return format_version(self.radar_version_raw)


class DeviceConfig(Component):
    """Device configuration component"""

    register_space = "holding"

    detection_distance = gauge(0, 0.01, signed=False, unit="m")
    """ Detection distance (0.6-10 m, default 6 m) """

    detection_shielding_distance = gauge(1, 0.01, signed=False, unit="m")
    """ Detection shielding distance (0.1-5 m, default 0.6 m) """

    entry_confirmation_delay = gauge(2, 0.01, signed=False, unit="s")
    """ Delay in admission confirmation (0-5 s, default 0.1 s) """

    departure_disappearance_delay = gauge(3, 1, signed=False, unit="s")
    """ Departure disappearance delay (5-1500 s, default 30 s) """

    trigger_sensitivity = integer(4, signed=False)
    """ Trigger sensitivity (1-9, default 7) """

    personnel_maintain_sensitivity = integer(5, signed=False)
    """ Personnel maintain sensitivity (1-9, default 7) """

    entry_indentation_distance = gauge(6, 0.01, signed=False, unit="m")
    """ Entrance distance indented (0-10 m, default 0.6 m) """

    device_id = integer(7, signed=False)
    """ Device ID (1-247, default 1) """

    baud_rate = integer(8, signed=False, unit="bps")
    """ Baud rate (1200-57600 bps, default 9600 bps) """

    parity_type = enum(9, ParityType)
    """ Parity type (0: No parity, 1: Odd parity, 2: Even parity, default 0) """

    data_report_mode = enum(10, DataReportMode)
    """ Data report mode (1: Report data on, 2: Report data off, default 2) """

    light_threshold = gauge(11, 0.1, signed=False, unit="Lux")
    """ Light threshold (0-4200 Lux, default 0 - disable lighting threshold function)

    If current lighting value is less than the lighting threshold and someone is detected, output the presence status; otherwise, output no one. """

    data_report_interval = gauge(12, 1, signed=False, unit="s")
    """ Data report interval (1-36000 s, default 1) """

    device_mac = integer(13, signed=False)
    """ Device MAC address (0-23, default factory random) """


class MTDx62_MB(ComponentGroup):
    """MTDx62-MB human presence sensor."""

    def __init__(self, modbus_unit: ModbusUnit):
        self._modbus_unit = modbus_unit

        self.device_state = DeviceState(modbus_unit)
        self.device_config = DeviceConfig(modbus_unit)
