"""Classes to represent device config"""

from __future__ import annotations
from enum import IntEnum

from modbus_connection.model import (
    Component,
    gauge,
    integer,
    enum,
)


class DetectionConfig(Component):
    """Detection configuration component"""

    register_space = "holding"

    detection_distance = gauge(0, 0.01, signed=False, unit="m")
    """ Detection distance (0.6-10 m, default 6 m)

    Maximum distance for presence detection. Note:
    1. Detection distance refers to the longest distance of the sensor from
    the straight line that can detect the movement, micromovement and breathing
    target, and the maximumdiameter or radiusnot mapping to the ground.
    2. The distance is non-absolute distance, the sensor detection has a
    distance resolution, the resolution is about 1m. If 3m is set, it is normal
    to trigger in the ±1m interval at the 3m position.
    3. The distance value is mainly used as filter glass partition, gypsum board
    and wood partition, and is not strictly used as the detection area. If 3m is
    set, there may be missing report and false touch at 3m position ± 1m
    """

    detection_shielding_distance = gauge(1, 0.01, signed=False, unit="m")
    """ Detection shielding distance (0.1-5 m, default 0.6 m)

    Minimum distance for presence detection. """

    entry_confirmation_delay = gauge(2, 0.01, signed=False, unit="s")
    """ Delay in admission confirmation (0-0.5 s, default 0.05 s)

    Admission filtering time (No one to someone).

    The longer the setting time, the slower the sensor response and the less
    likely it is to trigger incorrectly;
    The time setting is short and the response is fast, but the probability
    of error increases. In practical use, it is recommended to set the sensor
    response time to no more than 0.25s, as a response time greater than 0.25s
    is considered slow.

    Note: The main function is to solve the following interferences:
    1. False triggering caused by rapid flashing in and out of the detection
    boundary.
    2. Installing sensors in environments that may experience momentary
    lighting changesshaking to avoid false triggering.
    3. Installing in environments with large changes in wind pressure that
    can easily cause momentary vibration. """

    departure_disappearance_delay = gauge(3, 1, signed=False, unit="s")
    """ Departure disappearance delay (2-64800 s, default 15 s)

    Practical usage recommendation is 15-180 seconds. If it is too small, it
    is easy to miss the report, and if it is too large, it will affect the experience.

    Note:

    This delay represents:
    1. The time when the sensor triggers the person to leave and become unmanned;
    2. The sensor triggers within the delay time, continue delay accordingly.
    3. The observation window of the sensor, the longer the delay, the lower the
    probability of sensor false positives, and the respiratory detection delay should
    not be less than 60 seconds. """

    trigger_sensitivity = integer(4, signed=False)
    """ Trigger sensitivity (1-9, default 7)

    Note:

    The larger the value, the more sensitive it is. Sensitivity within 6 can only be used
    for motion detection, while sensitivity between 7-9 can be used for respiratory
    detection, indicating reliability. """

    maintain_sensitivity = integer(5, signed=False)
    """ Maintain presence sensitivity (1-9, default 7)

    This parameter is related to the "Departure disappearance delay" (refer to the
    recommended parameter configuration for different scenarios for corresponding settings).

    Note:

    The larger the value, the more sensitive it is. Sensitivity within 6 can only be used
    for motion detection, while sensitivity between 7-9 can be used for respiratory
    detection, indicating reliability. """

    entry_indentation_distance = gauge(6, 0.01, signed=False, unit="m")
    """ Entrance distance indented (0-10 m, default 0.6 m) """

    light_threshold = gauge(11, 0.1, signed=False, unit="Lux")
    """ Light threshold (0-4200 Lux, default 0 - disable lighting threshold function)

    If current lighting value is less than the lighting threshold and someone is detected,
    output the presence status; otherwise, output no one. """


class ParityType(IntEnum):
    """Enumerates the possible parity types for Modbus communication."""

    NO_PARITY = 0
    ODD_PARITY = 1
    EVEN_PARITY = 2


class ModbusConfig(Component):
    """Modbus configuration component"""

    register_space = "holding"

    device_id = integer(7, signed=False)
    """ Device ID (1-247, default 1) """

    baud_rate = integer(8, signed=False, unit="bps")
    """ Baud rate (1200-57600 bps, default 9600 bps) """

    parity_type = enum(9, ParityType)
    """ Parity type (0: No parity, 1: Odd parity, 2: Even parity, default 0) """

    device_mac = integer(13, signed=False)
    """ Device MAC address (0-23, default factory random) """


class DataReportMode(IntEnum):
    """Enumerates the possible data report modes for the device."""

    REPORT_ON = 1
    """ Report data on """

    REPORT_OFF = 2
    """ Report data off """


class DataReportConfig(Component):
    """Data report configuration component"""

    register_space = "holding"

    data_report_mode = enum(10, DataReportMode)
    """ Data report mode (1: Report data on, 2: Report data off, default 2) """

    data_report_interval = gauge(12, 1, signed=False, unit="s")
    """ Data report interval (1-36000 s, default 1) """
