# Sensor Behavior

> This documentation applies to Weather Alerts version 2026.1.0 and newer.
>  
> Behavior and configuration may differ in earlier versions.

## Sensor State

The sensor state represents the total number of active alerts.

Example:
  `state: 2`

## Sensor Attributes

### alerts
A list of parsed alert objects from the National Weather Service.

Each alert includes:
- event
- headline
- description
- severity
- urgency
- certainty
- sent
- effective
- onset
- expires
- instruction
- area
- icon

### alert_stats
Computed statistics for currently active alerts, including counts for:
- warnings
- watches
- advisories
- statements
- emergencies
- total active alerts

### alert_tracking
Persistent lifecycle tracking for alert IDs. See [Alert Tracking](https://github.com/custom-components/weatheralerts/blob/master/documentation/alert_tracking.md) link for more details on alert tracking

### zone
The combined feed identifier used for API queries.

### zone_name
Human-readable zone name when available.

### error
Structured error history including most recent successes and failures. See [Error Handling](https://github.com/custom-components/weatheralerts/blob/master/documentation/error_handling.md) link for error handling details.

---

## Documentation Navigation

- [Overview](https://github.com/custom-components/weatheralerts/blob/master/documentation/overview.md)
- [Installation](https://github.com/custom-components/weatheralerts/blob/master/documentation/installation.md)
- [Configuration](https://github.com/custom-components/weatheralerts/blob/master/documentation/configuration.md)
- [Sensor Behavior](https://github.com/custom-components/weatheralerts/blob/master/documentation/sensor.md) **<-- You are here**
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
