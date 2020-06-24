# An integration to get weather alerts from weather.gov

[![GitHub release (latest by date)][release-badge]][release-link]  [![GitHub][license-badge]][license-link]  [![hacs_badge][hacs-badge]][hacs-link]

[![GitHub stars][stars-badge]][stars-link]  ![GitHub][maintained-badge]  [![GitHub issues][issues-badge]][issues-link]  [![GitHub commits since latest release (by SemVer)][commits-badge]][commits-link]


# Breaking changes

### v0.1.2
 * The [YAML packages](https://github.com/custom-components/weatheralerts/blob/master/documentation/YAML_PACKAGES_DOCS.md) currently available for *weatheralerts v0.1.2* are not compatible with prior versions of *weatheralerts*. Older YAML packages should still work with *weatheralerts v0.1.2*, however, the most recent YAML package files contain new features and fixes.


# Installation Quickstart

This qickstart install guide assumes you are already familiar with custom component installation and with the Home Assistant YAML configuration. If you need more detailed step-by-step instructions, check the links at the bottom for detailed instructions. Troubleshooting information, weatheralerts YAML package information, and Lovelace UI examples are also included in the **Links** at the bottom.

Install the *weatheralerts* integration via *HACS*. After installing via *HACS*, don't restart Home Assistant yet. We will do that after completing the YAML platform configuration.

You will need to find your zone and county codes by looking for your state or marine zone at [https://alerts.weather.gov/](https://alerts.weather.gov/). Once you find your state or marine zone, click into the **Zone List** and **County List** links and find the **Zone Code** and **County Code** your county. All you need are just the first two letters (your state or marine zone abbreviation) and the last three digits (zone/county ID number) of your zone code and county code to put into the platform configuration. The zone and county ID numbers are not usually the same number, so be sure to look up both codes. 

Once installed and you have your state (or marine zone) abbreviation and ID numbers, add the weatheralerts sensor platform to your configuration. If your state is Wisconsin and your county is Outagamie, then the state abbreviation is `WI`, the zone ID number is `038`, and the county ID number is `087`. For the ID numbers, remove any leading zeros and your YAML platform configuration would look something like this:
```yaml
sensor:
  platform: weatheralerts
  state: WI
  zone: 38
  county: 87
```
Once your configuration is saved, restart Home Assistant. 

That completes the integration (custom component) installation.

Check the **Links** below for more detailed instructions, troubleshooting, and for YAML package and Lovelace UI usage and examples.


# Updating via HACS

Check the **Breaking Changes** section of this README to see if you need to manually update the YAML packages or make any changes to your custom YAML or Lovelace UI cards. Simply use the **Update** button for the *weatheralerts* integration within *HACS* if there are no breaking changes and then restart Home Assistant. 


# Links

  * [Detailed Instructions](https://github.com/custom-components/weatheralerts/blob/master/documentation/DOCUMENTATION.md)
  * [Troubleshooting](https://github.com/custom-components/weatheralerts/blob/master/documentation/TROUBLESHOOTING.md)
  * [YAML Package Info](https://github.com/custom-components/weatheralerts/blob/master/documentation/YAML_PACKAGES_DOCS.md)
  * [Lovelace UI Examples](https://github.com/custom-components/weatheralerts/blob/master/documentation/LOVELACE_EXAMPLES.md)
  * [GitHub Repository](https://github.com/custom-components/weatheralerts)
  * [View Issues/Feature Requests](https://github.com/custom-components/weatheralerts/issues)
  * [Report an Issue/Feature Request](https://github.com/custom-components/weatheralerts/issues/new/choose)
  * [Changelog](https://github.com/custom-components/weatheralerts/blob/master/CHANGELOG.md)




# Todo list
- [x] Add more documentation
- [ ] Add config flow to allow UI-based configuration (eliminate yaml-based platform configuration)
- [ ] Create alternative (possibly simpler) YAML package or move some template sensors into the integration
- [ ] Add backup weather alert source for occasions when weather.gov json feed is experiencing an outage


[release-badge]: https://img.shields.io/github/v/release/custom-components/weatheralerts?style=plastic
[release-link]: https://github.com/custom-components/weatheralerts/releases
[license-badge]: https://img.shields.io/github/license/custom-components/weatheralerts?style=plastic
[license-link]: https://github.com/custom-components/weatheralerts/blob/master/LICENSE
[hacs-badge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=plastic
[hacs-link]: https://github.com/custom-components/hacs
[stars-badge]: https://img.shields.io/github/stars/custom-components/weatheralerts?style=plastic
[stars-link]: https://github.com/custom-components/weatheralerts/stargazers
[maintained-badge]: https://img.shields.io/maintenance/yes/2020.svg?style=plastic
[issues-badge]: https://img.shields.io/github/issues/custom-components/weatheralerts?style=plastic
[issues-link]: https://github.com/custom-components/weatheralerts/issues
[commits-badge]: https://img.shields.io/github/commits-since/custom-components/weatheralerts/latest?style=plastic
[commits-link]: https://github.com/custom-components/weatheralerts/commits/master
