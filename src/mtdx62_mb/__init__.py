"""mtdx62-mb — read a MTDx62-MB human presence sensor over Modbus.

Construct ``MTDx62_MB(unit)`` with a ``modbus_connection.ModbusUnit``, call
``await device.async_update()``, then read its sub-systems as normal Python
objects::

    device.sensors.af1
    device.rk1.room_setpoint_active
    device.rk4.storage_tank_charging_pump_running

Controller domains live in ``subsystems``. Static models, hydronic tables,
range maps, settings, and sensor-variant logic live in ``configurations``.
The public subsystem classes remain available while ``Trovis557x`` exposes
stable ``rk1`` through ``rk4`` slots.
"""
from __future__ import annotations

__version__ = "0.0.2"
