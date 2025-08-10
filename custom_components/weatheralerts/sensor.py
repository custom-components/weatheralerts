"""
An integration which allows you to get weather alerts from weather.gov.
For more details about this integration, please refer to the documentation at
https://github.com/custom-components/weatheralerts
"""
import logging
import async_timeout
import re
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity, RestoreEntity
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    CoordinatorEntity,
    UpdateFailed,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    ALERTS_API,
    HEADERS,
    CONF_ZONE,
    CONF_COUNTY,
    CONF_ZONE_NAME,
    CONF_NAME,
    CONF_ENTITY_NAME,
    CONF_MARINE_ZONES,
    CONF_EVENT_ICONS,
    CONF_DEFAULT_ICON,
    CONF_DEDUPLICATE_ALERTS,
    DEFAULT_EVENT_ICONS,
    DEFAULT_EVENT_ICON,
    CONF_UPDATE_INTERVAL,
    CONF_API_TIMEOUT,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_API_TIMEOUT,
    DEFAULT_DEDUPLICATE_ALERTS,
)

_LOGGER = logging.getLogger(__name__)

def _clean_for_entity_id(text):
    return re.sub(r'[^a-z0-9_]', '', re.sub(r'[-\s,]+', '_', text.lower())).strip('_')

def _get_icon_for_event(event, entry_options=None):
    event_icons = None
    default_icon = None
    if entry_options:
        event_icons = entry_options.get(CONF_EVENT_ICONS)
        default_icon = entry_options.get(CONF_DEFAULT_ICON)
        if isinstance(event_icons, str):
            import json
            try:
                event_icons = json.loads(event_icons)
            except Exception:
                event_icons = None
    if not event_icons or not isinstance(event_icons, dict):
        event_icons = DEFAULT_EVENT_ICONS
    if not default_icon or not isinstance(default_icon, str):
        default_icon = DEFAULT_EVENT_ICON
    lower_map = {k.lower(): v for k, v in event_icons.items()}
    icon = lower_map.get(str(event or "").strip().lower())
    return icon if icon else default_icon

def _compute_active_alert_stats(alerts):
    now_ts = dt_util.as_timestamp(dt_util.now())
    def is_active(alert):
        ends_str = alert.get("expires")
        if not ends_str or ends_str == "null":
            return False
        try:
            ends_ts = dt_util.as_timestamp(ends_str)
            if not ends_ts:
                return False
            return (ends_ts - now_ts) > 0
        except Exception:
            _LOGGER.debug(f"weatheralerts: Could not parse 'expires' for active_alert_stats: {ends_str}")
            return False

    categories = {
        "active_warning": "warning",
        "active_watch": "watch",
        "active_advisory": "advisory",
        "active_statement": "statement",
        "active_outlook": "outlook",
        "active_alert": "alert",
        "active_message": "message",
        "active_important": "important",
        "active_test": "test",
        "active_outage": "outage",
        "active_emergency": "emergency",
        "active_immediate": "immediate",
        "active_forecast": "forecast",
    }

    stats = {k: 0 for k in categories}
    stats["total_active_alerts"] = 0

    for alert in alerts:
        if not alert.get("event"):
            continue
        event_text = alert["event"].lower()
        if is_active(alert):
            stats["total_active_alerts"] += 1
            for k, substr in categories.items():
                if substr in event_text:
                    stats[k] += 1
    return stats

def _dedup_key(text):
    return re.sub(r'\s+', '', text).lower()  # Remove all whitespace, make lowercase

