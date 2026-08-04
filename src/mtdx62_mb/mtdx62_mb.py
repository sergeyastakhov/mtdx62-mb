"""The top-level MTDx62_MB device object."""

from __future__ import annotations

from modbus_connection import ModbusUnit
from modbus_connection.model import ComponentGroup

from .device_state import DeviceState, DeviceVersionInfo
from .device_config import DetectionConfig, ModbusConfig, DataReportConfig


class MTDx62_MB:  # pylint: disable=invalid-name
    """MTDx62-MB human presence sensor."""

    def __init__(self, unit: ModbusUnit):
        self._unit = unit

        self.state = DeviceState(unit)
        self.version = DeviceVersionInfo(unit)

        self.detection_config = DetectionConfig(unit)
        self.modbus_config = ModbusConfig(unit)
        self.data_report_config = DataReportConfig(unit)

        self._components = (
            self.state,
            self.version,
            self.detection_config,
            self.modbus_config,
            self.data_report_config,
        )

        self._all_group = ComponentGroup(unit, self._components)

        self._state_group = ComponentGroup(unit, (self.state, self.version))

        self._config_group = ComponentGroup(
            unit, (self.detection_config, self.modbus_config, self.data_report_config)
        )

    async def async_update(self) -> None:
        """Refresh all components"""
        await self._all_group.async_update()

    async def async_update_state(self) -> None:
        """Refresh state components"""
        await self._state_group.async_update()

    async def async_update_config(self) -> None:
        """Refresh config info"""
        await self._config_group.async_update()
