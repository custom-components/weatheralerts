"""Frontend support for the Weather Alerts integration."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from homeassistant.components.http import StaticPathConfig
from homeassistant.components.lovelace.const import LOVELACE_DATA, MODE_STORAGE
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import CoreState, HomeAssistant
from homeassistant.helpers.event import async_call_later

from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)

URL_BASE = f"/{DOMAIN}_static"
CARD_FILENAME = "weatheralerts-alert-card.js"
CARD_URL = f"{URL_BASE}/{CARD_FILENAME}"
FRONTEND_DIR = Path(__file__).parent
MANIFEST_PATH = FRONTEND_DIR.parent / "manifest.json"
RESOURCE_TYPE = "module"
RESOURCE_RETRY_SECONDS = 5
RESOURCE_RETRY_LIMIT = 12


def _integration_version() -> str:
    """Return the integration version from manifest.json."""
    try:
        with MANIFEST_PATH.open(encoding="utf-8") as manifest_file:
            return str(json.load(manifest_file).get("version", "0.0.0"))
    except (OSError, json.JSONDecodeError):
        _LOGGER.debug("weatheralerts: unable to read manifest version", exc_info=True)
        return "0.0.0"


INTEGRATION_VERSION = _integration_version()
CARD_RESOURCE_URL = f"{CARD_URL}?v={INTEGRATION_VERSION}"


async def async_register_frontend(hass: HomeAssistant) -> None:
    """Register the bundled WeatherAlerts Alert Card static path and Lovelace resource."""
    await _async_register_static_path(hass)
    _async_schedule_resource_registration(hass)


async def _async_register_static_path(hass: HomeAssistant) -> None:
    """Register the static HTTP path for the bundled frontend files."""
    flag = f"{DOMAIN}_frontend_static_path_registered"
    if hass.data.get(flag):
        return

    try:
        await hass.http.async_register_static_paths(
            [StaticPathConfig(URL_BASE, str(FRONTEND_DIR), False)]
        )
        _LOGGER.debug(
            "weatheralerts: registered frontend static path %s -> %s",
            URL_BASE,
            FRONTEND_DIR,
        )
    except RuntimeError:
        _LOGGER.debug("weatheralerts: frontend static path already registered: %s", URL_BASE)

    hass.data[flag] = True


def _async_schedule_resource_registration(hass: HomeAssistant) -> None:
    """Schedule Lovelace resource registration once per Home Assistant run."""
    flag = f"{DOMAIN}_frontend_resource_registration_scheduled"
    if hass.data.get(flag):
        return

    hass.data[flag] = True

    async def _register_when_ready(_now: Any | None = None) -> None:
        await _async_register_lovelace_resource(hass, attempt=1)

    if hass.state == CoreState.running:
        hass.async_create_task(_register_when_ready())
    else:
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, _register_when_ready)


async def _async_register_lovelace_resource(
    hass: HomeAssistant,
    attempt: int,
) -> None:
    """Add or update the WeatherAlerts Alert Card dashboard resource."""
    lovelace = hass.data.get(LOVELACE_DATA) or hass.data.get("lovelace")
    if lovelace is None or not hasattr(lovelace, "resources"):
        await _async_retry_resource_registration(hass, attempt, "Lovelace is not ready")
        return

    resource_mode = getattr(lovelace, "resource_mode", getattr(lovelace, "mode", None))
    if resource_mode != MODE_STORAGE:
        _LOGGER.debug(
            "weatheralerts: Lovelace is not in storage mode; dashboard resource must be added manually"
        )
        return

    resources = lovelace.resources

    # Important: older/newer HA builds can lazily load Lovelace resources. Calling
    # async_items() or async_create_item() before resources are loaded can act on an
    # empty collection, so explicitly load before reading or writing.
    if not getattr(resources, "loaded", False):
        async_load = getattr(resources, "async_load", None)
        if async_load is None:
            await _async_retry_resource_registration(
                hass,
                attempt,
                "Lovelace resources are not loaded and async_load is unavailable",
            )
            return
        await async_load()

    existing_resource = None
    for resource in resources.async_items():
        if _resource_path(resource.get("url", "")) == CARD_URL:
            existing_resource = resource
            break

    if existing_resource is None:
        _LOGGER.info(
            "weatheralerts: adding dashboard resource for WeatherAlerts Alert Card: %s",
            CARD_RESOURCE_URL,
        )
        await resources.async_create_item(
            {
                "res_type": RESOURCE_TYPE,
                "url": CARD_RESOURCE_URL,
            }
        )
        return

    if (
        existing_resource.get("res_type") != RESOURCE_TYPE
        or existing_resource.get("url") != CARD_RESOURCE_URL
    ):
        _LOGGER.info(
            "weatheralerts: updating dashboard resource for WeatherAlerts Alert Card: %s",
            CARD_RESOURCE_URL,
        )
        await resources.async_update_item(
            existing_resource["id"],
            {
                "res_type": RESOURCE_TYPE,
                "url": CARD_RESOURCE_URL,
            },
        )
        return

    _LOGGER.debug(
        "weatheralerts: dashboard resource already registered for WeatherAlerts Alert Card"
    )


async def _async_retry_resource_registration(
    hass: HomeAssistant,
    attempt: int,
    reason: str,
) -> None:
    """Retry resource registration for a short time while Lovelace starts."""
    if attempt >= RESOURCE_RETRY_LIMIT:
        _LOGGER.warning(
            "weatheralerts: could not auto-add WeatherAlerts Alert Card dashboard resource after %s attempts: %s",
            attempt,
            reason,
        )
        return

    _LOGGER.debug(
        "weatheralerts: dashboard resource registration attempt %s/%s delayed: %s",
        attempt,
        RESOURCE_RETRY_LIMIT,
        reason,
    )

    async def _retry(_now: Any) -> None:
        await _async_register_lovelace_resource(hass, attempt=attempt + 1)

    async_call_later(hass, RESOURCE_RETRY_SECONDS, _retry)


def _resource_path(url: str) -> str:
    """Return a resource URL without query parameters."""
    return url.split("?", 1)[0]