def _deduplicate_alerts_by_description(alerts):
    """Deduplicate alerts by description, keeping only the newest sent, then latest expires, then top reverse-sorted id."""
    from collections import defaultdict
    grouped = defaultdict(list)
    for alert in alerts:
        key = _dedup_key(alert.get("description", ""))
        grouped[key].append(alert)
    deduped = []
    for desc, group in grouped.items():
        if len(group) == 1:
            deduped.append(group[0])
        else:
            # Sort by sent DESC (newest first), then expires DESC, then id DESC
            group.sort(key=lambda a: (
                a.get("sent", ""),
                a.get("expires", ""),
                a.get("id", ""),
            ), reverse=True)
            # Find the best "sent"
            best_sent = group[0].get("sent", "")
            sent_group = [a for a in group if a.get("sent", "") == best_sent]
            if len(sent_group) == 1:
                deduped.append(sent_group[0])
            else:
                # Further filter by expires DESC
                best_expires = max(a.get("expires", "") for a in sent_group)
                expires_group = [a for a in sent_group if a.get("expires", "") == best_expires]
                if len(expires_group) == 1:
                    deduped.append(expires_group[0])
                else:
                    # Reverse sort by id and keep the first one
                    expires_group.sort(key=lambda a: a.get("id", ""), reverse=True)
                    deduped.append(expires_group[0])
    return deduped

