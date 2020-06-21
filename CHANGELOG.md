# Changelog

  * [Detailed Instructions](documentation/DOCUMENTATION.md)
  * [Troubleshooting](documentation/TROUBLESHOOTING.md)
  * [YAML Package Info](documentation/YAML_PACKAGES_DOCS.md)
  * [Lovelace UI Examples](documentation/LOVELACE_EXAMPLES.md)
  * [GitHub Repository](https://github.com/custom-components/weatheralerts)
  * [View Issues/Feature Requests](https://github.com/custom-components/weatheralerts/issues)
  * [Report an Issue/Feature Request](https://github.com/custom-components/weatheralerts/issues/new/choose)
  * **Changelog**

## [v0.1.3](https://github.com/custom-components/weatheralerts/tree/v0.1.3) (2020-06-21)

**Changes:**

weatheralerts v0.1.3
  * Update README.md so links will work in HACS

## [v0.1.2](https://github.com/custom-components/weatheralerts/tree/0.1.2) (2020-06-21)

**Changes:**

weatheralerts v0.1.2
  * Update and add documentation
  * Changed default icon from mdi:weather-hurricane to mdi:alert-octagram
  * Simplify alert object sorting; reverse sort alerts by alert ID
  * Tweak logging levels and messages
  * Log sorted alert IDs for debugging purposes
  * Add endsExpire, hailSize, windGust, and waterspoutDetection alert attributes
  * Increase initial setup timeouts from 10 seconds to 20 seconds

weatheralerts YAML packages v0.1.2
  * Various improvements and fixes
  * Add input_text sensors to track triggered alerts
  * Turn off ended alerts (using endsExpire) if weather.gov has extended outage
  * Add additional count attributes to the weatheralerts_*_active_alerts sensor
