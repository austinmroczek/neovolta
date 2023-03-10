"""Sensor platform for neovolta."""
from __future__ import annotations
from dataclasses import dataclass
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
)

from .const import DOMAIN
from .coordinator import NeovoltaDataUpdateCoordinatoror
from .entity import NeovoltaEntity


class NeovoltaBatteryDescription(SensorEntityDescription):
    """Battery description."""

    def __init__(self, key, name):
        """Initialize."""
        super().__init__(key=key, name=name)
        self.device_class = SensorDeviceClass.BATTERY
        self.native_unit_of_measurement = "%"
        self.state_class = SensorStateClass.MEASUREMENT


class NeovoltaEnergyDescription(SensorEntityDescription):
    """Energy description."""

    def __init__(self, key, name):
        """Initialize."""
        super().__init__(key=key, name=name)
        self.device_class = SensorDeviceClass.ENERGY
        self.native_unit_of_measurement = "kWh"
        self.state_class = SensorStateClass.TOTAL_INCREASING


class NeovoltaVoltageDescription(SensorEntityDescription):
    """Voltage description."""

    def __init__(self, key, name):
        """Initialize."""
        super().__init__(key=key, name=name)
        self.device_class = SensorDeviceClass.VOLTAGE
        self.native_unit_of_measurement = "V"
        self.suggested_display_precision = 2
        self.state_class = SensorStateClass.MEASUREMENT


class NeovoltaCurrentDescription(SensorEntityDescription):
    """Current description."""

    def __init__(self, key, name):
        """Initialize."""
        super().__init__(key=key, name=name)
        self.device_class = SensorDeviceClass.CURRENT
        self.native_unit_of_measurement = "A"
        self.suggested_display_precision = 2
        self.state_class = SensorStateClass.MEASUREMENT


class NeovoltaFrequencyDescription(SensorEntityDescription):
    """Frequency description."""

    def __init__(self, key, name):
        """Initialize."""
        super().__init__(key=key, name=name)
        self.device_class = SensorDeviceClass.FREQUENCY
        self.native_unit_of_measurement = "Hz"
        self.suggested_display_precision = 2
        self.state_class = SensorStateClass.MEASUREMENT


