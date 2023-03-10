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


class NeovoltaFrequencyDescription(SensorEntityDescription):
    """Frequency description."""

    def __init__(self, key, name):
        """Initialize."""
        super().__init__(key=key, name=name)
        self.device_class = (SensorDeviceClass.FREQUENCY,)
        self.native_unit_of_measurement = ("Hz",)
        self.state_class = (SensorStateClass.MEASUREMENT,)


ENTITY_DESCRIPTIONS = (
    NeovoltaBatteryDescription(key="battery_total", name="Battery Total"),
    NeovoltaBatteryDescription(key="battery_tbd", name="Battery TBD"),
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
        key="battery_charged_cummulative",
        name="Battery Charged Cummulative",
    ),
    NeovoltaEnergyDescription(
        key="battery_discharged_cummulative",
        name="Battery Discharged Cummulative",
    ),
    NeovoltaVoltageDescription(key="battery_voltage1", name="Battery Voltage TBD1"),
    NeovoltaVoltageDescription(key="battery_voltage2", name="Battery Voltage TBD2"),
    NeovoltaVoltageDescription(key="battery_voltage3", name="Battery Voltage TBD3"),
    NeovoltaVoltageDescription(key="battery_voltage4", name="Battery Voltage TBD4"),
    NeovoltaEnergyDescription(
        key="energy_to_grid_cummulative",
        name="Energy to Grid Cummulative",
    ),
    NeovoltaEnergyDescription(
        key="energy_consumed_today",
        name="Energy Consumed Today",
    ),
    NeovoltaEnergyDescription(
        key="energy_consumed_cummulative",
        name="Energy Consumed Cummulative",
    ),
    NeovoltaVoltageDescription(key="grid_voltage_rua", name="Grid Voltage R/U/A"),
    NeovoltaVoltageDescription(key="grid_voltage_svb", name="Grid Voltage S/V/B"),
    NeovoltaVoltageDescription(key="pv_voltage1", name="PV Voltage1"),
    NeovoltaVoltageDescription(key="pv_voltage2", name="PV Voltage2"),
    NeovoltaVoltageDescription(key="grid_voltage_rsuvab", name="Grid Voltage RS/UV/AB"),
    NeovoltaFrequencyDescription(key="frequency1", name="Frequency1"),
    NeovoltaFrequencyDescription(key="frequency2", name="Frequency2"),
    NeovoltaFrequencyDescription(key="frequency3", name="Frequency3"),
    NeovoltaFrequencyDescription(key="frequency4", name="Frequency4"),
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
