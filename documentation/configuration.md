# Configuration

> This documentation applies to Weather Alerts version 2026.1.0 and newer.
>  
> Behavior and configuration may differ in earlier versions.

YAML configuration is deprecated and no longer supported for new setups.

All configuration is performed through the Home Assistant UI.

## Configuration Flow

On initial installation and on setup of new config entries, you will be presented with a config flow to setup the Weather Alerts integration.

### Step 1: Location (Optional)

If you have a Home zone configured in Home Assistant, the integration will prepopulate your latitude and longitude using your Home zone configuration.

If latitude and longitude are not prepopulated, you may be provide your latitude and longitude and the integration will attempt to automatically determine the appropriate NWS forecast zone and county codes for you in the next step of the config flow.

If latitude and longitude are not prepopulated, this step may be skipped by leaving the latitude and longitude fields blank, to manually enter zone and county codes in the next step of the config flow.

The latitude and longitude should be entered as numbers only (no degree symbol or cardinal direction appended); in the United States the latitude will be a positive number and longitude will be a negative number. If you leave the latitude and longitude fields blank, you will need to find your codes; just ask Google search:
- what is the nws zone and county code for _city_, _state_

In the Google search, just replace _city_ and _state_ with your city and state. Google should reply with a NWS zone Code that is 3 letters (State abbreviatation + Z) + 3 numbers (xxZ###) and you should also see a 3 letter (State abbreviation + C) + 3 numbers (xxC###) county code listed under FIPS County Code.

### Step 2: Zone Selection

- Zone Code (required)
  Example: WIZ038
- County Code (optional)
  Example: WIC087
- Marine Zones (optional, comma-separated)
  Example: LMZ043,LMZ080

Multiple zone types may be combined into a single sensor.

### Step 3: Sensor Update Settings

- Update Interval: 30–600 seconds
- API Timeout: 10–60 seconds
  Must be at least 5 seconds less than the update interval
- Deduplicate Alerts (optional)

Changes take effect immediately after submitting.

After the initial setup of a Weather Alerts config entry is done, you can click the gear icon of your new config entry to bring up the options flow. The options flow configuration will allow you to reconfigure the existing config entry settings (the settings from the config flow above) and will also allow you to add or change any alert event icons. See [Alert Icon Configuration](https://github.com/custom-components/weatheralerts/blob/master/documentation/icons.md) for details.

---

## Documentation Navigation

- [Overview](https://github.com/custom-components/weatheralerts/blob/master/documentation/overview.md)
- [Installation](https://github.com/custom-components/weatheralerts/blob/master/documentation/installation.md)
- [Configuration](https://github.com/custom-components/weatheralerts/blob/master/documentation/configuration.md) **<-- You are here**
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
