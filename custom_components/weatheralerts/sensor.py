"""
A component which allows you to get information about next departure from spesified stop.
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

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_STATE): cv.string, vol.Required(CONF_ZONE): cv.string}
)

URL = "https://api.weather.gov/alerts/active?zone={}"

HEADERS = {
    "accept": "application/ld+json",
    "user-agent": f"HomeAssistant/{__version__}",
}


async def async_setup_platform(
    hass, config, add_entities, discovery_info=None
):  # pylint: disable=missing-docstring, unused-argument
    state = config[CONF_STATE]
    zone = config[CONF_ZONE]

    if len(zone) == 1:
        zone = f"00{zone}"
    elif len(zone) == 2:
        zone = f"0{zone}"
    elif len(zone) == 3:
        zoneid = f"{state}Z{zone}"
    elif len(zone) >= 6:
        zoneid = f"{zone}"
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

    except Exception as exception:  # pylint: disable=broad-except
        _LOGGER.error("[%s] %s", sys.exc_info()[0].__name__, exception)
        return False

    if len(zone) <= 6:
        name = data["title"].split("advisories for ")[1].split(" (")[0]
    if len(zone) > 6:
        name = f"weatheralerts_{zoneid}"
        name = name.replace(",", "_")

    add_entities([WeatherAlertsSensor(name, state, zoneid, session)], True)
    _LOGGER.info("Added sensor with zoneid '%s'", zoneid)


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
                data = await response.json()

                if data.get("features") is not None:
                    for alert in data["features"]:
                        if alert.get("properties") is not None:
                            properties = alert["properties"]
                            alerts.append(
                                {
                                    "area": properties["areaDesc"],
                                    "certainty": properties["certainty"],
                                    "description": properties["description"],
                                    "ends": properties["ends"],
                                    "event": properties["event"],
                                    "instruction": properties["instruction"],
                                    "response": properties["response"],
                                    "sent": properties["sent"],
                                    "severity": properties["severity"],
                                    "title": properties["headline"].split(" issued ")[
                                        0
                                    ],
                                    "urgency": properties["urgency"],
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
                    _LOGGER.error(
                        "[%s] Could not update the sensor (%s)",
                        self.zoneid,
                        self.exception,
                    )

            elif not self.connected:
                if connected:
                    _LOGGER.info("[%s] Update of the sensor completed", self.zoneid)
                else:
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
        """Return a unique ID to use for this binary_sensor."""
        if len(self.zoneid) > 6:
            uniqueid = self.zoneid.replace(",", "_")
        else:
            uniqueid = self.zoneid
        return f"weatheralerts_{uniqueid}"

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
