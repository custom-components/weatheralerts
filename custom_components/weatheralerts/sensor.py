"""
A component which allows you to get weather alerts from weather.gov.
For more details about this component, please refer to the documentation at

https://github.com/custom-components/sensor.weatheralerts
"""
import sys
import logging
import async_timeout
import voluptuous as vol

from homeassistant.components.switch import PLATFORM_SCHEMA
from homeassistant.const import __version__
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

CONF_STATE = "state"
CONF_ZONE = "zone"
CONF_TYPE = "type"

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_STATE): cv.string, vol.Required(CONF_ZONE): cv.string, vol.Required(CONF_TYPE): cv.matches_regex("(^zone$|^county$)")}
)

URL = "https://api.weather.gov/alerts/active/zone/{}"

HEADERS = {
    "accept": "application/ld+json",
    "user-agent": f"HomeAssistant/{__version__}",
}


async def async_setup_platform(
    hass, config, add_entities, discovery_info=None
):  # pylint: disable=missing-docstring, unused-argument
    state = config[CONF_STATE].upper()
    zone = config[CONF_ZONE]
    zone_type = config[CONF_TYPE].lower()
    
    if len(state) != 2:
        _LOGGER.critical("Configured (YAML) state '%s' is not valid", state)
        return False

    if len(zone) == 1:
        zone = f"00{zone}"
    if len(zone) == 2:
        zone = f"0{zone}"

    if len(zone) == 3 and zone_type == "zone":
        zoneid = f"{state}Z{zone}"
    elif len(zone) == 3 and zone_type == "county":
        zoneid = f"{state}C{zone}"
    else:
        _LOGGER.critical("Configured (YAML) zone '%s' is not valid", zone)
        return False
    
    session = async_create_clientsession(hass)

    # Check the zoneid
    try:
        async with async_timeout.timeout(10, loop=hass.loop):
            response = await session.get(URL.format(zoneid))
            data = await response.json()

            if "status" in data:
                if data["status"] == 404:
                    _LOGGER.critical("Compiled zone ID '%s' is not valid", zoneid)
                    return False

            _LOGGER.debug(data)
            name = data["title"].split("advisories for ")[1].split(" (")[0]

    except Exception as exception:  # pylint: disable=broad-except
        _LOGGER.error("[%s] %s", sys.exc_info()[0].__name__, exception)
        return False

    add_entities([WeatherAlertsSensor(name, state, zoneid, session)], True)
    _LOGGER.info("Added sensor with name '%s' for zoneid '%s'", name, zoneid)


class WeatherAlertsSensor(Entity):  # pylint: disable=missing-docstring
    def __init__(self, name, zone_state, zoneid, session):
        self._name = name
        self.zone_state = zone_state
        self.zoneid = zoneid
        self.session = session
        self._state = 0
        self.connected = True
        self.exception = None
        self._attr = {}

    async def async_update(self):
        """Run update."""
        alerts = []

        try:
            async with async_timeout.timeout(10, loop=self.hass.loop):
                response = await self.session.get(URL.format(self.zoneid))
                if response.status != 200:
                    self._state = "unavailable"
                    _LOGGER.critical("Weather alert download failure - HTTP status code %s", response.status)
                else:
                    data = await response.json()

                    if data.get("features") is not None:
                        for alert in data["features"]:
                            if alert.get("properties") is not None:
                                properties = alert["properties"]
                                alerts.append(
                                    {
                                        "area": properties.get("areaDesc", "null"),
                                        "certainty": properties.get("certainty", "null"),
                                        "description": properties.get("description", "null"),
                                        "ends": properties.get("ends", "null"),
                                        "event": properties.get("event", "null"),
                                        "instruction": properties.get("instruction", "null"),
                                        "response": properties.get("response", "null"),
                                        "sent": properties.get("sent", "null"),
                                        "severity": properties.get("severity", "null"),
                                        "title": properties.get("headline", "null").split(" by ")[0],
                                        "urgency": properties.get("urgency", "null"),
                                        "NWSheadline": properties["parameters"].get("NWSheadline", "null"),
                                        "effective": properties.get("effective", "null"),
                                        "expires": properties.get("expires", "null"),
                                        "onset": properties.get("onset", "null"),
                                        "status": properties.get("status", "null"),
                                        "messageType": properties.get("messageType", "null"),
                                        "category": properties.get("category", "null"),
                                        "zoneid": self.zoneid,
                                    }
                                )

                    self._state = len(alerts)
                    self._attr = {
                        "alerts": alerts,
                        "integration": "weatheralerts",
                        "state": self.zone_state,
                        "zone": self.zoneid,
                    }
        except Exception:  # pylint: disable=broad-except
            self.exception = sys.exc_info()[0].__name__
            connected = False
        else:
            connected = True
        finally:
            # Handle connection messages here.
            if self.connected:
                if not connected:
                    self._state = "unavailable"
                    _LOGGER.error(
                        "[%s] Could not update the sensor (%s)",
                        self.zoneid,
                        self.exception,
                    )

            elif not self.connected:
                if connected:
                    _LOGGER.info("[%s] Update of the sensor completed", self.zoneid)
                else:
                    self._state = "unavailable"
                    _LOGGER.debug(
                        "[%s] Still no update (%s)", self.zoneid, self.exception
                    )

            self.connected = connected

    @property
    def name(self):
        """Return the name."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID to use for this sensor."""
        return f"weatheralerts_{self.zoneid}"

    @property
    def state(self):
        """Return the state."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit_of_measurement."""
        return "Alerts"

    @property
    def icon(self):
        """Return icon."""
        return "mdi:weather-hurricane"

    @property
    def device_state_attributes(self):
        """Return attributes."""
        return self._attr
    
