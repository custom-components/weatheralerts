"""
A component which allows you to get weather alerts from weather.gov.
For more details about this component, please refer to the documentation at

https://github.com/custom-components/weatheralerts
"""
import sys
import logging
import async_timeout
import voluptuous as vol

from homeassistant.exceptions import PlatformNotReady
from homeassistant.components.switch import PLATFORM_SCHEMA
from homeassistant.const import __version__
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

__version__ = '0.1.1'

CONF_STATE = "state"
CONF_ZONE = "zone"
CONF_COUNTY = "county"

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_STATE): cv.string,
        vol.Required(CONF_ZONE): cv.string,
        vol.Optional(CONF_COUNTY, default=''): cv.string,
    }
)

URL = "https://api.weather.gov/alerts/active?zone={}"
URL_ID_CHECK = "https://alerts.weather.gov/cap/wwaatmget.php?x={}&y=0"
ID_CHECK_ERRORS = ["? invalid county", "? invalid zone"]

HEADERS = {
    "accept": "application/ld+json",
    "user-agent": f"HomeAssistant/{__version__}",
}


async def async_setup_platform(
    hass, config, add_entities, discovery_info=None
):  # pylint: disable=missing-docstring, unused-argument
    state = config[CONF_STATE].upper()
    zone_config = config[CONF_ZONE]
    county_config = config[CONF_COUNTY]
    
    zone=zone_config
    county=county_config
    
    if len(state) != 2:
        _LOGGER.critical("Configured (YAML) state '%s' is not valid", state)
        return False

    if len(zone) == 1:
        zone = f"00{zone}"
    if len(zone) == 2:
        zone = f"0{zone}"
    if len(zone) == 3:
        zoneid = f"{state}Z{zone}"
    else:
        _LOGGER.critical("Configured (YAML) zone ID '%s' is not valid", zone_config)
        return False

    if len(county) == 1:
        county = f"00{county}"
    if len(county) == 2:
        county = f"0{county}"
    if len(county) == 3:
        countyid = f"{state}C{county}"
    elif county != '':
        _LOGGER.critical("Configured (YAML) county ID '%s' is not valid", county_config)
        return False

    if len(county) == 3:
        feedid = f"{zoneid},{countyid}"
    else:
        feedid = zoneid

    session = async_create_clientsession(hass)

    # Check the zoneid and set sensor name to county name from zoneid alert feed
    try:
        async with async_timeout.timeout(10, loop=hass.loop):
            zone_check_response = await session.get(URL_ID_CHECK.format(zoneid))
            zone_data = await zone_check_response.text()

            if any (id_error in zone_data for id_error in ID_CHECK_ERRORS):
                _LOGGER.critical("Compiled zone ID '%s' is not valid", zoneid)
                return False

        if len(county) == 3:
             async with async_timeout.timeout(10, loop=hass.loop):
                county_check_response = await session.get(URL_ID_CHECK.format(countyid))
                county_data = await county_check_response.text()

                if any (id_error in county_data for id_error in ID_CHECK_ERRORS):
                    _LOGGER.critical("Compiled county ID '%s' is not valid", countyid)
                    return False

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
        raise PlatformNotReady

    add_entities([WeatherAlertsSensor(name, state, feedid, session)], True)
    _LOGGER.info("Added sensor with name '%s' for feedid '%s'", name, feedid)


class WeatherAlertsSensor(Entity):  # pylint: disable=missing-docstring
    def __init__(self, name, zone_state, feedid, session):
        self._name = name
        self.zone_state = zone_state
        self.feedid = feedid
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
                response = await self.session.get(URL.format(self.feedid))
                if response.status != 200:
                    self._state = "unavailable"
                    _LOGGER.critical(
                        "[%s] weatheralert download failure - HTTP status code %s",
                        self.feedid,
                        response.status
                    )
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
                                        "sender": properties.get("sender", "null"),
                                        "senderName": properties.get("senderName", "null"),
                                        "id": properties.get("id", "null"),
                                        "zoneid": self.feedid,
                                    }
                                )
                        alerts.sort(key=lambda x: (x['sent'], x['id']), reverse=True)

                    self._state = len(alerts)
                    self._attr = {
                        "alerts": alerts,
                        "integration": "weatheralerts",
                        "state": self.zone_state,
                        "zone": self.feedid,
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
                        self.feedid,
                        self.exception,
                    )

            elif not self.connected:
                if connected:
                    _LOGGER.info("[%s] Update of the sensor completed", self.feedid)
                else:
                    self._state = "unavailable"
                    _LOGGER.debug(
                        "[%s] Still no update (%s)", self.feedid, self.exception
                    )

            self.connected = connected

    @property
    def name(self):
        """Return the name."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID to use for this sensor."""
        return f"weatheralerts_{self.feedid}".replace(",", "")

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
