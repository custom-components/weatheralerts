# Error Handling and API Fallback

> This documentation applies to Weather Alerts version 2026.1.0 and newer.
>  
> Behavior and configuration may differ in earlier versions.

The integration includes robust error handling for NWS API outages.

## API Outage Behavior

If the API becomes unavailable:
- The last known good data is retained
- Alerts expired for more than 60 minutes are removed
- Error details are stored in the sensor `error` attribute

## Error History

The sensor preserves:
- The most recent successful update
- The most recent failure

This information is available in the `error` attribute.

The `error` attribute is a two element array; `error[0]` and `error[1]`. `error[0]` will always contain the most recent API request status. If it is an error, then `error[1]` will contain the last logged successful API request. If `error[0]` changes from error condition back to a success condition, then `error[1]` will contain the last logged error.

---

## Documentation Navigation

- [Overview](https://github.com/custom-components/weatheralerts/blob/master/documentation/overview.md)
- [Installation](https://github.com/custom-components/weatheralerts/blob/master/documentation/installation.md)
- [Configuration](https://github.com/custom-components/weatheralerts/blob/master/documentation/configuration.md)
- [Sensor Behavior](https://github.com/custom-components/weatheralerts/blob/master/documentation/sensor.md)
- [Alert Tracking](https://github.com/custom-components/weatheralerts/blob/master/documentation/alert_tracking.md)
- [Alert Deduplication](https://github.com/custom-components/weatheralerts/blob/master/documentation/deduplication.md)
- [Alert Icon Configuration](https://github.com/custom-components/weatheralerts/blob/master/documentation/icons.md)
- [Error Handling](https://github.com/custom-components/weatheralerts/blob/master/documentation/error_handling.md) **<-- You are here**
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
