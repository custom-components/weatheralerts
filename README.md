# An integration to get weather alerts from weather.gov

[![GitHub release (latest by date)][release-badge]][release-link]  [![GitHub][license-badge]][license-link]  [![hacs_badge][hacs-badge]][hacs-link]

[![GitHub stars][stars-badge]][stars-link]  ![GitHub][maintained-badge]  [![GitHub issues][issues-badge]][issues-link]  [![GitHub commits since latest release (by SemVer)][commits-badge]][commits-link]

> This documentation applies to Weather Alerts version 2026.1.0 and newer.
>  
> Behavior and configuration may differ in earlier versions.

# Breaking changes

### v2026.1.0
 * This new version will migrate your YAML integration platform config to the new config flow automatically and create a new sensor. It will NOT migrate or re-use your old sensor (i.e. sensor.weatheralerts_1 or sensor.zone_name) and it will generate a new sensor named using data from your zone name and zone/county/marine codes. If you want to continue using the YAML package (not recommended) for its template sensors and automations, it should still be compatible; but you will need to delete the old sensor.weatheralerts_1 sensor entity and rename the new weatheralerts integration sensor entity to sensor.weatheralerts_1. This renaming is not require if you plan to use the new automation and dashboard examples. I highly recommend using the new automation and dashboard examples and to stop using the old YAML package due to the possibility of missed alert notifications.


# Upgrading

If you are upgrading from a previous version (v0.1.5 or earlier), installing this new version will migrate your YAML weatheralerts platform configuration(s) to the newer config entry system and will be found in the **Home Assistant → Settings → Devices & Services → Integrations → Weather Alerts** menu. If you are using the YAML Package files which provides several template sensors and automations to work in conjuntion with the weatheralerts sensor, the migration will not migrate the sensor.weatheralerts_1 sensor to the new integration. A new sensor will be created and the old sensor will become abandoned. To continue using the YAML Package files (not recommended due to potential failure to get notifications for new alerts) or to continue using your custom automations and dashboard configuration using sensor.weatheralerts_1, you will have to delete the abandoned sensor.weatheralerts_1 sensor and rename the new sensor entity to sensor.weatheralerts_1. My recommendation is to use the new automation blueprint (or automation exmaples) and the updated dashboard examples.

To fully upgrade and stop using the YAML config and YAML packages, these are the recommended steps:
 * Install this new version of Weather Alerts
 * Restart Home Assistant 
 * Check to ensure Weather Alerts shows in **Home Assistant → Settings → Devices & Services → Integrations**
 * Check **Home Assistant → Settings → Devices & Services → Integrations → Weather Alerts** menu to ensure your configuration was migrated to a config entry (config entry should be named with your zone/county name and the zone/county codes for your location)
 * Delete your old YAML weatheralerts platform configuration and the YAML package files
 * Restart Home Assistant again
 * Delete any abandoned weatheralerts sensors (the new automations and dashboard examples should not need these extra sensors)
 * Grab the Weather Alerts Persistent Automation blueprint or check the Automation Examples link to see how the blueprint works and for other example automations
 * Check the Dashboard Examples link for examples of how to use the weatheralerts sensor arrays (with no need for YAML Package template sensors)

To fully upgrade and continue using the deprecated YAML Package files, these are the unrecommended steps:
 * Install this new version of Weather Alerts
 * Restart Home Assistant 
 * Check to ensure Weather Alerts shows in **Home Assistant → Settings → Devices & Services → Integrations**
 * Check **Home Assistant → Settings → Devices & Services → Integrations → Weather Alerts** menu to ensure your configuration was migrated to a config entry (config entry should be named with your zone/county name and the zone/county codes for your location)
 * Delete your old YAML weatheralerts platform configuration but leave the rest of the YAML Package files
 * Delete the abandoned sensor.weatheralerts_1 (and sensor.weatheralerts_2, etc. if you had more than one weatheralerts platform configured)
 * Rename the new weatheralerts sensor entity for each config entry to the appropriate name (sensor.weatheralerts_1, sensor.weatheralerts_2, etc)


# Installing and Using Weather Alerts Integration

## Manual Installation