ENTITY_DESCRIPTIONS = (
    NeovoltaBatteryDescription(key="battery_total", name="Battery Total"),
    NeovoltaBatteryDescription(key="battery_tbd", name="Battery TBD"),
    NeovoltaEnergyDescription(
        key="energy_from_grid_cumulative", name="Energy From Grid Cumulative"
    ),
    NeovoltaEnergyDescription(key="daily_generation", name="Daily Generation"),
    NeovoltaEnergyDescription(
        key="battery_charged_today",
        name="Battery Charged Today",
    ),
    NeovoltaEnergyDescription(
        key="battery_discharged_today",
        name="Battery Discharged Today",
    ),
    NeovoltaEnergyDescription(
        key="energy_from_grid_today",
        name="Energy From Grid Today",
    ),
    NeovoltaEnergyDescription(
        key="energy_to_grid_today",
        name="Energy To Grid Today",
    ),
    NeovoltaEnergyDescription(
        key="battery_charged_cumulative",
        name="Battery Charged Cumulative",
    ),
    NeovoltaEnergyDescription(
        key="battery_discharged_cumulative",
        name="Battery Discharged Cumulative",
    ),
    NeovoltaVoltageDescription(key="battery_voltage1", name="Battery Voltage TBD1"),
    NeovoltaVoltageDescription(key="battery_voltage2", name="Battery Voltage TBD2"),
    NeovoltaVoltageDescription(key="battery_voltage3", name="Battery Voltage TBD3"),
    NeovoltaVoltageDescription(key="bms_voltage", name="BMS Voltage"),
    NeovoltaEnergyDescription(
        key="energy_to_grid_cumulative",
        name="Energy to Grid Cumulative",
    ),
    NeovoltaEnergyDescription(
        key="energy_consumed_today",
        name="Energy Consumed Today",
    ),
    NeovoltaEnergyDescription(
        key="energy_consumed_cumulative",
        name="Energy Consumed Cumulative",
    ),
    NeovoltaVoltageDescription(key="grid_voltage_rua", name="Grid Voltage R/U/A"),
    NeovoltaVoltageDescription(key="grid_voltage_svb", name="Grid Voltage S/V/B"),
    NeovoltaVoltageDescription(key="pv_voltage1", name="PV Voltage1"),
    NeovoltaVoltageDescription(key="pv_voltage2", name="PV Voltage2"),
    NeovoltaVoltageDescription(key="grid_voltage_rsuvab", name="Grid Voltage RS/UV/AB"),
    NeovoltaFrequencyDescription(key="grid_frequency", name="Grid Frequency"),
    NeovoltaFrequencyDescription(key="frequency2", name="Frequency2"),
    NeovoltaFrequencyDescription(key="frequency3", name="Frequency3"),
    NeovoltaFrequencyDescription(key="frequency4", name="Frequency4"),
    NeovoltaVoltageDescription(key="voltage148", name="Voltage 148"),
    NeovoltaVoltageDescription(key="voltage149", name="Voltage 149"),
    NeovoltaVoltageDescription(key="voltage150", name="Voltage 150"),
    NeovoltaVoltageDescription(key="voltage151", name="Voltage 151"),
    NeovoltaVoltageDescription(key="voltage152", name="Voltage 152"),
    NeovoltaVoltageDescription(key="voltage153", name="Voltage 153"),
    NeovoltaVoltageDescription(key="voltage154", name="Voltage 154"),
    NeovoltaVoltageDescription(key="voltage155", name="Voltage 155"),
    NeovoltaVoltageDescription(key="voltage156", name="Voltage 156"),
    NeovoltaVoltageDescription(key="voltage157", name="Voltage 157"),
    NeovoltaVoltageDescription(key="voltage158", name="Voltage 158"),
    NeovoltaVoltageDescription(key="voltage181", name="Voltage 181"),
    NeovoltaVoltageDescription(key="voltage182", name="Voltage 182"),
    NeovoltaVoltageDescription(key="voltage319", name="Voltage 319"),
    NeovoltaCurrentDescription(key="grid_current_rua", name="Grid Current R/U/A"),
    NeovoltaCurrentDescription(key="grid_current_svb", name="Grid Current S/V/B"),
    NeovoltaCurrentDescription(key="meter_ac_current_a", name="Meter AC Current A"),
    NeovoltaCurrentDescription(key="meter_ac_current_b", name="Meter AC Current B"),
    NeovoltaCurrentDescription(key="current132", name="Current 132"),
    NeovoltaCurrentDescription(key="current133", name="Current 133"),
    NeovoltaCurrentDescription(key="current164", name="Current 164"),
    NeovoltaCurrentDescription(key="current165", name="Current 165"),
    NeovoltaCurrentDescription(key="current166", name="Current 166"),
    NeovoltaCurrentDescription(key="current176", name="Current 176"),
    NeovoltaCurrentDescription(key="current177", name="Current 177"),
    NeovoltaCurrentDescription(key="current178", name="Current 178"),
    NeovoltaCurrentDescription(key="current179", name="Current 179"),
    NeovoltaCurrentDescription(key="current180", name="Current 180"),
    NeovoltaCurrentDescription(key="current185", name="Current 185"),
    NeovoltaCurrentDescription(key="current314", name="Current 314"),
    NeovoltaCurrentDescription(key="current315", name="Current 315"),
    NeovoltaEnergyDescription(key="energy24", name="Energy 24"),
    NeovoltaEnergyDescription(key="energy65", name="Energy 65"),
    NeovoltaEnergyDescription(key="energy66", name="Energy 66"),
    NeovoltaEnergyDescription(key="energy68", name="Energy 68"),
    NeovoltaEnergyDescription(key="energy87", name="Energy 87"),
    NeovoltaEnergyDescription(key="energy96", name="Energy 96"),
    NeovoltaEnergyDescription(key="energy131", name="Energy 131"),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        NeovoltaSensor(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class NeovoltaSensor(NeovoltaEntity, SensorEntity):
    """neovolta Sensor class."""

    def __init__(
        self,
        coordinator: NeovoltaDataUpdateCoordinatoror,
        entity_description: SensorEntityDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{self.coordinator.client.data['serial_number']}_{entity_description.key}"
        )

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        return self.coordinator.client.data.get(self.entity_description.key)
