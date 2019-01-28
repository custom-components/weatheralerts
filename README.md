# custom_component to get info from alerts.weather.gov

A platform which allows you to get information from alerts.weather.gov.
  
To get started put `/custom_components/weatheralerts/sensor.py` here:  
`<config directory>/custom_components/weatheralerts/sensor.py`  
  
**Example configuration.yaml:**

```yaml
sensor:
  platform: weatheralerts
  sameid: '034035'
```

**Configuration variables:**  
  
key | description  
:--- | :---  
**platform (Required)** | The platform name.  
**sameid (Required)** | The SAME ID for your county.  
  
## Sample overview

![Sample overview](overview.png)
  
To find the sameid go to [http://www.nws.noaa.gov/nwr/coverage/county_coverage.html](http://www.nws.noaa.gov/nwr/coverage/county_coverage.html).  
  
***
Due to how `custom_components` are loaded, it is normal to see a `ModuleNotFoundError` error on first boot after adding this, to resolve it, restart Home-Assistant.
