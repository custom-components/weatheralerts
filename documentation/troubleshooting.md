# Troubleshooting

> This documentation applies to Weather Alerts version 2026.1.0 and newer.
>  
> Behavior and configuration may differ in earlier versions.

This page describes common troubleshooting steps for the Weather Alerts integration, including how to enable and disable debug logging.

The most common issue that pops up relates to NWS API outages. These outages and intermittent outages can persist for hours or even days. These outages are typically regional and don't affect everyone at the same time, so you may be able to overcome the issue by using a VPN to route your Internet connection to a different part of the country. These outages manifest as Timeout and HTTP errors and are almost always going to be related to an Internet or network issue on your end or a NWS API outage on the NWS end. These errors don't generally need to be reported since there isn't anything in the integration that can be done to fix those errors; the integration just reports them as an FYI for you. If you believe the issue isn't the Internet or network on your end and https://api.weather.gov seems functional, feel free to open an issue on Github.

If you install the Weather Alerts integration during one of these NWS API outages, you will likely get hung up on Step 2 of the config flow where you submit your zone, county, and marine codes. If that happens, you will have to keep trying until the NWS API is working again. If you've waited several hours or a full day and it still isn't allowing you to get past the second config flow step, follow the directions below to enable debug logging and reporting the issue on Github.

---

## Enabling Debug Logging

Debug logging is enabled from the integration page itself using Home Assistant’s built-in debug controls.

### Steps

1. Open Home Assistant in your browser
2. Go to **Settings → Devices & Services**
3. Select the **Integrations** tab
4. Locate **Weather Alerts**
5. Open the integration
6. In the upper-right corner of the page, open the three-dot menu
7. Select **Enable debug logging**

A confirmation message will appear indicating that debug logging is enabled.

Debug logging takes effect immediately and does not require a restart. Once enabled, reproduce the error or issue (or wait for it to occur), and then disable the debug logging and report the issue on Github.

---

## Disabling Debug Logging

Debug logging should be disabled once troubleshooting is complete.

### Steps

1. Open Home Assistant in your browser
2. Go to **Settings → Devices & Services**
3. Select the **Integrations** tab
4. Locate **Weather Alerts**
5. Open the integration
6. Click **Disable** on the debug logging banner shown on the integration page

When debug logging is disabled, your browser will automatically download the current Home Assistant log file.

---

## Viewing Logs

After enabling debug logging, log output can be viewed from:

- **Settings → System → Logs**

Weather Alerts log messages are prefixed with: `weatheralerts:`

This can be used to find or filter relevant log messages.

---

## When to Use Debug Logging

Debug logging is useful when:

- Alerts are not updating as expected
- The integration reports API errors _(see note below)_
- Alert counts appear incorrect
- Alert tracking behavior needs verification
- Troubleshooting configuration or zone issues
- Providing logs when opening a GitHub issue

  - _Note:_ API errors are almost always going to be an issue with the NWS API and not an actual issue with the integration. If you believe the issue isn't with the API, or if you're unsure, feel free to [open an issue](https://github.com/custom-components/weatheralerts/issues/new/choose).

---

## When Not to Use Debug Logging

Debug logging should not be left enabled permanently.

It may:
- Increase log file size
- Produce excessive log output
- Make unrelated issues harder to diagnose

Disable debug logging once troubleshooting is complete.

---

## Reporting Issues

If you need to report an issue:

1. Enable debug logging
2. Reproduce the issue
3. Collect relevant log entries
4. Disable debug logging
5. Open an issue at:

https://github.com/custom-components/weatheralerts/issues

Include:
- Your Weather Alerts version
- Your Home Assistant version
- A brief description of the problem
- Relevant log entries (or attach your log file)

Before attaching log files, be sure scan for and censor or remove usernames, passwords, API keys, and any other sensitive data you don't want to share publicly.

Preference for log postings in Github issues (1 to 4, most prefered to least prefered):
- 1. Use grep or similar command-line tool to create a clean log file with all `weatheralerts` log entries from your log file
- 2. Your full log file (censored to remove any sensitive or private data)
- 3. Just the log entries that indicate errors
- 4. No log data, just describe the error you are observing

---

## Documentation Navigation

- [Overview](https://github.com/custom-components/weatheralerts/blob/master/documentation/overview.md)
- [Installation](https://github.com/custom-components/weatheralerts/blob/master/documentation/installation.md)
- [Configuration](https://github.com/custom-components/weatheralerts/blob/master/documentation/configuration.md)
- [Sensor Behavior](https://github.com/custom-components/weatheralerts/blob/master/documentation/sensor.md)
- [Alert Tracking](https://github.com/custom-components/weatheralerts/blob/master/documentation/alert_tracking.md)
- [Alert Deduplication](https://github.com/custom-components/weatheralerts/blob/master/documentation/deduplication.md)
- [Alert Icon Configuration](https://github.com/custom-components/weatheralerts/blob/master/documentation/icons.md)
- [Error Handling](https://github.com/custom-components/weatheralerts/blob/master/documentation/error_handling.md)
- [Automation Examples](https://github.com/custom-components/weatheralerts/blob/master/documentation/examples_automations.md)
- [Dashboard Examples](https://github.com/custom-components/weatheralerts/blob/master/documentation/examples_dashboard.md)
- [Troubleshooting](https://github.com/custom-components/weatheralerts/blob/master/documentation/troubleshooting.md) **<-- You are here**
- [Migration from YAML](https://github.com/custom-components/weatheralerts/blob/master/documentation/migration.md)
- [Documentation Versioning Policy](https://github.com/custom-components/weatheralerts/blob/master/documentation/versioning.md)

## Support and Issues

- [Support Forum](https://github.com/custom-components/weatheralerts/discussions)
- [GitHub Repository Home](https://github.com/custom-components/weatheralerts)
- [View Issues/Feature Requests](https://github.com/custom-components/weatheralerts/issues)
- [Report an Issue/Feature Request](https://github.com/custom-components/weatheralerts/issues/new/choose)
