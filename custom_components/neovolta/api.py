"""NeoVolta API Client."""
from __future__ import annotations

import asyncio
import async_timeout
import logging

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ConnectionException

_LOGGER = logging.getLogger(__name__)


class NeovoltaApiClientError(Exception):
    """Exception to indicate a general API error."""


class NeovoltaApiClientCommunicationError(NeovoltaApiClientError):
    """Exception to indicate a communication error."""


class NeovoltaApiClientAuthenticationError(NeovoltaApiClientError):
    """Exception to indicate an authentication error."""


class NeovoltaApiClient:
    """Neovolta API Client."""

    def __init__(
        self,
        host: str = "0.0.0.0",
        port: str = "8899",
    ) -> None:
        """Initialize."""
        self._host = host
        self._port = port
        self._static_data_loaded = False
        self.data = {}

        self._client = AsyncModbusTcpClient(host=self._host, port=self._port)

    async def _async_get_static_data(self) -> any:
        """Get static data only once."""
        # serial number
        serial_number = ""
        response = await self._get_value(3, 5)
        for bits in response:
            serial_number += chr(bits >> 8) + chr(bits & 0xFF)
        self.data["serial_number"] = serial_number

        self._static_data_loaded = True

    def _scaled_value(self, value, scale=1) -> any:
        """Return a scaled value."""
        return float(value) * scale

    async def async_get_data(self) -> any:
        """Get data from the API."""
        if not self._static_data_loaded:
            await self._async_get_static_data()

        _LOGGER.debug("Neovolta starting async_get_data")

        # battery enegery today
        response = await self._get_value(70, 10)
        self.data["battery_charged_today"] = self._scaled_value(response[0], 0.1)
        self.data["battery_discharged_today"] = self._scaled_value(response[1], 0.1)
        self.data["battery_charged_cummulative"] = self._scaled_value(response[2], 0.1)
        # unusre if response[3] is anything useful
        self.data["battery_discharged_cummulative"] = self._scaled_value(
            response[4], 0.1
        )
        self.data["energy_from_grid_today"] = self._scaled_value(response[6], 0.1)
        self.data["energy_to_grid_today"] = self._scaled_value(response[7], 0.1)
        # 79: frequency TBD1
        self.data["frequency1"] = self._scaled_value(response[9], 0.01)

        response = await self._get_value(81, 5)
        # 81: energy to grid cummulative
        self.data["energy_to_grid_cummulative"] = self._scaled_value(response[0], 0.1)
        # 84: energy consumed today
        self.data["energy_consumed_today"] = self._scaled_value(response[3], 0.1)
        # 85: energy consumed cummulative
        self.data["energy_consumed_cummulative"] = self._scaled_value(response[4], 0.1)

        response = await self._get_value(109, 3)
        # 109/111: PV voltage
        self.data["pv_voltage1"] = self._scaled_value(response[0], 0.1)
        self.data["pv_voltage2"] = self._scaled_value(response[2], 0.1)

        response = await self._get_value(126, 1)
        # 126: battery voltage
        self.data["battery_voltage1"] = self._scaled_value(response[0], 0.01)

        response = await self._get_value(138, 3)
        # 138: grid voltage R/U/A
        self.data["grid_voltage_rua"] = self._scaled_value(response[0], 0.1)
        # 139: grid voltage S/V/B
        self.data["grid_voltage_svb"] = self._scaled_value(response[1], 0.1)
        # 140: grid voltage RS/UV/AB
        self.data["grid_voltage_rsuvab"] = self._scaled_value(response[2], 0.1)

        response = await self._get_value(143, 1)
        # 143: battery voltage
        self.data["battery_voltage2"] = self._scaled_value(response[0], 0.01)

        response = await self._get_value(183, 2)
        # 183: battery voltage
        self.data["battery_voltage3"] = self._scaled_value(response[0], 0.01)
        # 184: battery total %
        self.data["battery_total"] = self._scaled_value(response[1], 1)

        response = await self._get_value(192, 2)
        # 192: frequency TBD
        self.data["frequency2"] = self._scaled_value(response[0], 0.01)
        # 193: frequency TBD
        self.data["frequency3"] = self._scaled_value(response[1], 0.01)

        response = await self._get_value(316, 2)
        # 316: battery component TBD %
        self.data["battery_tbd"] = self._scaled_value(response[0], 1)
        # 317: battery voltage
        self.data["battery_voltage4"] = self._scaled_value(response[1], 0.01)

        _LOGGER.debug("Neovolta finish async_get_data")

    async def _get_value(
        self,
        address: int,
        size: int,
        unit: int = 1,
        tries=10,
    ) -> any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(30):
                if not self._client.connected:
                    _LOGGER.debug("Neovolta client connecting")
                    await self._client.connect()

                response = await self._client.read_holding_registers(
                    address=address, count=size, slave=unit
                )

                if response.isError():
                    _LOGGER.debug(f"response error: {response}")
                    _LOGGER.debug(f"Neovolta try # {tries}")
                    return await self._get_value(address, size, unit, tries - 1)

                return response.registers

        except asyncio.TimeoutError as exception:
            _LOGGER.debug(f"Neovolta timeout try # {tries} for addresss ({address})")
            if tries > 0:
                return await self._get_value(address, size, unit, tries - 1)
            raise NeovoltaApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except ConnectionException:
            _LOGGER.debug(f"Neovolta connectionException try # {tries}")
            return await self._get_value(address, size, unit, tries - 1)
        except Exception as exception:  # pylint: disable=broad-except
            raise NeovoltaApiClientError(
                "Something really wrong happened!"
            ) from exception
