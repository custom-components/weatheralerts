"""Config flow for weatheralerts integration."""
from __future__ import annotations

import logging
import voluptuous as vol
import async_timeout
import re
import json

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers import translation

from .const import (
    DOMAIN,
    CONF_ZONE,
    CONF_COUNTY,
    CONF_ZONE_NAME,
    CONF_NAME,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_ENTITY_NAME,
    CONF_MARINE_ZONES,
    CONF_UPDATE_INTERVAL,
    CONF_API_TIMEOUT,
    CONF_EVENT_ICONS,
    CONF_DEFAULT_ICON,
    CONF_DEDUPLICATE_ALERTS,
    ALERTS_API,
    POINTS_API,
    ZONE_API,
    COUNTY_API,
    HEADERS,
    NWS_CODE_REGEX,
    MARINE_API,
    DEFAULT_EVENT_ICONS,
    DEFAULT_EVENT_ICON,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_API_TIMEOUT,
    MIN_UPDATE_INTERVAL,
    MAX_UPDATE_INTERVAL,
    MIN_API_TIMEOUT,
    MAX_API_TIMEOUT,
    TIMEOUT_BUFFER,
    DEFAULT_DEDUPLICATE_ALERTS,
)

_LOGGER = logging.getLogger(__name__)


def _clean_for_entity_id(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"[^a-z0-9_]", "", re.sub(r"[-\s,]+", "_", text.lower())).strip("_")

async def _get_friendly_error(hass, key):
    """Return the user-friendly error message for the given key using en.json translation."""
    # Fetch English translations for your integration
    translations = await translation.async_get_translations(
        hass, "en", f"component.{DOMAIN}"
    )
    # Path for config flow errors in translations is: config.error.<key>
    error_path = f"config.error.{key}"
    return translations.get(error_path, key)

async def _get_zone_name(session, zone):
    """Fetch the human-readable name of a public-zone code (or “” on failure)."""
    try:
        async with async_timeout.timeout(20):
            resp = await session.get(ZONE_API.format(zone), headers=HEADERS)
            if resp.status == 200:
                return (await resp.json()).get("properties", {}).get("name", "")
    except Exception as ex:
        _LOGGER.debug("Failed to fetch zone name: %s", ex)
    return ""

async def _validate_zone_api(hass, zone, county, marine_zones, errors):
    session = async_get_clientsession(hass)
    try:
        async with async_timeout.timeout(20):
            resp = await session.get(ZONE_API.format(zone), headers=HEADERS)
            if resp.status == 404:
                marine_resp = await session.get(MARINE_API.format(zone), headers=HEADERS)
                if marine_resp.status == 404:
                    errors["zone"] = "invalid_zone"
                    errors["base"] = f"Invalid zone code: {zone}"
                    return False
            elif resp.status != 200:
                errors["base"] = "api_outage"
                return False
    except Exception:
        errors["base"] = "api_outage"
        return False
    if county:
        try:
            async with async_timeout.timeout(20):
                resp = await session.get(COUNTY_API.format(county), headers=HEADERS)
                if resp.status == 404:
                    errors["county"] = "invalid_county"
                    errors["base"] = f"Invalid county code: {county}"
                    return False
                elif resp.status != 200:
                    errors["base"] = "api_outage"
                    return False
        except Exception:
            errors["base"] = "api_outage"
            return False
    for m in marine_zones.split(","):
        m = m.strip()
        if not m:
            continue
        try:
            async with async_timeout.timeout(20):
                resp = await session.get(MARINE_API.format(m), headers=HEADERS)
                if resp.status == 404:
                    # Try as zone if not found as marine
                    zone_resp = await session.get(ZONE_API.format(m), headers=HEADERS)
                    if zone_resp.status == 404:
                        errors["marine_zones"] = "invalid_marine"
                        errors["base"] = f"Invalid marine_zones code: {m}"
                        return False
                    elif zone_resp.status != 200:
                        errors["base"] = "api_outage"
                        return False
                elif resp.status != 200:
                    errors["base"] = "api_outage"
                    return False
        except Exception:
            errors["base"] = "api_outage"
            return False
    return True


class WeatheralertsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Weather Alerts."""

    VERSION = 2

    def __init__(self):
        self._lat = None
        self._lon = None
        self._parsed_zone = None
        self._parsed_county = None
        self._zone = None
        self._county = None
        self._marine = None

    async def async_step_user(self, user_input=None):
        errors = {}
        zone_home = self.hass.states.get("zone.home")
        default_lat = str(zone_home.attributes.get("latitude", "")) if zone_home else ""
        default_lon = str(zone_home.attributes.get("longitude", "")) if zone_home else ""
        schema = vol.Schema({
            vol.Optional(CONF_LATITUDE, default=default_lat): str,
            vol.Optional(CONF_LONGITUDE, default=default_lon): str,
        })

        if user_input:
            lat = user_input[CONF_LATITUDE].strip()
            lon = user_input[CONF_LONGITUDE].strip()
            self._lat, self._lon = lat, lon

            if not lat or not lon:
                return await self.async_step_zone(None)

            try:
                float(lat)
                float(lon)
            except ValueError:
                friendly_error = await _get_friendly_error(self.hass, "invalid_latlon")
                _LOGGER.error(
                    "Invalid latitude/longitude: lat=%s, lon=%s - Error: %s",
                    lat, lon, friendly_error
                )
                errors["base"] = "invalid_latlon"
            else:
                session = async_get_clientsession(self.hass)
                async with async_timeout.timeout(20):
                    resp = await session.get(POINTS_API.format(lat, lon), headers=HEADERS)
                    code = resp.status
                    # If not 200 and not 404, this is an API outage.
                    if code != 200 and code != 404:
                        friendly_error = await _get_friendly_error(self.hass, "api_outage")
                        _LOGGER.error(
                            "API outage for lat=%s, lon=%s - HTTP code: %s, error: %s",
                            lat, lon, code, friendly_error
                        )
                        errors["base"] = "api_outage"
                    # If 404, check JSON
                    elif code == 404:
                        try:
                            data = await resp.json()
                        except Exception:
                            data = None
                        # If no data or no status key in JSON, unknown error
                        if not data or not isinstance(data, dict) or "status" not in data:
                            friendly_error = await _get_friendly_error(self.hass, "unknown_error")
                            _LOGGER.error(
                                "404 error for lat=%s, lon=%s - HTTP code: 404, error: %s (no valid JSON/status)",
                                lat, lon, friendly_error
                            )
                            errors["base"] = "unknown_error"
                        else:
                            # Continue with rest of JSON logic
                            status = data.get("status")
                            err_type = data.get("type", "")
                            if status == 404 and "InvalidPoint" in err_type:
                                friendly_error = await _get_friendly_error(self.hass, "invalid_point")
                                _LOGGER.error(
                                    "InvalidPoint error for lat=%s, lon=%s - HTTP code: %s, error: %s",
                                    lat, lon, code, friendly_error
                                )
                                errors["base"] = "invalid_point"
                            elif status is not None and status == 404 and "InvalidPoint" not in err_type:
                                title = data.get("title", "Unknown Error")
                                msg = f"{status} - {title} (Out-of-bounds?)"
                                _LOGGER.error(
                                    "API error for lat=%s, lon=%s - HTTP code: %s, error: %s",
                                    lat, lon, code, msg
                                )
                                errors["base"] = msg
                            elif status is not None and status != 404:
                                title = data.get("title", "Unknown Error")
                                msg = f"{status} - {title}"
                                _LOGGER.error(
                                    "API error for lat=%s, lon=%s - HTTP code: %s, error: %s",
                                    lat, lon, code, msg
                                )
                                errors["base"] = msg
                            else:
                                props = data.get("properties", {})
                                self._parsed_zone = props.get("forecastZone", "").split("/")[-1] or ""
                                self._parsed_county = props.get("county", "").split("/")[-1] or ""
                                return await self.async_step_zone(None)
                    # If 200, normal processing
                    else:
                        data = await resp.json()
                        if isinstance(data, dict):
                            status = data.get("status")
                            err_type = data.get("type", "")
                            if status == 404 and "InvalidPoint" in err_type:
                                friendly_error = await _get_friendly_error(self.hass, "invalid_point")
                                _LOGGER.error(
                                    "InvalidPoint error for lat=%s, lon=%s - HTTP code: %s, error: %s",
                                    lat, lon, code, friendly_error
                                )
                                errors["base"] = "invalid_point"
                            elif status is not None and status != 404:
                                title = data.get("title", "Unknown Error")
                                msg = f"{status} - {title}"
                                _LOGGER.error(
                                    "API error for lat=%s, lon=%s - HTTP code: %s, error: %s",
                                    lat, lon, code, msg
                                )
                                errors["base"] = msg
                            elif status is not None and status == 404 and "InvalidPoint" not in err_type:
                                title = data.get("title", "Unknown Error")
                                msg = f"{status} - {title}  (Out-of-bounds?)"
                                _LOGGER.error(
                                    "API error for lat=%s, lon=%s - HTTP code: %s, error: %s",
                                    lat, lon, code, msg
                                )
                                errors["base"] = msg
                            else:
                                props = data.get("properties", {})
                                self._parsed_zone = props.get("forecastZone", "").split("/")[-1] or ""
                                self._parsed_county = props.get("county", "").split("/")[-1] or ""
                                return await self.async_step_zone(None)
                        else:
                            friendly_error = await _get_friendly_error(self.hass, "unknown_error")
                            _LOGGER.error(
                                "Unknown error (non-dict API response) for lat=%s, lon=%s - HTTP code: %s, error: %s",
                                lat, lon, code, friendly_error
                            )
                            errors["base"] = "unknown_error"

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_zone(self, user_input=None):
        errors = {}
        suggested_zone = self._parsed_zone or ""
        suggested_county = self._parsed_county or ""
        schema = vol.Schema({
            vol.Required(CONF_ZONE): str,
            vol.Optional(CONF_COUNTY): str,
            vol.Optional(CONF_MARINE_ZONES): str,
        })
        schema = self.add_suggested_values_to_schema(schema, {
            CONF_ZONE: suggested_zone,
            CONF_COUNTY: suggested_county,
            CONF_MARINE_ZONES: "",
        })

        if user_input:
            zone = user_input[CONF_ZONE].strip().upper()
            county = user_input.get(CONF_COUNTY, "").strip().upper()
            marine = user_input.get(CONF_MARINE_ZONES, "").strip().upper()

            if not re.match(NWS_CODE_REGEX, zone):
                errors["zone"] = "invalid_zone"
                errors["base"] = f"Invalid zone code: {zone}"
            elif county and not re.match(NWS_CODE_REGEX, county):
                errors["county"] = "invalid_county"
                errors["base"] = f"Invalid county code: {county}"
            elif marine and not all(re.match(NWS_CODE_REGEX, m.strip()) for m in marine.split(",") if m.strip()):
                errors["marine_zones"] = "invalid_marine"
                invalid_m = next((m for m in marine.split(",") if not re.match(NWS_CODE_REGEX, m.strip())), "")
                errors["base"] = f"Invalid zone code: {invalid_m}"
            else:
                valid = await _validate_zone_api(self.hass, zone, county, marine, errors)
                if not valid:
                    return self.async_show_form(step_id="zone", data_schema=schema, errors=errors)

                # Store for next step
                self._zone = zone
                self._county = county
                self._marine = marine

                return await self.async_step_update_options()

        return self.async_show_form(step_id="zone", data_schema=schema, errors=errors)

    async def async_step_update_options(self, user_input=None):
        from .const import (
            CONF_UPDATE_INTERVAL,
            CONF_API_TIMEOUT,
            DEFAULT_UPDATE_INTERVAL,
            DEFAULT_API_TIMEOUT,
            MIN_UPDATE_INTERVAL,
            MAX_UPDATE_INTERVAL,
            MIN_API_TIMEOUT,
            MAX_API_TIMEOUT,
            TIMEOUT_BUFFER,
        )

        errors = {}
        schema = vol.Schema({
            vol.Required(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): int,
            vol.Required(CONF_API_TIMEOUT, default=DEFAULT_API_TIMEOUT): int,
            vol.Optional(CONF_DEDUPLICATE_ALERTS, default=DEFAULT_DEDUPLICATE_ALERTS): bool,
       })

        if user_input:
            update = int(user_input[CONF_UPDATE_INTERVAL])
            timeout = int(user_input[CONF_API_TIMEOUT])
            deduplicate = user_input.get(CONF_DEDUPLICATE_ALERTS, DEFAULT_DEDUPLICATE_ALERTS)

            if update < MIN_UPDATE_INTERVAL or update > MAX_UPDATE_INTERVAL:
                errors[CONF_UPDATE_INTERVAL] = f"Must be between {MIN_UPDATE_INTERVAL} and {MAX_UPDATE_INTERVAL}"
            elif timeout < MIN_API_TIMEOUT or timeout > MAX_API_TIMEOUT:
                errors[CONF_API_TIMEOUT] = f"Must be between {MIN_API_TIMEOUT} and {MAX_API_TIMEOUT}"
            elif timeout >= update - TIMEOUT_BUFFER:
                errors[CONF_API_TIMEOUT] = f"Must be at least {TIMEOUT_BUFFER}s less than update interval"
            else:
                # Construct entity
                parts = [self._zone]
                if self._county:
                    parts.append(self._county)
                parts += [m.strip() for m in self._marine.split(",") if m.strip()]
                feed_id = ",".join(parts)

                session = async_get_clientsession(self.hass)
                zone_name = await _get_zone_name(session, self._zone)
                if zone_name and len(zone_name) > 40:
                    zone_name = "NWS"
                clean_name = _clean_for_entity_id(zone_name or self._zone)
                clean_id = _clean_for_entity_id(feed_id)
                entity_name = f"weatheralerts_{clean_name}_{clean_id}"
                friendly_name = f"{zone_name} ({feed_id})" if zone_name else f"NWS ({feed_id})"

                await self.async_set_unique_id(f"{DOMAIN}_{clean_id}")
                self._abort_if_unique_id_configured()

                data = {
                    CONF_ZONE: self._zone,
                    CONF_ZONE_NAME: zone_name,
                    CONF_NAME: friendly_name,
                    CONF_ENTITY_NAME: entity_name,
                    CONF_UPDATE_INTERVAL: update,
                    CONF_API_TIMEOUT: timeout,
                    CONF_DEDUPLICATE_ALERTS: deduplicate,
                }
                if self._county:
                    data[CONF_COUNTY] = self._county
                if self._lat and self._lon:
                    data[CONF_LATITUDE] = self._lat
                    data[CONF_LONGITUDE] = self._lon
                if self._marine:
                    data[CONF_MARINE_ZONES] = self._marine

                return self.async_create_entry(title=friendly_name, data=data)

        return self.async_show_form(step_id="update_options", data_schema=schema, errors=errors)

    async def async_step_import(self, import_data):
        """Silent import of YAML — no user input required."""
        state = import_data.get("state", "")
        raw_zone = import_data.get("zone", "")
        raw_county = import_data.get("county", "")

        # Normalize codes
        if state and raw_zone and len(str(raw_zone)) <= 3:
            zone = f"{state.upper()}Z{str(raw_zone).zfill(3)}"
        else:
            zone = raw_zone.upper()
        if state and raw_county and len(str(raw_county)) <= 3:
            county = f"{state.upper()}C{str(raw_county).zfill(3)}"
        else:
            county = raw_county.upper()

        # No marine zones in YAML
        marine = ""

        # Fetch zone_name (=40 chars, else fallback to 'NWS')
        session = async_get_clientsession(self.hass)
        zone_name = await _get_zone_name(session, zone)
        if zone_name and len(zone_name) > 40:
            zone_name = "NWS"

        # Build feed_id, entity & friendly names
        feed_parts = [zone] + ([county] if county else []) + []
        feed_id = ",".join(feed_parts)
        clean_name = _clean_for_entity_id(zone_name or zone)
        clean_id = _clean_for_entity_id(feed_id)
        entity_name = f"weatheralerts_{clean_name}_{clean_id}"
        friendly_name = f"{zone_name} ({feed_id})" if zone_name else f"NWS ({feed_id})"

        # Ensure uniqueness & avoid dupes
        await self.async_set_unique_id(f"{DOMAIN}_{clean_id}")
        self._abort_if_unique_id_configured()

        data = {
            CONF_ZONE: zone,
            CONF_COUNTY: county,
            CONF_ZONE_NAME: zone_name,
            CONF_NAME: friendly_name,
            CONF_ENTITY_NAME: entity_name,
        }
        # No latitude/longitude from YAML import
        # No marine zones

        return self.async_create_entry(title=friendly_name, data=data)

    @staticmethod
    @callback
    def async_get_options_flow(entry):
        return WeatheralertsOptionsFlow(entry)


class WeatheralertsOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Weather Alerts."""

    def __init__(self, entry):
        self._entry = entry
        self.updated_options = dict(entry.options)
        for key in [CONF_ZONE, CONF_COUNTY, CONF_MARINE_ZONES, CONF_NAME, CONF_ENTITY_NAME, CONF_ZONE_NAME]:
            if key not in self.updated_options and key in entry.data:
                self.updated_options[key] = entry.data[key]

    async def async_step_init(self, user_input=None):
        errors = {}
        schema = vol.Schema({
            vol.Required(CONF_ZONE): str,
            vol.Optional(CONF_COUNTY): str,
            vol.Optional(CONF_MARINE_ZONES): str,
        })
        data_schema = self.add_suggested_values_to_schema(schema, self.updated_options)

        if user_input is not None:
            zone = user_input[CONF_ZONE].strip().upper()
            county = user_input.get(CONF_COUNTY, "").strip().upper()
            marine = user_input.get(CONF_MARINE_ZONES, "").strip().upper()
            
            # VALIDATION using config flow logic
            valid = await _validate_zone_api(self.hass, zone, county, marine, errors)
            if not valid:
                # Show the form again with error(s)
                return self.async_show_form(step_id="init", data_schema=data_schema, errors=errors)

            parts = [zone] + ([county] if county else []) + [m.strip() for m in marine.split(",") if m.strip()]
            feed_id = ",".join(parts)
            session = async_get_clientsession(self.hass)
            session = async_get_clientsession(self.hass)
            zone_name = await _get_zone_name(session, zone)
            if zone_name and len(zone_name) > 40:
                zone_name = "NWS"
            friendly_name = f"{zone_name} ({feed_id})" if zone_name else f"NWS ({feed_id})"
            entity_name = f"weatheralerts_{_clean_for_entity_id(zone_name or zone)}_{_clean_for_entity_id(feed_id)}"

            self.updated_options[CONF_ZONE] = zone
            self.updated_options[CONF_COUNTY] = county
            self.updated_options[CONF_MARINE_ZONES] = marine
            self.updated_options[CONF_ZONE_NAME] = zone_name
            self.updated_options[CONF_NAME] = friendly_name
            self.updated_options[CONF_ENTITY_NAME] = entity_name

            self.hass.config_entries.async_update_entry(self._entry, title=friendly_name)
            return await self.async_step_update_options()

        return self.async_show_form(step_id="init", data_schema=data_schema, errors=errors)

    async def async_step_update_options(self, user_input=None):
        errors = {}
        update = self.updated_options.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
        timeout = self.updated_options.get(CONF_API_TIMEOUT, DEFAULT_API_TIMEOUT)
        dedup_default = self.updated_options.get(CONF_DEDUPLICATE_ALERTS, DEFAULT_DEDUPLICATE_ALERTS)

        schema = vol.Schema({
            vol.Required(CONF_UPDATE_INTERVAL, default=update): int,
            vol.Required(CONF_API_TIMEOUT, default=timeout): int,
            vol.Optional(CONF_DEDUPLICATE_ALERTS, default=dedup_default): bool,
        })

        if user_input:
            update = int(user_input[CONF_UPDATE_INTERVAL])
            timeout = int(user_input[CONF_API_TIMEOUT])
            deduplicate = user_input.get(CONF_DEDUPLICATE_ALERTS, DEFAULT_DEDUPLICATE_ALERTS)


            if update < MIN_UPDATE_INTERVAL or update > MAX_UPDATE_INTERVAL:
                errors[CONF_UPDATE_INTERVAL] = f"Must be between {MIN_UPDATE_INTERVAL} and {MAX_UPDATE_INTERVAL}"
            elif timeout < MIN_API_TIMEOUT or timeout > MAX_API_TIMEOUT:
                errors[CONF_API_TIMEOUT] = f"Must be between {MIN_API_TIMEOUT} and {MAX_API_TIMEOUT}"
            elif timeout >= update - TIMEOUT_BUFFER:
                errors[CONF_API_TIMEOUT] = f"Must be at least {TIMEOUT_BUFFER}s less than update interval"
            else:
                self.updated_options[CONF_UPDATE_INTERVAL] = update
                self.updated_options[CONF_API_TIMEOUT] = timeout
                self.updated_options[CONF_DEDUPLICATE_ALERTS] = deduplicate
                return await self.async_step_icon_config()

        return self.async_show_form(step_id="update_options", data_schema=schema, errors=errors)

    async def async_step_icon_config(self, user_input=None):
        """Icon configuration step for options flow."""
        errors = {}

        import json

        # Load existing icons from updated_options or entry options
        raw = self.updated_options.get(
            CONF_EVENT_ICONS,
            self._entry.options.get(CONF_EVENT_ICONS, {})
        )
        icon_data = json.loads(raw) if isinstance(raw, str) else dict(raw)

        # Default icon (existing or built-in)
        default_icon = self.updated_options.get(
            CONF_DEFAULT_ICON,
            self._entry.options.get(CONF_DEFAULT_ICON, DEFAULT_EVENT_ICON)
        )

        # Base mapping + overrides
        icon_map = {**DEFAULT_EVENT_ICONS, **icon_data}

        suggested_values = dict(icon_map)
        suggested_values[CONF_DEFAULT_ICON] = default_icon

        base_schema = {
            vol.Optional(CONF_DEFAULT_ICON, default="", description={"suggested_value": default_icon}): str,
            vol.Optional("new_event_type", default=""): str,
            vol.Optional("new_icon_def", default=""): str,
        }
        for event in sorted(icon_map):
            base_schema[vol.Optional(event, default="")] = str

        schema = vol.Schema(base_schema)
        data_schema = self.add_suggested_values_to_schema(schema, suggested_values)

        if user_input is not None:
            new_opts = dict(self.updated_options)

            # Handle Default Icon (now always present in user_input)
            iv = user_input.get(CONF_DEFAULT_ICON, None)
            if iv is None:
                # Defensive: key missing from form, treat as reset to default
                new_opts.pop(CONF_DEFAULT_ICON, None)
            else:
                iv = iv.strip()
                if not iv or iv == DEFAULT_EVENT_ICON:
                    new_opts.pop(CONF_DEFAULT_ICON, None)
                else:
                    new_opts[CONF_DEFAULT_ICON] = iv
    
            # New event mapping
            new_event = user_input.get("new_event_type", "").strip()
            new_icon = user_input.get("new_icon_def", "").strip()
            if new_event and new_icon:
                icon_data[new_event] = new_icon

            # Existing icons—including cleared ones
            for event in sorted(icon_map):
                if event in user_input:
                    val = user_input[event].strip()
                    if val:
                        icon_data[event] = val
                    else:
                        icon_data.pop(event, None)

            # Persist icon overrides or remove entirely if empty
            if icon_data:
                new_opts[CONF_EVENT_ICONS] = icon_data
            else:
                new_opts.pop(CONF_EVENT_ICONS, None)

            self.updated_options = new_opts
            return self.async_create_entry(data=new_opts)

        return self.async_show_form(
            step_id="icon_config",
            data_schema=data_schema,
            errors=errors,
        )
