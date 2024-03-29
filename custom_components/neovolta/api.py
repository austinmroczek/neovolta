"""NeoVolta API Client."""
from __future__ import annotations

import asyncio
import logging

import async_timeout
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ConnectionException, ModbusIOException
from pymodbus.pdu import ExceptionResponse
from pymodbus import pymodbus_apply_logging_config

# logging.getLogger("pymodbus.logging").setLevel(logging.DEBUG)
pymodbus_apply_logging_config()

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
        self._stats = {
            "async_get_data": 0,
            "get_value": 0,
            "TimeoutError": 0,
            "ConnectionException": 0,
            "ModbusIOException": 0,
            "Exception": 0,
            "isError": 0,
            "ExceptionResponse": 0,
            "tries": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
        }

        self._client = AsyncModbusTcpClient(
            host=self._host,
            port=self._port,
            close_comm_on_error=True,
            reconnect_delay=1000,
            retry_on_empty=True,
        )

    async def async_get_static_data(self) -> any:
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
        self._stats["async_get_data"] += 1

        if not self._static_data_loaded:
            await self.async_get_static_data()

        # grab register 0 to 99
        response = await self._get_value(0, 100)
        self.data["energy24"] = self._scaled_value(response[24], 0.1)
        self.data["energy65"] = self._scaled_value(response[65], 0.1)
        self.data["energy66"] = self._scaled_value(response[66], 0.1)
        self.data["energy68"] = self._scaled_value(response[68], 0.1)
        self.data["battery_charged_today"] = self._scaled_value(response[70], 0.1)
        self.data["battery_discharged_today"] = self._scaled_value(response[71], 0.1)
        self.data["battery_charged_cumulative"] = self._scaled_value(response[72], 0.1)
        self.data["battery_discharged_cumulative"] = self._scaled_value(
            response[74], 0.1
        )
        self.data["energy_from_grid_today"] = self._scaled_value(response[76], 0.1)
        self.data["energy_to_grid_today"] = self._scaled_value(response[77], 0.1)
        self.data["energy_from_grid_cumulative"] = self._scaled_value(response[78], 0.1)
        self.data["grid_frequency"] = self._scaled_value(response[79], 0.01)
        self.data["energy_to_grid_cumulative"] = self._scaled_value(response[81], 0.1)
        self.data["energy_consumed_today"] = self._scaled_value(response[84], 0.1)
        self.data["energy_consumed_cumulative"] = self._scaled_value(response[85], 0.1)
        self.data["energy87"] = self._scaled_value(response[87], 0.1)
        self.data["energy96"] = self._scaled_value(response[96], 0.1)

        # grab register 100 to 199
        response = await self._get_value(100, 100)
        self.data["daily_generation"] = self._scaled_value(response[8], 0.1)
        self.data["pv_voltage1"] = self._scaled_value(response[9], 0.1)
        self.data["pv_voltage2"] = self._scaled_value(response[11], 0.1)
        self.data["battery_voltage1"] = self._scaled_value(response[26], 0.01)
        self.data["energy131"] = self._scaled_value(response[31], 0.1)
        self.data["current132"] = self._scaled_value(response[32], 0.01)
        self.data["current133"] = self._scaled_value(response[33], 0.01)
        self.data["grid_voltage_rua"] = self._scaled_value(response[38], 0.1)
        self.data["grid_voltage_svb"] = self._scaled_value(response[39], 0.1)
        self.data["grid_voltage_rsuvab"] = self._scaled_value(response[40], 0.1)
        self.data["battery_voltage2"] = self._scaled_value(response[43], 0.01)
        self.data["voltage148"] = self._scaled_value(response[48], 0.1)
        self.data["voltage149"] = self._scaled_value(response[49], 0.1)
        self.data["voltage150"] = self._scaled_value(response[50], 0.1)
        self.data["voltage151"] = self._scaled_value(response[51], 0.1)
        self.data["voltage152"] = self._scaled_value(response[52], 0.1)
        self.data["voltage153"] = self._scaled_value(response[53], 0.1)
        self.data["voltage154"] = self._scaled_value(response[54], 0.1)
        self.data["voltage155"] = self._scaled_value(response[55], 0.1)
        self.data["voltage156"] = self._scaled_value(response[56], 0.1)
        self.data["voltage157"] = self._scaled_value(response[57], 0.1)
        self.data["voltage158"] = self._scaled_value(response[58], 0.1)
        self.data["grid_current_rua"] = self._scaled_value(response[60], 0.01)
        self.data["grid_current_svb"] = self._scaled_value(response[61], 0.01)
        self.data["meter_ac_current_a"] = self._scaled_value(response[62], 0.01)
        self.data["meter_ac_current_b"] = self._scaled_value(response[63], 0.01)
        self.data["current164"] = self._scaled_value(response[64], 0.01)
        self.data["current165"] = self._scaled_value(response[65], 0.01)
        self.data["current166"] = self._scaled_value(response[66], 0.01)
        self.data["current176"] = self._scaled_value(response[76], 0.01)
        self.data["current177"] = self._scaled_value(response[77], 0.01)
        self.data["current178"] = self._scaled_value(response[78], 0.01)
        self.data["current179"] = self._scaled_value(response[79], 0.01)
        self.data["current180"] = self._scaled_value(response[80], 0.01)
        self.data["voltage181"] = self._scaled_value(response[81], 0.1)
        self.data["voltage182"] = self._scaled_value(response[82], 0.1)

        self.data["battery_voltage3"] = self._scaled_value(response[83], 0.01)
        self.data["battery_total"] = self._scaled_value(response[84], 1)
        self.data["current185"] = self._scaled_value(response[85], 0.01)
        self.data["frequency2"] = self._scaled_value(response[92], 0.01)
        self.data["frequency3"] = self._scaled_value(response[93], 0.01)

        # grab register 300 to 399
        response = await self._get_value(300, 100)
        self.data["current314"] = self._scaled_value(response[14], 0.1)
        self.data["current315"] = self._scaled_value(response[15], 0.1)
        self.data["battery_tbd"] = self._scaled_value(response[16], 1)
        self.data["bms_voltage"] = self._scaled_value(response[17], 0.01)
        self.data["voltage319"] = self._scaled_value(response[19], 0.1)
        self.data["frequency4"] = self._scaled_value(response[44], 0.01)

        await self._calculate_stats()

    async def _get_value(
        self,
        address: int,
        size: int,
        unit: int = 1,
        tries=1,
    ) -> any:
        """Get information from the API."""
        self._stats["get_value"] += 1
        self._stats["tries"][tries] += 1
        if tries >= 10:
            await self._calculate_stats()
            raise NeovoltaApiClientCommunicationError(
                f"Timeout fetching NeoVolta information",
            )

        if tries > 1:
            _LOGGER.debug(f"Neovolta re-try # {tries} for register {address}")
            # await asyncio.sleep(tries)
            await asyncio.sleep(5)

        try:
            async with async_timeout.timeout(30):
                response = await self._client.read_holding_registers(
                    address=address, count=size, slave=unit
                )

        except asyncio.TimeoutError as exception:
            _LOGGER.debug(f"Neovolta timeout: {exception}")
            self._stats["TimeoutError"] += 1
            return await self._get_value(address, size, unit, tries + 1)
        except ConnectionException as exception:
            _LOGGER.debug(f"Neovolta connection problem: {exception}")
            self._stats["ConnectionException"] += 1
            return await self._get_value(address, size, unit, tries + 1)
        except ModbusIOException as exception:
            _LOGGER.debug(f"Neovolta ModbusIOException: {exception.message}")
            self._stats["ModbusIOException"] += 1
            self._client.close()
            return await self._get_value(address, size, unit, tries + 1)
        except Exception as exception:  # pylint: disable=broad-except
            self._stats["Exception"] += 1
            await self._calculate_stats()
            raise NeovoltaApiClientError(
                "Something really wrong happened!"
            ) from exception

        if response.isError():
            self._stats["isError"] += 1
            _LOGGER.debug(f"NeoVolta MODBUS response error: {response}")
            return await self._get_value(address, size, unit, tries + 1)

        if isinstance(response, ExceptionResponse):
            self._stats["ExceptionResponse"] += 1
            _LOGGER.debug(f"NeoVolta device rejected MODBUS request: {response}")
            return await self._get_value(address, size, unit, tries + 1)

        return response.registers

    async def _calculate_stats(self):
        """Calculate stats."""

        stats = (
            f"\nNeoVolta Integration Debug STATS:\n"
            f"async_get_data {self._stats['async_get_data']}\t"
            f"get_value {self._stats['get_value']}\n"
            f"TimeoutError {self._stats['TimeoutError']}\t"
            f"ConnectionException {self._stats['ConnectionException']}\t"
            f"ModbusIOException {self._stats['ModbusIOException']}\n"
            f"Exception {self._stats['Exception']}\t"
            f"isError {self._stats['isError']}\t"
            f"ExceptionResponse {self._stats['ExceptionResponse']}\n"
        )

        tries = "tries - "
        i = 1
        for i in range(1, 11):
            tries = tries + f"{i}: {self._stats['tries'][i]}\t"

        stats = stats + tries

        _LOGGER.debug(stats)
