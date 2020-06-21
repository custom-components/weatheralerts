# Detailed Instructions

 * **Detailed Instructions**
 * [Troubleshooting](TROUBLESHOOTING.md)
 * [YAML Package Info](YAML_PACKAGES_DOCS.md)
 * [Lovelace UI Examples](LOVELACE_EXAMPLES.md)
 * [GitHub Repository](https://github.com/custom-components/weatheralerts)
 * [View Issues/Feature Requests](https://github.com/custom-components/weatheralerts/issues)
 * [Report an Issue/Feature Request](https://github.com/custom-components/weatheralerts/issues/new/choose)
 * [Changelog](/CHANGELOG.md)


## Installation

It is recommended to install *weatheralerts* via *HACS*. To install manually, put all the files from `/custom_components/weatheralerts/` here:
`<config directory>/custom_components/weatheralerts/`

Once installed (via *HACS* or manually), continue reading below to configure the weatheralerts sensor platform.


## Configuration

You will need to configure the *weatheralerts* sensor platform via YAML (for now). This can be done by adding the platform to the 

```yaml
sensor:
```
section of your **configuration.yaml** or adding it to another dedicated YAML file you have setup for sensor configuration. The absolute minimum information your need to configure *weatheralerts* are your two-letter state or marine zone abbreviation and your zone ID number.

```yaml
sensor:
  platform: weatheralerts
  state: <your state or marine two letter abbreviation>
  zone: <your zone ID number>
```
Your state abbreviation is simply the standard two letter postal abbreviation. Your state or marine abbreviation can be found by going to [https://alerts.weather.gov/](https://alerts.weather.gov/), find your state or marine area in the list, and click the *Zone List* link to view the zones. The first two letters of the Zone Code is what you would use for the *state* configuration option.

To find your zone ID number (both state and marine zones) for the *zone* configuration option, go to [https://alerts.weather.gov/](https://alerts.weather.gov/), scroll down the page to find your state or marine location, click the *Zone List* link for your state or marine location, and lookup the six character code in the *Zone Code* column for your county or marine zone. The first two letters of your six character zone code will be used for your state configuration option. The three digit number is your zone ID number and will be used for your zone configuration option. For example, Outagamie County in Wisconsin has a zone code of `WIZ038`. The state config is `WI` and the zone ID number for the *zone* config option is `38` (omit any leading zeros, so 038 = 38). 

To find your county ID number, go to [https://alerts.weather.gov/](https://alerts.weather.gov/), scroll down the page to find your state, click the County List link next to your state, lookup the six character county code for your county in the table, and then take just the number from that county code to use as your county ID number. For example, Outagamie County in Wisconsin has county code `WIC087`. The county ID number for the *county* config option is `87` (omit any leading zeros, so 087 = 87).

**Example configuration.yaml:**

```yaml
sensor:
  platform: weatheralerts
  state: WI
  zone: 38
  county: 87
```

**If your zone or county ID number starts with one or more 0's you need to wrap quotes around it, or just skip the leading 0's (so `010` should be `"010"` or `10`, and `003` should be `"003"` or `3`)**

**Configuration variables:**

| key | description |
| :--- | :--- |
| **platform (Required)** | The platform name. |
| **state (Required)** | Two letter code for your state ex.("CA" for California). |
| **zone (Required)** |  One, two, or three digit code of the zone you want to monitor ex. 38 |
| **county (Optional)** | One, two, or three digit code of the zone you want to monitor ex. 87 |
| **scan_interval (Optional)** | Number of seconds between updates. Default is 30 seconds if option is not specified. |

### **It is highly recommended to use BOTH zone and county IDs in the platform configuration to increase the reliability of alerts. If you only use the 'zone' config option, you may not get all of the active alerts for your location.**


## Sample Overview

![Sample overview](/sensor.png)

The main *weatheralerts* sensor will be given the name of your zone or county and can be changed via the Home Assistant Entities Overview in the Home Assistant Configuration menu.

This main sensor state will be the number of alerts that are currently active, or it will be set to `unavailable` if *weatheralerts* is unable to update the sensor due to problems with the weather.gov API server. Due to the possiblity of the state being `unavailable`, you need to be careful when using it as a trigger for automations. Additional conditions may need to be applied to automations to prevent unwanted re-triggering.

## Attributes

![Sample overview](/attributes.png)

When there are alerts, the information about them are stored in a list in the attributes.
The content of that list can be used in automations, template sensors, and Lovelace cards.
The following attributes are available:
| attribute | description |
| :--- | :--- |
| **area** | The text describing the affected area of the alert message. |
| **certainty** | Certainty of the subject event of the alert message.<br>(Observed, Likely, Possible, Unlikely, Unknown) |
| **description** | The text describing the subject event of the alert message. |
| **ends** | The expected end time of the subject event in the alert message.<br>The time at which the hazard conditions of the subject event are no longer expected. |
| **event** | The text denoting the type of the subject event in the alert message. |
| **instruction** | The text describing the recommended action to be taken by recipients of the alert message. |
| **response** | The code denoting the type of action recommended.<br>(Shelter, Evacuate, Prepare, Execute, Avoid, Monitor, Assess, AllClear, None) |
| **sent** | The origination time and date of the alert message. |
| **severity** | Severity of the subject event of the alert message.<br>(Extreme, Severe, Moderate, Minor, Unknown) |
| **title** | A brief human-readable headline containing the alert type and valid time of the alert. |
| **urgency** | Urgency of the subject event of the alert message.<br>(Immediate, Expected, Future, Past, Unknown) |
| **NWSheadline** | A brief human-readable headline containing the alert type and valid time of the alert.. |
| **hailSize** | Potential hail size (inches) of storm. |
| **windGust** | Potential wind gusts of storm. |
| **waterspoutDetection** | Potential for waterspout formation in storm. |
| **effective** | The effective date and time of the information in the alert message. |
| **expires** | The expiry date and time of the information in the alert message. |
| **endsExpires** | If *ends* time is not set, this is equal to *expires* time. Otherwise this is equal to *ends* time.<br>This can be used to hide stale alerts if weather.gov API is experiencing an outage. |
| **onset** | Expected time of the beginning of the subject event in the alert message. |
| **status** | The code denoting the appropriate handling of the alert message.<br>(Actual, Exercise, System, Test, Draft). |
| **messageType** | The code denoting the nature of the alert message.<br>(Alert, Update, Cancel, Ack, Error) |
| **category** | The code denoting the category of the subject event in the alert message.<br>(Geo, Met, Safety, Security, Rescue, Fire, Health, Env, Transport, Infra, CBRNE, Other) |
| **sender** | Email address of the NWS webmaster. |
| **senderName** | Name of the issuing NWS Office. |
| **id** | A unique ID for the alert. |
| **zoneid** | The zone ID (and county ID if configured) used to fetch your weather alerts. |
