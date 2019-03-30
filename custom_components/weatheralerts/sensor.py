"""
A component which allows you to get information about next departure from spesified stop.
For more details about this component, please refer to the documentation at

https://github.com/custom-components/sensor.weatheralerts
"""
from datetime import timedelta
import voluptuous as vol
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.switch import PLATFORM_SCHEMA

VERSION = "0.1.0"

REQUIREMENTS = ["weatheralerts"]

CONF_SAMEID = "sameid"

SCAN_INTERVAL = timedelta(seconds=30)

ICON = "mdi:weather-hurricane"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({vol.Required(CONF_SAMEID): cv.string})


def setup_platform(hass, config, add_devices, discovery_info=None):
    sameid = str(config.get(CONF_SAMEID))
    add_devices([WeatherAlertsSensor(sameid)], True)


class WeatherAlertsSensor(Entity):
    def __init__(self, sameid):
        self._sameid = sameid
        self._state = None
        self._attr = {}

    def update(self):
        from weatheralerts import WeatherAlerts

        try:
            nws = WeatherAlerts(samecodes=self._sameid)
            last_event = nws.alerts[0]
        except Exception:
            last_event = {}
        for item in last_event:
            if item == "event":
                self._state = last_event.get(item)
            else:
                self._attr[item] = last_event.get(item)

    @property
    def name(self):
        return "WeatherAlerts"

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return ICON

    @property
    def device_state_attributes(self):
        return self._attr
