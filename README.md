# custom_component to get info from alerts.weather.gov
![Version](https://img.shields.io/badge/version-1.0.0-green.svg?style=for-the-badge) ![mantained](https://img.shields.io/maintenance/yes/2018.svg?style=for-the-badge)   
A platform which allows you to get information from alerts.weather.gov. 
  
To get started put `/custom_components/sensor/weatheralerts.py` here:
`<config directory>/custom_components/sensor/weatheralerts.py`  
  
**Example configuration.yaml:**
```yaml
sensor:
  platform: weatheralerts
  sameid: 2190400
```
**Configuration variables:**  
  
key | description  
:--- | :---  
**platform (Required)** | The platform name.  
**sameid (Required)** | The SAME ID for your county.  
  
#### Sample overview
![Sample overview](overview.png)
  
[Home-Assistant demo site.](https://ha-test-weatheralerts.halfdecent.io)
  
To find the sameid go to [http://www.nws.noaa.gov/nwr/coverage/county_coverage.html](http://www.nws.noaa.gov/nwr/coverage/county_coverage.html).  
push_github:  stage: deploy
  script:
    - curl -sL https://gitlab.com/ludeeus/toolbox/raw/master/CI-Scripts/push_to_public_repo/init.sh | bash -s github pip-packages  /root
    - curl -sL https://gitlab.com/ludeeus/toolbox/raw/master/CI-Scripts/push_to_public_repo/push.sh | bash -s Europe/Oslo
