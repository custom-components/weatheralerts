# Troubleshooting

  * [Detailed Instructions](https://github.com/custom-components/documentation/DOCUMENTATION.md)
  * **Troubleshooting**
  * [YAML Package Info](https://github.com/custom-components/documentation/YAML_PACKAGES_DOCS.md)
  * [Lovelace UI Examples](https://github.com/custom-components/documentation/LOVELACE_EXAMPLES.md)
  * [GitHub Repository](https://github.com/custom-components/weatheralerts)
  * [View Issues/Feature Requests](https://github.com/custom-components/weatheralerts/issues)
  * [Report an Issue/Feature Request](https://github.com/custom-components/weatheralerts/issues/new/choose)
  * [Changelog](https://github.com/custom-components/CHANGELOG.md)


Most warnings and errors that are likely to be logged by the *weatheralerts* integration are harmless.

Any log warning message regarding **TimeoutError** or **Possible API outage** will almost always represent a problem with the weather.gov alert API server. There is always a chance these particular warnings could be an issue with your LAN configuration, wifi, or your Internet connection, but it will most likely be a problem with the API server. 

You may be able to verify if the weather.gov API server is experiencing an outage by visiting these URLs:
  * [http://api.weather.gov](http://api.weather.gov) - should return a JSON result "status": "OK"
  * [http://api.weather.gov/alerts](http://api.weather.gov/alerts) - should return JSON results of all weather alerts
  * [http://api.weather.gov/alerts/active?zone=WIC075](http://api.weather.gov/alerts/active?zone=WIC075) - should return JSON result for Outagamie County, Wisconsin

If any or all of those links return NGINX error pages or anything other than valid JSON results, then the weather.gov API server is very likely undergoing maintenance or is experiencing some type of a network or service outage. These outages can last for several hours when they occur. 

If you happen to start or restart Home Assistant during one of these outages, *weatheralerts* will make a few attempts over approximately 10 to 11 minutes to connect to the weather.gov API server. If all attempts fail, *weatheralerts* will not be set up and will not work until the weather.gov API server resumes normal operation and Home Assistant is restarted while the weather.gov API server is operating normally.