class WeatherAlertsCoordinator(DataUpdateCoordinator):
    """Coordinator for fetching weather alerts and tracking alert_tracking."""

    def __init__(self, hass, session, feedid, config_entry_id, update_interval):
        super().__init__(
            hass,
            _LOGGER,
            name=f"WeatherAlerts ({feedid})",
            update_interval=update_interval,
        )
        self.session = session
        self.feedid = feedid
        self.config_entry_id = config_entry_id
        self._last_good_data = None
        self._last_error = []
        self._alert_tracking_list = []
        _LOGGER.info("weatheralerts: WeatherAlertsCoordinator initialized for feedid: %s", feedid)

    async def _async_update_data(self):
        _LOGGER.debug("weatheralerts: _async_update_data called for feedid: %s", self.feedid)
        update_error = []

        entry = next((e for e in self.hass.config_entries.async_entries(DOMAIN)
                     if e.entry_id == self.config_entry_id), None)
        timeout_seconds = entry.options.get(CONF_API_TIMEOUT,
                            entry.data.get(CONF_API_TIMEOUT, DEFAULT_API_TIMEOUT)) if entry else DEFAULT_API_TIMEOUT
        deduplicate_alerts = entry.options.get(CONF_DEDUPLICATE_ALERTS, entry.data.get(CONF_DEDUPLICATE_ALERTS, DEFAULT_DEDUPLICATE_ALERTS)) if entry else DEFAULT_DEDUPLICATE_ALERTS

        try:
            async with async_timeout.timeout(timeout_seconds):
                alerts_url = ALERTS_API.format(self.feedid)
                _LOGGER.debug("weatheralerts: Fetching Alerts URL: %s", alerts_url)
                response = await self.session.get(alerts_url, headers=HEADERS)
                _LOGGER.debug("weatheralerts: HTTP status code: %s", response.status)
                if response.status != 200:
                    error_msg = f"Possible API outage (status {response.status})"
                    current_entry = {
                        "type": "http_error",
                        "status": response.status,
                        "message": error_msg,
                        "timestamp": dt_util.now().isoformat(),
                    }
                    previous_entry = next((e for e in reversed(self._last_error) if e.get("type") == "success"), None)
                    update_error = [current_entry]
                    if previous_entry:
                        update_error.append(previous_entry)
                    if self._last_good_data:
                        data = dict(self._last_good_data)
                        # --- prune stale alerts when falling back to previous data ---
                        try:
                            now = dt_util.now()
                            fallback_delete_buffer = timedelta(minutes=10)

                            alerts = list(data.get("alerts", []))
                            kept_alerts = []
                            kept_ids = set()

                            for a in alerts:
                                exp = a.get("expires")
                                drop = False
                                if exp and exp != "null":
                                    try:
                                        exp_dt = dt_util.parse_datetime(exp)
                                        if exp_dt and now >= (exp_dt + fallback_delete_buffer):
                                            drop = True
                                    except Exception:
                                        # If we can't parse, keep it rather than accidentally dropping
                                        pass

                                if not drop:
                                    kept_alerts.append(a)
                                    if a.get("id"):
                                        kept_ids.add(a["id"])

                            # Replace with pruned alerts, update count + stats
                            data["alerts"] = kept_alerts
                            data["count"] = len(kept_alerts)
                            data["alert_stats"] = _compute_active_alert_stats(kept_alerts)

                            # Drop any alert_tracking rows for removed alerts
                            tracking = list(data.get("alert_tracking", []))
                            data["alert_tracking"] = [t for t in tracking if t.get("id") in kept_ids]

                        except Exception as e:
                            _LOGGER.debug("weatheralerts: prune-on-fallback failed: %s", e)
                        # --- end prune block ---
                        data["error"] = update_error
                        self._last_error = update_error
                        return data
                    else:
                        return {
                            "alerts": [],
                            "count": 0,
                            "alert_stats": {},
                            "integration": "weatheralerts",
                            "zone": self.feedid,
                            "alert_tracking": self._alert_tracking_list,
                            "error": update_error,
                        }
                data = await response.json()
                _LOGGER.debug("weatheralerts: Fetched data keys: %s", list(data.keys()))
        except Exception as err:
            error_msg = f"Update failed: {err}"
            current_entry = {
                "type": "exception",
                "status": "",
                "message": str(err),
                "timestamp": dt_util.now().isoformat(),
            }
            previous_entry = next((e for e in reversed(self._last_error) if e.get("type") == "success"), None)
            update_error = [current_entry]
            if previous_entry:
                update_error.append(previous_entry)
            _LOGGER.debug("weatheralerts: Exception in _async_update_data: %s", err)
            if self._last_good_data:
                data = dict(self._last_good_data)
                # --- prune stale alerts when falling back to previous data ---
                try:
                    now = dt_util.now()
                    fallback_delete_buffer = timedelta(minutes=10)

                    alerts = list(data.get("alerts", []))
                    kept_alerts = []
                    kept_ids = set()

                    for a in alerts:
                        exp = a.get("expires")
                        drop = False
                        if exp and exp != "null":
                            try:
                                exp_dt = dt_util.parse_datetime(exp)
                                if exp_dt and now >= (exp_dt + fallback_delete_buffer):
                                    drop = True
                            except Exception:
                                # If we can't parse, keep it rather than accidentally dropping
                                pass

                        if not drop:
                            kept_alerts.append(a)
                            if a.get("id"):
                                kept_ids.add(a["id"])

                    # Replace with pruned alerts, update count + stats
                    data["alerts"] = kept_alerts
                    data["count"] = len(kept_alerts)
                    data["alert_stats"] = _compute_active_alert_stats(kept_alerts)

                    # Drop any alert_tracking rows for removed alerts
                    tracking = list(data.get("alert_tracking", []))
                    data["alert_tracking"] = [t for t in tracking if t.get("id") in kept_ids]

                except Exception as e:
                    _LOGGER.debug("weatheralerts: prune-on-fallback failed: %s", e)
                # --- end prune block ---
                data["error"] = update_error
                self._last_error = update_error
                return data
            else:
                return {
                    "alerts": [],
                    "count": 0,
                    "alert_stats": {},
                    "integration": "weatheralerts",
                    "zone": self.feedid,
                    "alert_tracking": self._alert_tracking_list,
                    "error": update_error,
                }

        # Get config entry options
        entry = None
        if hasattr(self.hass, "config_entries"):
            for e in self.hass.config_entries.async_entries(DOMAIN):
                if e.entry_id == self.config_entry_id:
                    entry = e
                    break
        entry_options = entry.options if entry else None

        # Build alerts list as before
        alerts = []
        for feature in data.get("features", []):
            props = feature.get("properties", {})
            props["endsExpires"] = (
                props.get("expires", "null")
                if props.get("ends") is None
                else props.get("ends", "null")
            )
            event_value = props.get("event", "null")
            alert = {
                "area": props.get("areaDesc", "null"),
                "certainty": props.get("certainty", "null"),
                "description": props.get("description", "null"),
                "ends": props.get("ends", "null"),
                "event": event_value,
                "instruction": props.get("instruction", "null"),
                "response": props.get("response", "null"),
                "sent": props.get("sent", "null"),
                "severity": props.get("severity", "null"),
                "title": props.get("headline", "null").split(" by ")[0],
                "urgency": props.get("urgency", "null"),
                "NWSheadline": props.get("NWSheadline", "null"),
                "hailSize": props.get("hailSize", "null"),
                "windGust": props.get("windGust", "null"),
                "waterspoutDetection": props.get("waterspoutDetection", "null"),
                "effective": props.get("effective", "null"),
                "expires": props.get("expires", "null"),
                "onset": props.get("onset", "null"),
                "endsExpires": props.get("endsExpires", "null"),
                "status": props.get("status", "null"),
                "messageType": props.get("messageType", "null"),
                "category": props.get("category", "null"),
                "sender": props.get("sender", "null"),
                "senderName": props.get("senderName", "null"),
                "id": props.get("id", "null"),
                "zoneid": self.feedid,
            }
            alert["icon"] = _get_icon_for_event(event_value, entry_options)
            alerts.append(alert)
        _LOGGER.debug("weatheralerts: Parsed %d alerts", len(alerts))

        if deduplicate_alerts:
            alerts = _deduplicate_alerts_by_description(alerts)
            _LOGGER.debug("weatheralerts: %d alerts after deduplication", len(alerts))

        alerts.sort(key=lambda x: (x.get("sent", ""), x.get("id", "")), reverse=True)
        alert_stats = _compute_active_alert_stats(alerts)

        # ------- alert_tracking TRACKING LOGIC -------
        now = dt_util.now()

        # 1. Build lookups for current and previous
        current_alerts_by_id = {a["id"]: a for a in alerts if a.get("id")}
        prev_alerts_by_id = {e["id"]: e for e in self._alert_tracking_list if "id" in e}

        # 2. Build new alert_tracking list
        new_alert_tracking_list = []
        is_initial = not self._alert_tracking_list
        for alert_tracking, alert in current_alerts_by_id.items():
            expires = alert.get("expires")
            sent = alert.get("sent")
            prev_entry = prev_alerts_by_id.get(alert_tracking)

            if is_initial or prev_entry is None:
                status = "new"
                status_ts = now.isoformat()
            else:
                # if it existed before—even if it was “delete”—treat as “old”
                status = "old"
                # keep old timestamp when status unchanged; bump when status changed
                if prev_entry.get("status") == status and prev_entry.get("status_timestamp"):
                    status_ts = prev_entry["status_timestamp"]
                else:
                    status_ts = now.isoformat()

            new_alert_tracking_list.append({
                "id": alert_tracking,
                "sent": sent,
                "expires": expires,
                "status": status,
                "status_timestamp": status_ts,
            })

        # 3. Mark as deleted if missing from live alerts
        for alert_tracking, prev_entry in prev_alerts_by_id.items():
            if alert_tracking not in current_alerts_by_id:
                prev_status = prev_entry.get("status")
                # preserve timestamp if already 'delete', else bump to now
                status_ts = (
                    prev_entry.get("status_timestamp")
                    if prev_status == "delete" and prev_entry.get("status_timestamp")
                    else now.isoformat()
                )
                new_alert_tracking_list.append({
                    "id": alert_tracking,
                    "sent": prev_entry.get("sent"),
                    "expires": prev_entry.get("expires"),
                    "status": "delete",
                    "status_timestamp": status_ts,
                })

        # 4. Drop entries based on expiration or 'delete' age (delete_buffer window)
        cleaned_alert_tracking_list = []
        delete_buffer = timedelta(minutes=10)

        for entry in new_alert_tracking_list:
            # Parse expires
            exp_dt = None
            expires = entry.get("expires")
            if expires:
                try:
                    exp_dt = dt_util.parse_datetime(expires)
                except Exception:
                    exp_dt = None

            # Parse status_timestamp
            status_ts_dt = None
            status_ts = entry.get("status_timestamp")
            if status_ts:
                try:
                    status_ts_dt = dt_util.parse_datetime(status_ts)
                except Exception:
                    status_ts_dt = None

            drop_for_expiry = exp_dt is not None and now >= (exp_dt + delete_buffer)
            drop_for_delete_age = (
                entry.get("status") == "delete"
                and status_ts_dt is not None
                and now >= (status_ts_dt + delete_buffer)
            )

            if drop_for_expiry or drop_for_delete_age:
                # Skip adding -> effectively removed
                continue

            cleaned_alert_tracking_list.append(entry)

        cleaned_alert_tracking_list.sort(
            key=lambda x: (x.get("sent", ""), x.get("id", "")), reverse=True
        )
        self._alert_tracking_list = cleaned_alert_tracking_list
        # ------- END alert_tracking TRACKING LOGIC -------

        # Build success + last failure error tracking
        current_entry = {
            "type": "success",
            "status": "OK",
            "message": "no errors",
            "timestamp": dt_util.now().isoformat(),
        }
        previous_entry = next((e for e in reversed(self._last_error) if e.get("type") != "success"), None)
        update_error = [current_entry]
        if previous_entry:
            update_error.append(previous_entry)

        result = {
            "alerts": alerts,
            "count": len(alerts),
            "alert_stats": alert_stats,
            "integration": "weatheralerts",
            "zone": self.feedid,
            "alert_tracking": self._alert_tracking_list,
            "error": update_error,
        }
        self._last_good_data = dict(result)
        self._last_error = update_error
        _LOGGER.debug("weatheralerts: Returning update data: count=%d", len(alerts))
        return result

