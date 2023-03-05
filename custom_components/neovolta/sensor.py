"""Sensor platform for neovolta."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
)

from .const import DOMAIN
from .coordinator import NeovoltaDataUpdateCoordinatoror
from .entity import NeovoltaEntity

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="battery_total",
        name="Battery Total",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="battery_tbd",
        name="Battery TBD",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="battery_charged_today",
        name="Battery Charged Today",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement="kWh",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="battery_discharged_today",
        name="Battery Discharged Today",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement="kWh",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="energy_from_grid_today",
        name="Energy From Grid Today",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement="kWh",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="energy_to_grid_today",
        name="Energy To Grid Today",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement="kWh",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="battery_charged_cummulative",
        name="Battery Charged Cummulative",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement="kWh",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="battery_discharged_cummulative",
        name="Battery Discharged Cummulative",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement="kWh",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="battery_voltage1",
        name="Battery Voltage TBD1",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="battery_voltage2",
        name="Battery Voltage TBD2",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="battery_voltage3",
        name="Battery Voltage TBD3",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="battery_voltage4",
        name="Battery Voltage TBD4",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="energy_to_grid_cummulative",
        name="Energy to Grid Cummulative",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement="kWh",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="energy_consumed_today",
        name="Energy Consumed Today",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement="kWh",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="energy_consumed_cummulative",
        name="Energy Consumed Cummulative",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement="kWh",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="grid_voltage_rua",
        name="Grid Voltage R/U/A",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="grid_voltage_svb",
        name="Grid Voltage S/V/B",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="grid_voltage_rsuvab",
        name="Grid Voltage RS/UV/AB",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="frequency1",
        name="Frequency1",
        device_class=SensorDeviceClass.FREQUENCY,
        native_unit_of_measurement="Hz",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="frequency2",
        name="Frequency2",
        device_class=SensorDeviceClass.FREQUENCY,
        native_unit_of_measurement="Hz",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="frequency3",
        name="Frequency3",
        device_class=SensorDeviceClass.FREQUENCY,
        native_unit_of_measurement="Hz",
        state_class=SensorStateClass.MEASUREMENT,
    ),
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
