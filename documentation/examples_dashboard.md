# Examples (Dashboard)

> This documentation applies to Weather Alerts version 2026.1.0 and newer.
>  
> Behavior and configuration may differ in earlier versions.

This page contains dashboard examples for the Weather Alerts integration, including:
- Displaying short alert summaries on dashboards
- Displaying full alert details (headline, description, instructions)
- Displaying integration error status

All examples assume your entity is named `sensor.weather_alerts`.
Replace `sensor.weather_alerts` with your actual Weather Alerts sensor entity_id as needed.

---

## Notes and Assumptions

The Weather Alerts sensor exposes these key attributes:

- `alerts`: List of alert objects
- `alert_tracking`: List tracking alert lifecycle status (`new`, `old`, `delete`)
- `alert_stats`: Computed counts by category
- `error`: Structured list containing recent success and failure entries

---

## Dashboard Examples

### Simple state display

```yaml
type: entity
entity: sensor.weather_alerts
name: Weather Alerts
```

---

### Short alert summary (titles only)

```yaml
type: markdown
title: Weather Alerts (Summary)
content: >
  {% set alerts = state_attr('sensor.weather_alerts', 'alerts') or [] %}
  {% if alerts|length == 0 %}
  No active alerts.
  {% else %}
  {% for alert in alerts[:5] %}
  <font color="orange"><ha-icon icon="{{ alert.icon }}"></ha-icon></font> {{ alert.get('event','Alert') }}: {{ alert.get('title', alert.get('headline','')) }}
  <br><br>
  {% endfor %}
  {% endif %}
```
Note the font color usage to color the icon and the <ha-icon icon=""></ha-icon> tags to display the alert event icon.

---

### Full alert details for three most recent alerts (headline, description, instructions)

```yaml
type: markdown
title: Weather Alerts (Full Details)
content: |
  {% set alerts = state_attr('sensor.weather_alerts', 'alerts') or [] %}
  {% if alerts|length == 0 %}
  No active alerts.
  {% else %}
  {% for alert in alerts[:3] %}
  
  ## <font color="orange"><ha-icon icon="{{ alert.icon }}"></ha-icon></font> {{ alert.get('event','Alert') }}: {{ alert.get('title', alert.get('headline','')) }}

  **Sent:** {{ alert.get('sent','') | as_timestamp | timestamp_custom('%m-%d-%Y %I:%M:%S %p', false) }}  
  
  **Expires:** {{ alert.get('expires','') | as_timestamp | timestamp_custom('%m-%d-%Y %I:%M:%S %p', false) }}


  **Description:**
  {{ alert.get('description','') | replace('\n\n','<br>') | replace('* ',' **\*** ') | replace('\n',' ') }}

  {% set instr = alert.get('instruction','') %}
  {% if instr and instr != 'null' %}
  **Instructions:**
  {{ instr | replace('\n\n','<br>') | replace('* ',' **\*** ') | replace('\n',' ')}}
  {% endif %}

  <hr>

  {% endfor %}
  {% endif %}
```
Note the font color usage to color the icon and the <ha-icon icon=""></ha-icon> tags to display the alert event icon. Also note the usage of as_timestamp and timestamp_custom to customize the datetime text. Due to the use of new line (\n) and list (*) in the alert text, you may have to get creative with the **replace()** modifier to fix the text to get it to display correctly in the dashboard card.

The `[:3]` in `{% for alert in alerts[:3] %}` is what limits the number alerts to display. You can change the number to change the limit or remove `[:3]` completely to show all alerts.

---

### Integration error status indicator

```yaml
type: markdown
title: Weather Alerts Status
content: >
  {% set errs = state_attr('sensor.weather_alerts', 'error') or [] %}
  {% if errs|length == 0 %}
  **Status:** <font color="orange">Unknown</font>
  {% else %}
  {% set err = errs[0] %}
  {% if err.get('type') == 'success' %}
  **Status:** <font color="green">**OK**</font>
  {% else %}
  **Status:** <font color="red">**Error**</font> 
  **Type:** {{ err.get('type','') }}  
  **Status:** {{ err.get('status','') }}  
  **Message:** {{ err.get('message','') }}  
  **Time:** {{ err.get('timestamp','') }}
  {% endif %}
  {% endif %}
```

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
- [Dashboard Examples](https://github.com/custom-components/weatheralerts/blob/master/documentation/examples_dashboard.md) **<-- You are here**
- [Troubleshooting](https://github.com/custom-components/weatheralerts/blob/master/documentation/troubleshooting.md)
- [Migration from YAML](https://github.com/custom-components/weatheralerts/blob/master/documentation/migration.md)
- [Documentation Versioning Policy](https://github.com/custom-components/weatheralerts/blob/master/documentation/versioning.md)

## Support and Issues

- [Support Forum](https://github.com/custom-components/weatheralerts/discussions)
- [GitHub Repository Home](https://github.com/custom-components/weatheralerts)
- [View Issues/Feature Requests](https://github.com/custom-components/weatheralerts/issues)
- [Report an Issue/Feature Request](https://github.com/custom-components/weatheralerts/issues/new/choose)
