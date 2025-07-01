"""Config flow for weatheralerts integration."""
from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant import config_entries

from .sensor import CONF_STATE, CONF_ZONE, CONF_COUNTY
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class WeatheralertsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Weather Alerts."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None):  # type: ignore[override]
        """Handle the initial configuration step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            state = user_input[CONF_STATE].strip().upper()
            zone = user_input[CONF_ZONE].strip()
            county = user_input.get(CONF_COUNTY, "").strip()

            # Validate input sizes
            if len(state) != 2:
                errors[CONF_STATE] = "invalid_state"
            elif not zone.isdigit() or len(zone) == 0 or len(zone) > 3:
                errors[CONF_ZONE] = "invalid_zone"
            elif county and (not county.isdigit() or len(county) > 3):
                errors[CONF_COUNTY] = "invalid_county"
            else:
                zone_id = f"{state}Z{zone.zfill(3)}"
                if county:
                    county_id = f"{state}C{county.zfill(3)}"
                    feed_id = f"{zone_id},{county_id}"
                else:
                    feed_id = zone_id

                await self.async_set_unique_id(feed_id.replace(",", ""))
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"NWS {feed_id}",
                    data={
                        CONF_STATE: state,
                        CONF_ZONE: zone,
                        CONF_COUNTY: county,
                    },
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_STATE): str,
                vol.Required(CONF_ZONE): str,
                vol.Optional(CONF_COUNTY, default=""): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)


    async def async_step_import(self, import_data: dict):
        """Import a config entry from YAML."""
        # Delegate to async_step_user for validation and entry creation
        return await self.async_step_user(import_data)

    @staticmethod
    def async_get_options_flow(config_entry):  # type: ignore[override]
        """Get the options flow for this handler."""
        return WeatheralertsOptionsFlow(config_entry)

class WeatheralertsOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Weather Alerts."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict | None = None):  # type: ignore[override]
        """Manage the options."""
        errors: dict[str, str] = {}
        if user_input is not None:
            state = user_input[CONF_STATE].strip().upper()
            zone = user_input[CONF_ZONE].strip()
            county = user_input.get(CONF_COUNTY, "").strip()

            # Validate input sizes
            if len(state) != 2:
                errors[CONF_STATE] = "invalid_state"
            elif not zone.isdigit() or len(zone) == 0 or len(zone) > 3:
                errors[CONF_ZONE] = "invalid_zone"
            elif county and (not county.isdigit() or len(county) > 3):
                errors[CONF_COUNTY] = "invalid_county"
            else:
                return self.async_create_entry(title="", data={
                    CONF_STATE: state,
                    CONF_ZONE: zone,
                    CONF_COUNTY: county,
                })
        data_schema = vol.Schema(
            {
                vol.Required(CONF_STATE, default=self.config_entry.options.get(CONF_STATE, self.config_entry.data[CONF_STATE])): str,
                vol.Required(CONF_ZONE, default=self.config_entry.options.get(CONF_ZONE, self.config_entry.data[CONF_ZONE])): str,
                vol.Required(CONF_COUNTY, default=self.config_entry.options.get(CONF_COUNTY, self.config_entry.data.get(CONF_COUNTY, ""))): str,
            }
        )
        return self.async_show_form(step_id="init", data_schema=data_schema, errors=errors)
