# custom_component to get info from alerts.weather.gov

A platform which allows you to get information from alerts.weather.gov.

# Breaking change

On December 25 2019, this custom_component was rewritten to use a more modern API to get alerts.
At the same time the configuration and storing of alert data was changed.

To find your zone go to [https://www.weather.gov/pimar/PubZone](https://www.weather.gov/pimar/PubZone), click the PDF or JPG for your state, then find your Zone number on the map.

To get started put all the files from `/custom_components/weatheralerts/` here:
`<config directory>/custom_components/weatheralerts/`

**Example configuration.yaml:**

```yaml
sensor:
  platform: weatheralerts
  state: CA
  zone: 560
```

**Configuration variables:**

key | description
:--- | :---
**platform (Required)** | The platform name.
**state (Required)** | Two letter code for your state ex.("CA" for California).
**zone (Required)** | 3 number code of the zone you want to monitor ex. "560"

## Sample overview

![Sample overview](sensor.png)

## Attributes

![Sample overview](attributes.png)

When there are alerts, the information about them are stored in a list in the attributes.
The content of that list can be used in automation templates, template sensors and a good amount of custom Lovelace cards.