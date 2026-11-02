# Alert Deduplication

> This documentation applies to Weather Alerts version 2026.1.0 and newer.
>  
> Behavior and configuration may differ in earlier versions.

Alert deduplication is optional and can be performed in two different ways.

## NWS Alert ID Deduplication (Recommended)

When enabled, alerts with the same NWS alert ID are treated as the same alert and only the first copy is retained.

This is useful when a sensor monitors overlapping zone types, such as a public forecast zone and a county zone, because the NWS API can return the same alert more than once when it applies to multiple requested zones.

Alerts without a usable ID are always preserved and are not deduplicated by this option.

NWS alert ID deduplication is disabled by default for backward compatibility.

## Description Deduplication (Not Recommended)

When enabled, alerts with identical descriptions are grouped together internally.

The integration processes the internally grouped duplicates and retains a single alert using the following priority:

1. Newest sent timestamp
2. Latest expires timestamp
3. Highest alert ID

Description deduplication is disabled by default and is not recommended unless the user understands the implications.

The implication is the potential for severe weather alerts not triggering a notification if a new alert is omitted from the sensor as a duplicate. While it _shouldn't_ happen, there are absolutely no guarantees that it won't happen.

If both options are enabled, NWS alert ID deduplication is applied first, followed by description deduplication.

---

## Documentation Navigation

- [Overview](https://github.com/custom-components/weatheralerts/blob/master/documentation/overview.md)
- [Installation](https://github.com/custom-components/weatheralerts/blob/master/documentation/installation.md)
- [Configuration](https://github.com/custom-components/weatheralerts/blob/master/documentation/configuration.md)
- [Sensor Behavior](https://github.com/custom-components/weatheralerts/blob/master/documentation/sensor.md)
- [Alert Tracking](https://github.com/custom-components/weatheralerts/blob/master/documentation/alert_tracking.md)
- [Alert Deduplication](https://github.com/custom-components/weatheralerts/blob/master/documentation/deduplication.md) **<-- You are here**
- [Alert Icon Configuration](https://github.com/custom-components/weatheralerts/blob/master/documentation/icons.md)
- [Error Handling](https://github.com/custom-components/weatheralerts/blob/master/documentation/error_handling.md)
- [Automation Examples](https://github.com/custom-components/weatheralerts/blob/master/documentation/examples_automations.md)
- [Dashboard Examples](https://github.com/custom-components/weatheralerts/blob/master/documentation/examples_dashboard.md)
- [Alert Card](https://github.com/custom-components/weatheralerts/blob/master/documentation/alert_card.md)
- [Troubleshooting](https://github.com/custom-components/weatheralerts/blob/master/documentation/troubleshooting.md)
- [Migration from YAML](https://github.com/custom-components/weatheralerts/blob/master/documentation/migration.md)
- [Documentation Versioning Policy](https://github.com/custom-components/weatheralerts/blob/master/documentation/versioning.md)

## Support and Issues

- [Support Forum](https://github.com/custom-components/weatheralerts/discussions)
- [GitHub Repository Home](https://github.com/custom-components/weatheralerts)
- [View Issues/Feature Requests](https://github.com/custom-components/weatheralerts/issues)
- [Report an Issue/Feature Request](https://github.com/custom-components/weatheralerts/issues/new/choose)