# ------------ RestoreEntity ADDED! ------------
class WeatherAlertsSensor(CoordinatorEntity, RestoreEntity, SensorEntity):
    """Representation of a weather alerts sensor with persistence."""

    def __init__(self, coordinator, entity_name, feedid):
        if not entity_name:
            entity_name = f"weatheralerts_{_clean_for_entity_id(feedid)}"
            _LOGGER.debug("weatheralerts: entity_name missing, using fallback %s", entity_name)
        else:
            entity_name = _clean_for_entity_id(entity_name)
        _LOGGER.debug("weatheralerts: WeatherAlertsSensor __init__ for %s", entity_name)
        super().__init__(coordinator)
        self.entity_id = f"sensor.{entity_name}"
        self._feedid = feedid
        self._attr_name = None

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self._update_friendly_name()
        entry = self._get_config_entry()
        if entry:
            self.async_on_remove(
                entry.add_update_listener(self._config_entry_updated)
            )
        # ------------- Restore alert_tracking after restart -------------
        last_state = await self.async_get_last_state()
        if last_state is not None:
            restored_alert_tracking = last_state.attributes.get("alert_tracking")
            if restored_alert_tracking and isinstance(self.coordinator, WeatherAlertsCoordinator):
                self.coordinator._alert_tracking_list = restored_alert_tracking
                _LOGGER.info("weatheralerts: Restored alert_tracking list from last state")
        # ----------------------------------------------------------

    async def _config_entry_updated(self, hass, entry):
        self._update_friendly_name()
        self.async_write_ha_state()

    def _get_config_entry(self):
        if hasattr(self.coordinator, "config_entry_id"):
            for entry in self.hass.config_entries.async_entries(DOMAIN):
                if entry.entry_id == self.coordinator.config_entry_id:
                    return entry
        entries = self.hass.config_entries.async_entries(DOMAIN)
        return entries[0] if entries else None

    def _update_friendly_name(self):
        entry = self._get_config_entry()
        if entry:
            self._attr_name = entry.data.get(CONF_NAME, self._attr_name)
            _LOGGER.debug("weatheralerts: Updated friendly name to: %s", self._attr_name)

    @property
    def name(self):
        return self._attr_name

    @property
    def unique_id(self):
        uid = f"weatheralerts_{self._feedid.replace(',', '').lower()}"
        _LOGGER.debug("weatheralerts: WeatherAlertsSensor unique_id: %s", uid)
        return uid

    @property
    def state(self):
        if self.coordinator.data:
            _LOGGER.debug("weatheralerts: WeatherAlertsSensor state: %s", self.coordinator.data.get('count', None))
            return self.coordinator.data.get("count", None)
        _LOGGER.debug("weatheralerts: WeatherAlertsSensor state: coordinator.data is None")
        return None

    @property
    def unit_of_measurement(self):
        return "Alerts"

    @property
    def icon(self):
        return "mdi:alert-octagram"

    @property
    def extra_state_attributes(self):
        if self.coordinator.data:
            _LOGGER.debug("weatheralerts: WeatherAlertsSensor extra_state_attributes: %s", self.coordinator.data)
            entry = self._get_config_entry()
            zone_name = (
                entry.options.get(CONF_ZONE_NAME)
                or entry.data.get(CONF_ZONE_NAME)
                or None
            )
            return {
                "integration": self.coordinator.data["integration"],
                "zone": self.coordinator.data["zone"],
                "zone_name": zone_name,
                "alert_stats": self.coordinator.data.get("alert_stats", {}),
                "alerts": self.coordinator.data["alerts"],
                "alert_tracking": self.coordinator.data.get("alert_tracking", []),
                "error": self.coordinator.data.get("error", []),
            }
        _LOGGER.debug("weatheralerts: WeatherAlertsSensor extra_state_attributes: coordinator.data is None")
        return {}

