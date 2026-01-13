# Changelog

  * [Detailed Instructions](https://github.com/custom-components/weatheralerts/blob/master/documentation/DOCUMENTATION.md)
  * [Troubleshooting](https://github.com/custom-components/weatheralerts/blob/master/documentation/TROUBLESHOOTING.md)
  * [Automation Examples](https://github.com/custom-components/weatheralerts/blob/master/documentation/AUTOMATION_EXAMPLES.md)
  * [Lovelace UI Examples](https://github.com/custom-components/weatheralerts/blob/master/documentation/LOVELACE_EXAMPLES.md)
  * [GitHub Repository](https://github.com/custom-components/weatheralerts)
  * [View Issues/Feature Requests](https://github.com/custom-components/weatheralerts/issues)
  * [Report an Issue/Feature Request](https://github.com/custom-components/weatheralerts/issues/new/choose)


## **Changelog**

## [v2026.1.0](https://github.com/custom-components/weatheralerts/blob/master/CHANGELOG.md) (2026-01-12)

**Changes:**

weatheralerts v2026.1.0
  * Finally updated with config and options flow to allow setup and configuration from Home Assistant UI
  * Will attempt to prepopulate the correct zone and county codes during setup using your Home Assistant Home Zone latitude and longitude
  * Configuration options for county/zone/marine codes, sensor update interval, API timeout, deduplication of identical alerts, and custom icon definitions
  * Sensor now includes many of the features used in the YAML packages (i.e. counts for each alert type, alert icons, alert tracking for persistent notifications)
  * Sensor now has an error array that can be used to see when the sensor isn't being updated due to network/internet/api failures or bugs in the integration
  * Deprecrated YAML platform/integration configuration
  * YAML packages are also deprecated and will no longer be maintained
  * Updated documentation
  * Added automation blueprint for easy setup of persistent notifications
  * Added automation example that can be used as a template for additional weather alert notifications (i.e. TTS notifications)
  * Added examples of dashboard cards for displaying the alerts without the need of the YAML package
