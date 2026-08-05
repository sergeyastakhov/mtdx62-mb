"""Testing functions from the source code."""

from __future__ import annotations

from mtdx62_mb import MTDx62_MB
from mtdx62_mb.device_state import format_version, DeviceStatus

from conftext import mock_device


def test_format_version():
    """
    Test function format_version
    """
    assert format_version(None) is None
    assert format_version(0x00010203) == "1.2.3"


async def test_device_state(mock_device: MTDx62_MB) -> None:
    """Test the MTDx62-MB device state reading."""
    await mock_device.async_update_state()
    state = mock_device.state

    assert state.person_status is True
    assert state.illumination == 100
    assert state.target_distance == 1.0
    assert state.device_status == DeviceStatus.SELF_TEST_SUCCESS

    version = mock_device.version

    assert version.app_version == "1.1.4"
    assert version.radar_version == "0.0.0"
