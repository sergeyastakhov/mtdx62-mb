"""Classes to represent device status"""

from __future__ import annotations
from enum import IntEnum

from modbus_connection.model import (
    Component,
    gauge,
    integer,
    uint32,
    enum,
)


class DeviceStatus(IntEnum):
    """Enumerates the possible statuses of an MTDx62-MB device."""

    SELF_CHECKING = 0
    """ Device program self checking in progress """

    SELF_TEST_SUCCESS = 1
    """ Device program self-test successful """

    SELF_TEST_FAILED = 2
    """ Device program self-test failed """

    OTHER_FAULTS = 3
    """ Other faults """

    RADAR_MALFUNCTION = 4
    """ Radar module malfunction """

    RS485_FAILURE = 5
    """ RS485 communication failure """

    RADAR_AND_RS485_MALFUNCTION = 6
    """ Radar and RS485 both malfunction """


class DeviceState(Component):
    """Device state component"""

    register_space = "input"

    _person_status = integer(0, signed=False)
    illumination = gauge(1, 0.1, signed=False, unit="Lux")
    target_distance = gauge(2, 0.01, signed=False, unit="m")
    device_status = enum(3, DeviceStatus)

    @property
    def person_status(self) -> bool | None:
        """Return True if a person is detected, False if not, or None if unknown."""

        if self.device_status != DeviceStatus.SELF_TEST_SUCCESS:
            return None

        return self._person_status != 0


def format_version(value: int | None) -> str | None:
    """Format raw version as string, e.g. 0x00010203 indicates version information is '1.2.3'."""

    if value is None:
        return None

    version_major = value >> 16 & 0xFF
    version_minor = value >> 8 & 0xFF
    version_revision = value & 0xFF
    return f"{version_major}.{version_minor}.{version_revision}"


class DeviceVersionInfo(Component):
    """Device version info component"""

    register_space = "input"

    _app_version_raw = uint32(4)
    _radar_version_raw = uint32(6)

    @property
    def app_version(self) -> str | None:
        """Return the formatted application version string, e.g. '1.2.3'."""
        return format_version(self._app_version_raw)

    @property
    def radar_version(self) -> str | None:
        """Return the formatted radar version string, e.g. '1.2.3'."""
        return format_version(self._radar_version_raw)
