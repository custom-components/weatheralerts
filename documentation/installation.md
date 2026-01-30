# Installation

> This documentation applies to Weather Alerts version 2026.1.0 and newer.
>  
> Behavior and configuration may differ in earlier versions.

## Manual Installation

- 1. Download the repository
- 2. Create a `weatheralerts` directory in your Home Assistant `config/custom_components` directory
  - If the `config/custom_components/weatheralerts` directory already exists, delete any files and directories in the existing `weatheralerts` directory
- 3. Copy the repository `custom_components/weatheralerts` directory contents into your Home Assistant `config/custom_components/weatheralerts` directory
- 4. Restart Home Assistant
- 5. Continue with **Step 5** in the **Install via HACS** section below

## Install via HACS (Recommended)

Weather Alerts is included in the default HACS integration list.

- 1. In Home Assistant go to **HACS → Integrations**
- 2. In the search bar at the top of the page, search for **Weather Alerts**
- 3. Install the integration
- 4. Restart Home Assistant after installation
- 5. For new installs (skip this step if you are upgrading from a previous version):
  - Go to **Home Assistant → Settings → Devices & Services → Integrations**
  - Click **Add integration**
  - Search for and select **Weather Alerts**
  - Follow the config flow to finish the configuration. See the [Configuration](https://github.com/custom-components/weatheralerts/blob/master/documentation/configuration.md) link for a config walk-through. 
  - Check out the rest of the documentation to learn more about config options, automations, and dashboard usage

If you are upgrading from a previous version (v0.1.5 or earlier), installing this new version will migrate your YAML weatheralerts platform configuration(s) to the newer config entry system and will be found in the **Home Assistant > Settings > Devices & Services > Weather Alerts** menu after restarting Home Assistant after installing the Weather Alerts update. If you are using the YAML Package files which provides several template sensors and automations to work in conjuntion with the weatheralerts sensor, the migration will not migrate the `sensor.weatheralerts_1` sensor to the new integration. A new sensor will be created and the old sensor will become abandoned. To continue using the YAML Package files (not recommended due to potential failure to get notifications for new alerts) or to continue using your custom automations and dashboard configuration using `sensor.weatheralerts_1`, you will have to delete the abandoned `sensor.weatheralerts_1` sensor and rename the new sensor entity to `sensor.weatheralerts_1`. My recommendation is to use the new automation blueprint (or automation exmaples) and the updated dashboard examples.

To fully upgrade and stop using the YAML config and YAML packages, these are the recommended additional steps:
 - Check **Home Assistant → Settings → Devices & Services → Weather Alerts** menu to ensure your configuration was migrated to a config entry (config entry should be named with your zone/county name and the zone/county codes for your location)
 - Delete your old YAML weatheralerts platform configuration and the YAML package files
 - Restart Home Assistant again
 - Delete any abandoned weatheralerts sensors (the new automations and dashboard examples will not need these extra sensors)
 - Grab the **WeatherAlerts – Persistent Notification and Cleanup** blueprint. Check the [Automation Examples](https://github.com/custom-components/weatheralerts/blob/master/documentation/examples_automations.md) link to see how the automation blueprint works and for other example automations.
 - Check the [Dashboard Examples](https://github.com/custom-components/weatheralerts/blob/master/documentation/examples_dashboard.md) link for examples of how to use the weatheralerts sensor arrays (with no need for YAML Package template sensors)

To fully upgrade and continue using the deprecated YAML Package files, these are the (un)recommended steps:
 - Install this new version of Weather Alerts
 - Restart Home Assistant 
 - Check to ensure Weather Alerts shows in **Home Assistant → Settings → Devices & Services → Integrations**
 - Check **Home Assistant → Settings → Devices & Services → Integrations → Weather Alerts** menu to ensure your configuration was migrated to a config entry (config entry should be named with your zone/county name and the zone/county codes for your location)
 - Delete your old YAML weatheralerts platform configuration but leave the rest of the YAML Package files
 - Delete the abandoned sensor.weatheralerts_1 (and sensor.weatheralerts_2, etc. if you had more than one weatheralerts platform configured)
 - Rename the new weatheralerts sensor entity for each config entry to the appropriate name (sensor.weatheralerts_1, sensor.weatheralerts_2, etc)
 - You're on your own to fix the deprecated YAML package code

---

## Documentation Navigation

- [Overview](https://github.com/custom-components/weatheralerts/blob/master/documentation/overview.md)
- [Installation](https://github.com/custom-components/weatheralerts/blob/master/documentation/installation.md) **<-- You are here**
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
