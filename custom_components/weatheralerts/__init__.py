"""Custom weatheralerts integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor"]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:  # type: ignore[override]
    """Set up via YAML (now deprecated)."""
    if DOMAIN in config:
        _LOGGER.warning(
            "YAML configuration for Weather Alerts is deprecated; please remove it and use the UI config flow instead."
        )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:  # type: ignore[override]
    """Set up Weather Alerts from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Forward to platform(s)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:  # type: ignore[override]
    """Unload a Weather Alerts config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok and entry.entry_id in hass.data.get(DOMAIN, {}):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

