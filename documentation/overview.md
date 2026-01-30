# Weather Alerts Integration Overview

> This documentation applies to Weather Alerts version 2026.1.0 and newer.
>  
> Behavior and configuration may differ in earlier versions.

The Weather Alerts integration provides weather alert data from the U.S. National Weather Service (weather.gov) as a Home Assistant sensor.

Alerts are retrieved from the official NWS API and exposed with detailed attributes suitable for dashboards, automations, and notifications.

---

## Version

**Current version:** 2026.1.0

This release represents a significant evolution of the integration and includes:

- UI-only configuration (YAML deprecated)
- Persistent alert tracking across restarts
- Configurable update interval and API timeout
- Optional alert deduplication
- Marine zone support
- Custom alert event icon configuration

**Behavioral Changes in 2026.1.0**

- Alert state and attributes now persist across Home Assistant restarts
- Alert lifecycle tracking has been added directly to the sensor as alert_tracking attribute
- Alert counts have been added directly to the sensor as alert_stats attribute
- Error handling and API fallback behavior have been improved
- Icon configuration has moved to the integration options menu

---

## Features

- Fetches active weather alerts from weather.gov
- Supports public zones, county zones, and marine zones
- Single sensor entity per configured feed
- Sensor state reflects number of active alerts
- Detailed alert data exposed as attributes
- Tracks alert lifecycle (new, old, deleted)
- Persists alert state across Home Assistant restarts
- Optional deduplication of duplicate alerts
- Fully configurable via Home Assistant UI
- Customizable alert icons by event type

---

## Data Source

This integration uses the official National Weather Service API:

- https://api.weather.gov

A custom minimal User-Agent is sent with all requests as required by the NWS API policy.

---

## Documentation Navigation

- [Overview](https://github.com/custom-components/weatheralerts/blob/master/documentation/overview.md) **<-- You are here**
- [Installation](https://github.com/custom-components/weatheralerts/blob/master/documentation/installation.md)
- [Configuration](https://github.com/custom-components/weatheralerts/blob/master/documentation/configuration.md)
- [Sensor Behavior](https://github.com/custom-components/weatheralerts/blob/master/documentation/sensor.md)
- [Alert Tracking](https://github.com/custom-components/weatheralerts/blob/master/documentation/alert_tracking.md)
- [Alert Deduplication](https://github.com/custom-components/weatheralerts/blob/master/documentation/deduplication.md)
- [Alert Icon Configuration](https://github.com/custom-components/weatheralerts/blob/master/documentation/icons.md)
- [Error Handling](https://github.com/custom-components/weatheralerts/blob/master/documentation/error_handling.md)
- [Automation Examples](https://github.com/custom-components/weatheralerts/blob/master/documentation/examples_automations.md)
- [Dashboard Examples](https://github.com/custom-components/weatheralerts/blob/master/documentation/examples_dashboard.md)
- [Troubleshooting](https://github.com/custom-components/weatheralerts/blob/master/documentation/troubleshooting.md)
- [Migration from YAML](https://github.com/custom-components/weatheralerts/blob/master/documentation/migration.md)
- [Documentation Versioning Policy](https://github.com/custom-components/weatheralerts/blob/master/documentation/versioning.md)

## Support and Issues

- [Support Forum](https://github.com/custom-components/weatheralerts/discussions)
- [GitHub Repository Home](https://github.com/custom-components/weatheralerts)
- [View Issues/Feature Requests](https://github.com/custom-components/weatheralerts/issues)
- [Report an Issue/Feature Request](https://github.com/custom-components/weatheralerts/issues/new/choose)
