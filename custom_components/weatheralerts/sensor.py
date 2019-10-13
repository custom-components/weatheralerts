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
from weatheralerts import WeatherAlerts

CONF_SAMEID = "sameid"

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({vol.Required(CONF_SAMEID): cv.string})


def setup_platform(
    hass, config, add_entities, discovery_info=None
):  # pylint: disable=missing-docstring, unused-argument
    add_entities([WeatherAlertsSensor(str(config.get(CONF_SAMEID)))], True)


class WeatherAlertsSensor(Entity):  # pylint: disable=missing-docstring
    def __init__(self, sameid):
        self.sameid = sameid
        self._state = None
        self._attr = {}
        _LOGGER.info("Added sensor with sameid '%s'", sameid)

    def update(self):
        """Run update."""
        new = {"state": None, "attributes": {}}

        # Attach nws
        try:
            nws = WeatherAlerts(samecodes=self.sameid)
        except Exception as exeption:  # pylint: disable=broad-except
            nws = None
            _LOGGER.error(exeption)

        if nws is None:
            return

        # Get alerts
        try:
            alerts = nws.alerts
        except Exception as exeption:  # pylint: disable=broad-except
            alerts = None

        if not isinstance(alerts, list):
            return

        # Get last event
        try:
            last_event = alerts[0]
        except Exception as exeption:  # pylint: disable=broad-except
            last_event = None

        if last_event is None:
            return

        try:
            new["state"] = last_event.event
        except Exception as exeption:  # pylint: disable=broad-except
            _LOGGER.debug(exeption)
        try:
            new["attributes"]["published"] = last_event.published
        except Exception as exeption:  # pylint: disable=broad-except
            _LOGGER.debug(exeption)
        try:
            new["attributes"]["urgency"] = last_event.urgency
        except Exception as exeption:  # pylint: disable=broad-except
            _LOGGER.debug(exeption)
        try:
            new["attributes"]["category"] = last_event.category
        except Exception as exeption:  # pylint: disable=broad-except
            _LOGGER.debug(exeption)
        try:
            new["attributes"]["title"] = last_event.title
        except Exception as exeption:  # pylint: disable=broad-except
            _LOGGER.debug(exeption)
        try:
            new["attributes"]["summary"] = last_event.summary
        except Exception as exeption:  # pylint: disable=broad-except
            _LOGGER.debug(exeption)
        try:
            new["attributes"]["link"] = last_event.link
        except Exception as exeption:  # pylint: disable=broad-except
            _LOGGER.debug(exeption)

        self._state = new.get("state")
        self._attr = new.get("attributes", {})

    @property
    def name(self):
        """Return the name."""
        return "WeatherAlerts"

    @property
    def state(self):
        """Return the state."""
        if self._state is None:
            return "No alerts"
        return self._state

    @property
    def icon(self):
        """Return icon."""
        return "mdi:weather-hurricane"

    @property
    def device_state_attributes(self):
        """Return attributes."""
        return self._attr
