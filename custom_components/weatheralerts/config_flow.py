"""Config flow for weatheralerts integration."""
from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers import selector

from .sensor import CONF_STATE, CONF_ZONE, CONF_COUNTY  # reuse existing constants
from .const import DOMAIN  # type: ignore

_LOGGER = logging.getLogger(__name__)


class WeatheralertsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Weather Alerts."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None):  # type: ignore[override]
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Basic validation – mimic legacy YAML checks
            state: str = user_input[CONF_STATE].strip().upper()
            zone: str = user_input[CONF_ZONE].strip()
            county: str = user_input.get(CONF_COUNTY, "").strip()

            # Validate input sizes
            if len(state) != 2:
                errors[CONF_STATE] = "invalid_state"
            elif not zone.isdigit() or len(zone) > 3 or len(zone) == 0:
                errors[CONF_ZONE] = "invalid_zone"
            elif county and (not county.isdigit() or len(county) > 3):
                errors[CONF_COUNTY] = "invalid_county"
            else:
                # Build unique feed id similar to sensor implementation
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
