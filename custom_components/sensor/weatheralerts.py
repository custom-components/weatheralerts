"""
A component which allows you to get information about next departure from spesified stop.
For more details about this component, please refer to the documentation at
https://github.com/HalfDecent/HA-Custom_components/weatheralerts
"""

import voluptuous as vol
from datetime import timedelta
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.switch import (PLATFORM_SCHEMA)

__version_ = '0.0.3'

REQUIREMENTS = ['weatheralerts']

CONF_SAMEID = 'sameid'

ATTR_DESTINATION = 'destination'
ATTR_PUBLISHED = 'published'
ATTR_URGENCY = 'urgency'
ATTR_SEVERITY = 'severety'
ATTR_CATEGORY = 'category'
ATTR_TITLE = 'title'
ATTR_SUMMARY = 'summary'
ATTR_LINK = 'link'

SCAN_INTERVAL = timedelta(seconds=30)

ICON = 'mdi:weather-hurricane'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_SAMEID): cv.string,
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    sameid = str(config.get(CONF_SAMEID))
    add_devices([WeatherAlertsSensor(sameid)])

class WeatherAlertsSensor(Entity):
    def __init__(self, sameid):
        self._sameid = sameid
        self.update()

    def update(self):
        from weatheralerts import WeatherAlerts
        nws = WeatherAlerts(samecodes=self._sameid)
        self._published = nws.alerts[0].published
        self._state = nws.alerts[0].event
        self._urgency = nws.alerts[0].urgency
        self._severity = nws.alerts[0].severity
        self._category = nws.alerts[0].category
        self._title = nws.alerts[0].title
        self._summary = nws.alerts[0].summary
        self._link = nws.alerts[0].link
    
    @property
    def name(self):
        return 'WeatherAlerts'

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return ICON

    @property
    def device_state_attributes(self):
        return {
            ATTR_PUBLISHED: self._published,
            ATTR_URGENCY: self._urgency,
            ATTR_SEVERITY: self._severity,
            ATTR_CATEGORY: self._category,
            ATTR_TITLE: self._title,
            ATTR_SUMMARY: self._summary,
            ATTR_LINK: self._link,
        }