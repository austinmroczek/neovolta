"""Adds config flow for Neovolta."""
from __future__ import annotations

import ipaddress
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers import selector

from .api import (
    NeovoltaApiClient,
    NeovoltaApiClientAuthenticationError,
    NeovoltaApiClientCommunicationError,
    NeovoltaApiClientError,
)
from .const import DOMAIN, LOGGER


class NeovoltaFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Neovolta."""

    VERSION = 1

    def __init__(self):
        """Initialize."""
        self._client = None

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    host=user_input[CONF_HOST],
                    port=user_input[CONF_PORT],
                )
            except NeovoltaApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except NeovoltaApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except NeovoltaApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            except vol.Invalid as exception:
                LOGGER.exception(exception)
                _errors["base"] = "address"
            else:
                return self.async_create_entry(
                    title=self._client.data["serial_number"],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HOST,
                        default=(user_input or {}).get(CONF_HOST),
                        description="Neovolta IP Address",
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(
                        CONF_PORT,
                        default=(user_input or {}).get(CONF_PORT, "8899"),
                        description="Neovolta Port",
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.NUMBER
                        ),
                    ),
                }
            ),
            errors=_errors,
        )

    async def _test_credentials(self, host: str, port: str) -> None:
        """Validate credentials."""
        self._ip_v4_validator(host)

        self._client = NeovoltaApiClient(
            host=host,
            port=port,
        )
        await self._client.async_get_static_data()

    def _ip_v4_validator(self, value: Any) -> str:
        """Validate that value is parsable as IPv4 address."""
        try:
            address = ipaddress.IPv4Address(value)
        except ipaddress.AddressValueError as ex:
            raise vol.Invalid(
                f"value '{value}' is not a valid IPv4 address: {ex}"
            ) from ex
        return str(address)
