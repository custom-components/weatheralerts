# Alert Icon Configuration

> This documentation applies to Weather Alerts version 2026.1.0 and newer.
>  
> Behavior and configuration may differ in earlier versions.

Alert icons may be customized through the integration’s Options menu.

## Capabilities

- Override icons for built-in alert event types
- Add custom event type to icon mappings
- Set a global default icon for unmapped events

The icon settings are not available during the initial config flow setup of the Weather Alerts config entry. Once the initial setup is done, click the gear icon for your new config entry to open the Options Flow configuration. The icon settings are the last page of settings; just click Submit until you get to the icon mappings settings page.

Icons use standard Home Assistant icon definition.

- **Default Icon:** Override for unknown event types (uses Material Design Icons)
- **Custom Event Icons:** Add or edit mappings for specific alert events  
  To add a new event and icon:
    - In `New Event Type` field, enter the new event type such as `UFO Alert`
    - In `New Icon Definition` enter a valid icon definition such as `hass:ufo`
- You can change any existing pre-defined alert event to use whatever valid icon definition you have available
- You can revert a changed icon back to default value by blanking the icon defintion for any changed event types and clicking **Submit**

Once you click **Submit**, the changes apply immediately without needing to restart Home Assistant.

---

## Documentation Navigation

- [Overview](https://github.com/custom-components/weatheralerts/blob/master/documentation/overview.md)
- [Installation](https://github.com/custom-components/weatheralerts/blob/master/documentation/installation.md)
- [Configuration](https://github.com/custom-components/weatheralerts/blob/master/documentation/configuration.md)
- [Sensor Behavior](https://github.com/custom-components/weatheralerts/blob/master/documentation/sensor.md)
- [Alert Tracking](https://github.com/custom-components/weatheralerts/blob/master/documentation/alert_tracking.md)
- [Alert Deduplication](https://github.com/custom-components/weatheralerts/blob/master/documentation/deduplication.md)
- [Alert Icon Configuration](https://github.com/custom-components/weatheralerts/blob/master/documentation/icons.md) **<-- You are here**
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
