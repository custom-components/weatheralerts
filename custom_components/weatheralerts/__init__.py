"""Custom weatheralerts integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant import config_entries

from .const import DOMAIN
from .sensor import CONF_STATE, CONF_ZONE, CONF_COUNTY

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor"]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:  # type: ignore[override]
    """Set up via YAML (now deprecated)."""
    # Migrate legacy YAML sensor platform configuration to UI config entries
    sensor_conf = config.get("sensor")
    if not sensor_conf:
        return True
    # Normalize to list
    if isinstance(sensor_conf, dict):
        yaml_sensors = [sensor_conf]
    elif isinstance(sensor_conf, list):
        yaml_sensors = sensor_conf
    else:
        return True

    for conf in yaml_sensors:
        if not isinstance(conf, dict) or conf.get("platform") != DOMAIN:
            continue
        _LOGGER.warning(
            "YAML configuration for Weather Alerts platform is deprecated; migrating to UI config entries"
        )
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN,
                context={"source": config_entries.SOURCE_IMPORT},
                data={
                    CONF_STATE: conf.get(CONF_STATE),
                    CONF_ZONE: conf.get(CONF_ZONE),
                    CONF_COUNTY: conf.get(CONF_COUNTY, ""),
                },
            )
        )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:  # type: ignore[override]
    """Set up Weather Alerts from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    # Register update listener to reload integration on options update
    entry.add_update_listener(_async_update_listener)
    # Forward to platform(s)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update to reload the integration and update title."""
    # Compute new title based on updated options
    state = entry.options.get(CONF_STATE, entry.data[CONF_STATE]).strip().upper()
    zone = entry.options.get(CONF_ZONE, entry.data[CONF_ZONE]).strip()
    county = entry.options.get(CONF_COUNTY, entry.data.get(CONF_COUNTY, "")).strip()
    zone_id = f"{state}Z{zone.zfill(3)}"
    if county:
        county_id = f"{state}C{county.zfill(3)}"
        feed_id = f"{zone_id},{county_id}"
    else:
        feed_id = zone_id
    title = f"NWS {feed_id}"
    hass.config_entries.async_update_entry(entry, title=title)
    # Reload integration to apply changes
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:  # type: ignore[override]
    """Unload a Weather Alerts config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok and entry.entry_id in hass.data.get(DOMAIN, {}):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

