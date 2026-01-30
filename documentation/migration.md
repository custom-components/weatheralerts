# Migration from YAML Configuration

> This documentation applies to Weather Alerts version 2026.1.0 and newer.
>  
> Behavior and configuration may differ in earlier versions.

YAML-based configuration is deprecated.

Existing YAML configurations, from v0.1.5 and older, are automatically imported into UI-based config entries during startup.

No user interaction is required.

After migration, YAML weatheralerts platform configuration entries may be safely removed. You will get a deprecation warning in the log file until the platform configuration entries are removed from your configuration.yaml or YAML package file. An example of what this entry, that should be deleted, would look like is:

```yaml
sensor:
  platform: weatheralerts
  state: WI
  zone: 38
  county: 87
```

To migrate away from the previously provided YAML package files, replace your dashboard cards that use the YAML package template sensors with one or more of the examples from the [Dashboard Examples](https://github.com/custom-components/weatheralerts/blob/master/documentation/examples_dashboard.md) documentation. Then view the [Automation Examples](https://github.com/custom-components/weatheralerts/blob/master/documentation/examples_automations.md) documentation to replace your persistent notification automation and script with the new automation blueprint. Any other custom automations you have done using the template sensors will need to be fixed to use only the integration sensor. Once your new dashboard card(s) and automation(s) are working, delete the old weatheralerts*.yaml package files.

---

## Documentation Navigation

- [Overview](https://github.com/custom-components/weatheralerts/blob/master/documentation/overview.md)
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
- [Migration from YAML](https://github.com/custom-components/weatheralerts/blob/master/documentation/migration.md) **<-- You are here**
- [Documentation Versioning Policy](https://github.com/custom-components/weatheralerts/blob/master/documentation/versioning.md)

## Support and Issues

- [Support Forum](https://github.com/custom-components/weatheralerts/discussions)
- [GitHub Repository Home](https://github.com/custom-components/weatheralerts)
- [View Issues/Feature Requests](https://github.com/custom-components/weatheralerts/issues)
- [Report an Issue/Feature Request](https://github.com/custom-components/weatheralerts/issues/new/choose)
