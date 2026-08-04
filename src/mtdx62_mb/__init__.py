"""mtdx62-mb — read a MTDx62-MB human presence sensor over Modbus."""

from __future__ import annotations

from .mtdx62_mb import MTDx62_MB
from .device_state import DeviceState, DeviceVersionInfo, DeviceStatus
from .device_config import (
    DetectionConfig,
    ModbusConfig,
    ParityType,
    DataReportConfig,
    DataReportMode,
)

__all__ = [
    "MTDx62_MB",
    "DeviceState",
    "DeviceVersionInfo",
    "DeviceStatus",
    "DetectionConfig",
    "ModbusConfig",
    "ParityType",
    "DataReportConfig",
    "DataReportMode",
]

__version__ = "0.0.1"
