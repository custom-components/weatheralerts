"""Custom weatheralerts integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import config_validation as cv
from homeassistant import config_entries

from .const import (
    DOMAIN,
    CONF_ZONE,
    CONF_COUNTY,
    CONF_ZONE_NAME,
    CONF_NAME,
    CONF_ENTITY_NAME,
    CONF_MARINE_ZONES,
    CONF_UPDATE_INTERVAL,
    CONF_API_TIMEOUT,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_API_TIMEOUT,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor"]
CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    _LOGGER.debug("weatheralerts: async_setup called")
    entries = hass.config_entries.async_entries(DOMAIN)
    if entries:
        _LOGGER.debug("weatheralerts: skipping migration, existing entries found")
        return True

    sensor_conf = config.get("sensor")
    if not sensor_conf:
        return True

    yaml_sensors = (
        [sensor_conf] if isinstance(sensor_conf, dict)
        else sensor_conf if isinstance(sensor_conf, list)
        else []
    )
    for conf in yaml_sensors:
        if not isinstance(conf, dict) or conf.get("platform") != DOMAIN:
            continue

        # Extract old keys
        state = conf.get("state", "").upper()
        zone = conf.get("zone", "")
        county = conf.get("county", "")

        # Convert to new codes with zero-padding as needed
        zc = f"{state}Z{str(zone).zfill(3)}" if state and zone else ""
        cc = f"{state}C{str(county).zfill(3)}" if state and county else ""

        _LOGGER.warning(
            "weatheralerts: Migrating legacy YAML config to config entries (state=%s, zone=%s, county=%s) -> (zone=%s, county=%s)",
            state, zone, county, zc, cc,
        )

        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN,
                context={"source": config_entries.SOURCE_IMPORT},
                data={
                    CONF_ZONE: zc,
                    CONF_COUNTY: cc,
                },
            )
        )
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("weatheralerts: async_setup_entry called for %s", entry.entry_id)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    hass.data.setdefault(DOMAIN, {})
    _LOGGER.debug("weatheralerts: forwarding setup to platforms: %s", PLATFORMS)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.debug("weatheralerts: platform setup complete")

    return True

async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    _LOGGER.debug("weatheralerts: _async_update_listener triggered for %s", entry.entry_id)

    # Gather current zone and naming options, respecting blank (deletion) values
    if CONF_ZONE in entry.options:
        zone = entry.options[CONF_ZONE].strip()
    else:
        zone = entry.data.get(CONF_ZONE, "").strip()

    if CONF_COUNTY in entry.options:
        county = entry.options[CONF_COUNTY].strip()
    else:
        county = entry.data.get(CONF_COUNTY, "").strip()

    if CONF_MARINE_ZONES in entry.options:
        marine_zones = entry.options[CONF_MARINE_ZONES].strip()
    else:
        marine_zones = entry.data.get(CONF_MARINE_ZONES, "").strip()

    if CONF_NAME in entry.options:
        name = entry.options[CONF_NAME].strip()
    else:
        name = entry.data.get(CONF_NAME, "").strip()

    if CONF_ZONE_NAME in entry.options:
        name = entry.options[CONF_ZONE_NAME].strip()
    else:
        name = entry.data.get(CONF_ZONE_NAME, "").strip()

    if CONF_ENTITY_NAME in entry.options:
        entity_name = entry.options[CONF_ENTITY_NAME].strip()
    else:
        entity_name = entry.data.get(CONF_ENTITY_NAME, "").strip()

    update_interval = int(entry.options.get(CONF_UPDATE_INTERVAL, entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)))
    api_timeout = int(entry.options.get(CONF_API_TIMEOUT, entry.data.get(CONF_API_TIMEOUT, DEFAULT_API_TIMEOUT)))

    # Rebuild feed_id and title
    parts = [zone] if zone else []
    if county:
        parts.append(county)
    if marine_zones:
        parts.extend(z.strip() for z in marine_zones.split(",") if z.strip())
    feed_id = ",".join(parts)
    title = name or f"NWS {feed_id}"

    # Build the new static data dict
    new_data: dict[str, str] = {
        CONF_ZONE: zone,
        CONF_COUNTY: county,
        CONF_MARINE_ZONES: marine_zones,
        CONF_ZONE_NAME: zone_name,
        CONF_UPDATE_INTERVAL: update_interval,
        CONF_API_TIMEOUT: api_timeout,
    }
    if name:
        new_data[CONF_NAME] = name
    if entity_name:
        new_data[CONF_ENTITY_NAME] = entity_name

    # Merge into options (preserve icons)
    new_options = dict(entry.options)
    new_options.update({
        CONF_ZONE: zone,
        CONF_COUNTY: county,
        CONF_MARINE_ZONES: marine_zones,
        CONF_ZONE_NAME: zone_name,
        CONF_UPDATE_INTERVAL: update_interval,
        CONF_API_TIMEOUT: api_timeout,
    })
    if name:
        new_options[CONF_NAME] = name
    if entity_name:
        new_options[CONF_ENTITY_NAME] = entity_name

    # Only update if something really changed
    if entry.data != new_data or entry.options != new_options or entry.title != title:
        _LOGGER.debug("weatheralerts: Updating entry data/options/title")
        hass.config_entries.async_update_entry(
            entry,
            data=new_data,
            options=new_options,
            title=title,
        )
        await hass.config_entries.async_reload(entry.entry_id)
    else:
        _LOGGER.debug("weatheralerts: No changes detected; skipping reload")

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("weatheralerts: async_unload_entry called for %s", entry.entry_id)
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
        _LOGGER.debug("weatheralerts: entry removed from hass.data")
    return unload_ok

async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.info("weatheralerts: migrating entry %s", entry.title)
    data = dict(entry.data)
    version = entry.version or 1
    migrated = False

    if version < 2:
        state = data.pop("state", None)
        zone = data.get(CONF_ZONE)
        county = data.get(CONF_COUNTY)
        if state and zone and isinstance(zone, (str, int)) and len(str(zone)) <= 3:
            new_zone = f"{state.upper()}Z{str(zone).zfill(3)}"
            data[CONF_ZONE] = new_zone
            _LOGGER.info("weatheralerts: migrated zone to %s", new_zone)
            migrated = True
        if state and county and isinstance(county, (str, int)) and len(str(county)) <= 3:
            new_county = f"{state.upper()}C{str(county).zfill(3)}"
            data[CONF_COUNTY] = new_county
            _LOGGER.info("weatheralerts: migrated county to %s", new_county)
            migrated = True

    if migrated:
        hass.config_entries.async_update_entry(entry, data=data, version=2)
        _LOGGER.info("weatheralerts: migration complete for %s", entry.title)
    else:
        _LOGGER.info("weatheralerts: no migration needed for %s", entry.title)
    return True