Check the [Installation](https://github.com/custom-components/weatheralerts/blob/master/documentation/installation.md) documentation for full manual installation instructions.

## New Installation Quickstart (via HACS & Home Assistant UI)

### 1. Install via HACS

- In Home Assistant, go to **HACS → Integrations**
- Search for **Weather Alerts** and click **Install**
- **Restart Home Assistant** after installation

### 2. Add the Integration

- In Home Assistant, go to **Settings → Devices & Services → Integrations**
- Click **+ Add Integration**, search for **Weather Alerts**, and select it

### 3. Initial Setup via Config Flow

1. **Location**  
   - Enter your latitude and longitude (or use the prepopulated suggested values from your `zone.home`). The lat/lon should be entered as numbers only (no degree symbol or cardinal direction appended); in the United States the latitude will be a positive number and longitude will be a negative number. This lat/lon will be used to automatically fetch your zone and county code and prepopulate those fields in the next config step. If you leave the lat/lon fields blank, you will need to find your codes; just ask Google search:
     - what is the nws zone and county code for _city_, _state_

   In the Google search, just replace _city_ and _state_ with your city and state. Google should reply with a NWS zone Code that is 3 letters (State abbreviatation + Z) + 3 numbers (xxZ###) and you should also see a 3 letter (State abbreviation + C) + 3 numbers (xxC###) county code listed under FIPS County Code.

2. **Zone and County Selection**
   - **Zone Code:** Required. 
     - Example: `WIZ038`
   - **County Code:** *(Optional)*
     - Example: `WIC087`
   - **Marine Zones:** *(Optional, comma-separated)*
     - Marine zone lookup here: https://www.weather.gov/marine/wrdoffmz   
     - Example: `LMZ043,LMZ080`

3. **Sensor Update Settings**
   - **Sensor Update Interval:** Default: `90` seconds (range: `30 - 600`)
   - **API Request Timeout:** Default: `20` seconds (range: `10 - 60`, must be at least 5 seconds less than the update interval)

> Once setup is complete, the integration will create a sensor (e.g., `sensor.weatheralerts_outagamie_wiz038` with friendly name like `Outagamie (WIZ038)`) and automatically fetch current NWS weather alerts for your configured area. If you don't want land-based alerts with marine alerts, you can create a config entry for just a marine zone by entering the marine zone code in the Zone Code field and leaving the other fields blank or one marine zone code in the Zone Code field and additional marine zone codes in the Marine Zones field. 

---

## Usage & Configuration Guide (Options Flow)

You can change any settings after installation using the integration's options flow:

1. Go to **Settings → Devices & Services → Integrations**
2. Click the Weather Alerts integration
3. Click the gear icon for the config entry you want to configure

### Editable Options

- **Zone Code:** Your main NWS zone (e.g., `WIZ038`)
- **County Code:** *(Optional)* More specific NWS county (e.g., `WIC087`)
- **Marine Zones:** *(Optional)* Comma-separated NWS marine or public zone codes (e.g., `LMZ043,LMZ080`)

#### Sensor Update Settings

- **Sensor Update Interval:** How often to fetch new alerts (30 - 600 seconds)
- **API Request Timeout:** How long to wait for NWS API response (10 - 60 seconds, at least 5 seconds less than update interval)

#### Configure Alert Icons

- Alert icons can be customized via the integration options menu. See [Alert Icon Configuration](https://github.com/custom-components/weatheralerts/blob/master/documentation/icons.md) for more details.


For advanced configuration, automation and dashboard examples, and troubleshooting, see the full documentation linked below.

---

## Additional Notes

- **No YAML configuration needed:** All setup and changes are handled through the Home Assistant UI.
- **No YAML package(s) needed:** Sensor contains everything needed for automations and dashboard usage.
- **Live validation:** All codes are validated during entry.
- **Monitor multiple sources:** You can track land and marine zones together or seperately with multiple config entries.
- **Error Handling:** User-friendly error messages are shown if you enter invalid codes or encounter API issues.

---

## Need Help?

For troubleshooting steps and debug logging instructions, see the [Troubleshooting](https://github.com/custom-components/weatheralerts/blob/master/documentation/troubleshooting.md) documentation.

- [Support Forum](https://github.com/custom-components/weatheralerts/discussions)
- [GitHub Repository Home](https://github.com/custom-components/weatheralerts)
- [View Issues/Feature Requests](https://github.com/custom-components/weatheralerts/issues)
- [Report an Issue/Feature Request](https://github.com/custom-components/weatheralerts/issues/new/choose)
- Check the **Links** below for more detailed instructions, troubleshooting, and for automation and dashboard examples.


# Updating via HACS

Check the **Breaking Changes** section of this README to see if any special attention is needed before or after updating the integration. Simply use the **Update** button for the *weatheralerts* integration within *HACS* if there are no breaking changes and then restart Home Assistant. If there are significant breaking changes, take a backup, check the breaking changes and plan your update accordingly, and then use the **Update** button for the *weatheralerts* integration within *HACS* to start the update process.


# Links

Full documentation for the Weather Alerts integration is available in the repository:

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
- [Migration from YAML](https://github.com/custom-components/weatheralerts/blob/master/documentation/migration.md)
- [Documentation Versioning Policy](https://github.com/custom-components/weatheralerts/blob/master/documentation/versioning.md)

>Deprecated:
>  * [YAML Package Info](https://github.com/custom-components/weatheralerts/blob/master/documentation/YAML_PACKAGES_DOCS.md)



# Todo list
- [x] Add more documentation
- [x] Add config flow to allow UI-based configuration (eliminate yaml-based platform configuration)
- [x] Create alternative (possibly simpler) YAML package or move some template sensors into the integration
- [ ] Add backup weather alert source for occasions when weather.gov alerts api is experiencing an outage
- [ ] Add Canadian weather alerts


[release-badge]: https://img.shields.io/github/v/release/custom-components/weatheralerts?style=plastic
[release-link]: https://github.com/custom-components/weatheralerts/releases
[license-badge]: https://img.shields.io/github/license/custom-components/weatheralerts?style=plastic
[license-link]: https://github.com/custom-components/weatheralerts/blob/master/LICENSE
[hacs-badge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=plastic
[hacs-link]: https://github.com/hacs/integration
[stars-badge]: https://img.shields.io/github/stars/custom-components/weatheralerts?style=plastic
[stars-link]: https://github.com/custom-components/weatheralerts/stargazers
[maintained-badge]: https://img.shields.io/maintenance/yes/2026.svg?style=plastic
[issues-badge]: https://img.shields.io/github/issues/custom-components/weatheralerts?style=plastic
[issues-link]: https://github.com/custom-components/weatheralerts/issues
[commits-badge]: https://img.shields.io/github/commits-since/custom-components/weatheralerts/latest?style=plastic
[commits-link]: https://github.com/custom-components/weatheralerts/commits/master


