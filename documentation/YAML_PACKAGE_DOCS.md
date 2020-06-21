# YAML Package Info

  * [Detailed Instructions](https://github.com/custom-components/documentation/DOCUMENTATION.md)
  * [Troubleshooting](https://github.com/custom-components/documentation/TROUBLESHOOTING.md)
  * **YAML Package Info**
  * [Lovelace UI Examples](https://github.com/custom-components/documentation/LOVELACE_EXAMPLES.md)
  * [GitHub Repository](https://github.com/custom-components/weatheralerts)
  * [View Issues/Feature Requests](https://github.com/custom-components/weatheralerts/issues)
  * [Report an Issue/Feature Request](https://github.com/custom-components/weatheralerts/issues/new/choose)
  * [Changelog](https://github.com/custom-components/CHANGELOG.md)


## YAML Package Setup
 An alternative is to use YAML packages (recommended) by adding `packages:` to the homeassistant section of your configuration.yaml. Like this:

```
homeassistant:
  ...
  other config options here...
  ...
  packages: !include_dir_named packages
```

Add `packages: !include_dir_named packages` to the `homeassistant:` section, create a directory named packages in the root of your Home Assistant configuration directory (where your configuration.yaml is located). See [Home Assistant Packages](https://www.home-assistant.io/docs/configuration/packages/) for more info on how to setup and use yaml packages. 


## YAML Package Installation
Sample yaml packages are included in the repository packages directory [https://github.com/custom-components/weatheralerts/packages/](https://github.com/custom-components/weatheralerts/packages/). The yaml packages currently available:
* **weatheralerts.yaml** - includes the main weatheralerts sensor platform configuration. If you already have the weatheralerts platform configured elsewhere, you won't need this.
* **weatheralerts_1.yaml** - rename your first weatheralerts platform sensor entity ID to `sensor.weatheralerts_1` to use this yaml package which includes template sensors for up to 5 active alerts and a script and automations to handle UI notifications.
* **weatheralerts_2.yaml** - rename your second weatheralerts platform sensor entity ID to `sensor.weatheralerts_2` to use this yaml package which includes template sensors for up to 5 active alerts and a script and automations to handle UI notifications.

The yaml packages have some documentation included in them.


## YAML Package Usage

(coming soon)
