# YAML Package Info

Note: Don't forget to *Star* or *Watch* the *weatheralerts* GitHub repository so you can get notifications when the YAML packages are updated in between releases!

  * [Detailed Instructions](DOCUMENTATION.md)
  * [Troubleshooting](TROUBLESHOOTING.md)
  * **YAML Package Info**
  * [Lovelace UI Examples](LOVELACE_EXAMPLES.md)
  * [GitHub Repository](https://github.com/custom-components/weatheralerts)
  * [View Issues/Feature Requests](https://github.com/custom-components/weatheralerts/issues)
  * [Report an Issue/Feature Request](https://github.com/custom-components/weatheralerts/issues/new/choose)
  * [Changelog](/CHANGELOG.md)


## YAML Package Setup
The YAML packages provided here are not required for the weatheralerts integration to function. They contain scripts, automations, and some template sensors to make the automations a bit simpler and easier to follow.

Instead of configuring sensors/packages/integrations directly inside of configuration.yaml, an alternative is to use YAML packages (recommended for large or complex Home Assistant setups) by adding `packages:` to the homeassistant section of your configuration.yaml. Like this:

```
homeassistant:
  ...
  other config options here...
  ...
  packages: !include_dir_named packages
```

Add `packages: !include_dir_named packages` to the `homeassistant:` section, create a directory named packages in the root of your Home Assistant configuration directory (where your configuration.yaml is located). See [Home Assistant Packages](https://www.home-assistant.io/docs/configuration/packages/) for more info on how to setup and use yaml packages. 


## YAML Package Installation
Sample yaml packages are included in the repository packages directory [https://github.com/custom-components/weatheralerts/packages/](https://github.com/custom-components/weatheralerts/tree/master/packages). The yaml packages currently available:
* **weatheralerts.yaml** - includes the main weatheralerts sensor platform configuration. If you already have the weatheralerts platform configured elsewhere, you won't need this.
* **weatheralerts_1.yaml** - rename your first weatheralerts platform sensor entity ID to `sensor.weatheralerts_1` to use this yaml package which includes template sensors for up to 5 active alerts and a script and automations to handle UI notifications.
* **weatheralerts_2.yaml** - rename your second weatheralerts platform sensor entity ID to `sensor.weatheralerts_2` to use this yaml package which includes template sensors for up to 5 active alerts and a script and automations to handle UI notifications.

The yaml packages have some documentation included in them.

The weatheralerts_1.yaml and weatheralerts_2.yaml packages will eventually be deprecated, or greatly simplified.


## Troubleshooting

If you have made any changes or customizations to the YAML packages, double check your changes. YAML is very sensitive to format and syntax. Improper indentation or something missing or added in the wrong place will result in a configuration error and Home Assistant will start in safe mode if the problem is not fixed.

Template errors or warnings in your log file are not necessarily a cause for concern. Due to YAML packages potentially being loaded before the weatheralerts integration, there may be template related errors or warnings logged early in the log file while Home Assistant is starting up. Excessive template errors or warnings may be logged if the weatheralerts integration fails to load due to an incorrect state or zone configuration or due to a NWS alert API outage. 

If you are seeing a bunch of template errors or warnings in your log file, you can suppress them using the filter feature of the `logger:` configuration in your configuration.yaml. If you don't have a `logger:` section in your configuration.yaml file, it should look something like this:

```
logger:
  default: warning
  filters:
    homeassistant.helpers.template_entity:
      - "weatheralerts"
    homeassistant.components.template.template_entity:
      - "weatheralerts"
    homeassistant.helpers.template:
      - "weatheralerts"
    homeassistant.helpers.sensor:
      - "weatheralerts"
```

My `logger:` configuration section is placed below the `recorder:` section in the configuration.yaml file. If you already have a `logger:` section, just copy the `filters:` section (or just the filter entries if you have a `filters:` section) and add it to your `logger:` configuration.