async def async_setup_entry(hass, entry, add_entities):
    _LOGGER.debug("weatheralerts: async_setup_entry (sensor.py) called for entry: %s", entry.entry_id)
    zone = entry.options.get(CONF_ZONE, entry.data.get(CONF_ZONE, ""))
    county = entry.options.get(CONF_COUNTY, entry.data.get(CONF_COUNTY, ""))
    marine_zones = entry.options.get(CONF_MARINE_ZONES, entry.data.get(CONF_MARINE_ZONES, ""))
    conf_name = entry.data.get(CONF_NAME, "NWS Weather Alerts")
    entity_name = entry.data.get(CONF_ENTITY_NAME)
    parts = [zone]
    if county:
        parts.append(county)
    if marine_zones:
        parts += [z.strip() for z in marine_zones.split(",") if z.strip()]
    feedid = ",".join(parts)
    if not entity_name:
        entity_name = f"weatheralerts_{_clean_for_entity_id(feedid)}"
        _LOGGER.debug("weatheralerts: entity_name missing in setup_entry! Using fallback %s", entity_name)
    _LOGGER.debug(
        "weatheralerts: async_setup_entry (sensor.py): zone=%s, county=%s, marine_zones=%s, entity_name=%s, friendly_name=%s, feedid=%s",
        zone, county, marine_zones, entity_name, conf_name, feedid
    )
    session = async_get_clientsession(hass)
    update_interval_sec = entry.options.get(CONF_UPDATE_INTERVAL, entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL))
    update_interval = timedelta(seconds=update_interval_sec)
    coordinator = WeatherAlertsCoordinator(
        hass, session, feedid, entry.entry_id, update_interval=update_interval
    )
    await coordinator.async_config_entry_first_refresh()
    _LOGGER.debug("weatheralerts: async_setup_entry (sensor.py): finished first refresh")
    add_entities([WeatherAlertsSensor(coordinator, entity_name, feedid)], True)
    _LOGGER.info("weatheralerts: async_setup_entry (sensor.py): sensor entity added (%s)", entity_name)

async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    _LOGGER.warning(
        "weatheralerts: YAML configuration for weatheralerts is deprecated and no longer supported; "
        "please use the Home Assistant UI to set up the integration. "
        "See the documentation for migration details."
    )
    return True
