"""Sensor platform for neovolta."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .const import DOMAIN
from .coordinator import NeovoltaDataUpdateCoordinatoror
from .entity import NeovoltaEntity

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="neovolta",
        name="Integration Sensor",
        icon="mdi:format-quote-close",
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

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        return self.coordinator.data.get("body")
