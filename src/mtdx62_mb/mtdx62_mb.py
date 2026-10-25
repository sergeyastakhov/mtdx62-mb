"""The top-level MTDx62_MB device object."""

from __future__ import annotations

from modbus_connection import ModbusUnit
from modbus_connection.model import ComponentGroup, Device, UpdateReport

from .device_state import DeviceState, DeviceVersionInfo
from .device_config import DetectionConfig, ModbusConfig, DataReportConfig


class MTDx62_MB(Device):  # pylint: disable=invalid-name
    """MTDx62-MB human presence sensor."""

    def __init__(self, unit: ModbusUnit):
        super().__init__(unit)

        self.state = DeviceState(unit)
        self.version = DeviceVersionInfo(unit)

        self.detection_config = DetectionConfig(unit)
        self.modbus_config = ModbusConfig(unit)
        self.data_report_config = DataReportConfig(unit)

        self._all_group = ComponentGroup(
            unit,
            (
                self.state,
                self.version,
                self.detection_config,
                self.modbus_config,
                self.data_report_config,
            ),
        )

        self._config_group = ComponentGroup(
            unit, (self.detection_config, self.modbus_config, self.data_report_config)
        )

    async def _async_setup(self) -> None:
        """Read what never changes."""
        await self.version.async_update()  # version: read once, never polled

    async def async_update(self) -> None:
        """Refresh all components"""
        await self._all_group.async_update()

    async def async_update_state(self) -> UpdateReport:
        """Refresh state components"""
        return await self.async_poll(("state",))

    async def async_update_config(self) -> UpdateReport:
        """Refresh config info"""
        return await self.async_poll(("_config_group",))
