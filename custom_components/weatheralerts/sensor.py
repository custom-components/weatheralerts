"""
A component which allows you to get information about next departure from spesified stop.
For more details about this component, please refer to the documentation at

https://github.com/custom-components/sensor.weatheralerts
"""
from datetime import timedelta
import logging
import voluptuous as vol
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.switch import PLATFORM_SCHEMA

CONF_SAMEID = "sameid"

SCAN_INTERVAL = timedelta(seconds=30)

ICON = "mdi:weather-hurricane"

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({vol.Required(CONF_SAMEID): cv.string})


async def async_setup_platform(
    hass, config, async_add_entities, discovery_info=None
):  # pylint: disable=missing-docstring, unused-argument
    sameid = str(config.get(CONF_SAMEID))
    async_add_entities([WeatherAlertsSensor(sameid)], True)


class WeatherAlertsSensor(Entity):  # pylint: disable=missing-docstring
    def __init__(self, sameid):
        self._sameid = sameid
        self._state = None
        self._attr = {}

    async def async_update(self):  # pylint: disable=missing-docstring
        from weatheralerts import WeatherAlerts

        current = {"state": self._state, "attributes": self._attr}

        try:
            nws = None
            last_event = None
            try:
                nws = WeatherAlerts(samecodes=self._sameid)
            except Exception as error:  # pylint: disable=broad-except
                _LOGGER.error(error)
            if nws is None:
                try:
                    nws = WeatherAlerts(samecodes=self._sameid)
                except Exception as error:  # pylint: disable=broad-except
                    _LOGGER.error(error)
            if nws is None:
                try:
                    nws = WeatherAlerts(samecodes=self._sameid)
                except Exception as error:  # pylint: disable=broad-except
                    _LOGGER.error(error)
            if nws is None:
                try:
                    nws = WeatherAlerts(samecodes=self._sameid)
                except Exception as error:  # pylint: disable=broad-except
                    _LOGGER.error(error)
            if nws is None:
                try:
                    nws = WeatherAlerts(samecodes=self._sameid)
                except Exception as error:  # pylint: disable=broad-except
                    _LOGGER.error(error)
            last_event = nws.alerts[0]
            if last_event is not None:
                try:
                    self._state = last_event.event
                except Exception as error:  # pylint: disable=broad-except
                    _LOGGER.error(error)
                try:
                    self._attr["published"] = last_event.published
                except Exception as error:  # pylint: disable=broad-except
                    _LOGGER.error(error)
                try:
                    self._attr["urgency"] = last_event.urgency
                except Exception as error:  # pylint: disable=broad-except
                    _LOGGER.error(error)
                try:
                    self._attr["category"] = last_event.category
                except Exception as error:  # pylint: disable=broad-except
                    _LOGGER.error(error)
                try:
                    self._attr["title"] = last_event.title
                except Exception as error:  # pylint: disable=broad-except
                    _LOGGER.error(error)
                try:
                    self._attr["summary"] = last_event.summary
                except Exception as error:  # pylint: disable=broad-except
                    _LOGGER.error(error)
                try:
                    self._attr["link"] = last_event.link
                except Exception as error:  # pylint: disable=broad-except
                    _LOGGER.error(error)
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.error(error)
            self._state = current.get("state")
            self._attr = current.get("attributes")

    @property
    def name(self):  # pylint: disable=missing-docstring
        return "WeatherAlerts"

    @property
    def state(self):  # pylint: disable=missing-docstring
        return self._state

    @property
    def icon(self):  # pylint: disable=missing-docstring
        return ICON

    @property
    def device_state_attributes(self):  # pylint: disable=missing-docstring
        return self._attr
