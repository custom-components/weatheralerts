# Examples (Automations and Dashboards)

> This documentation applies to Weather Alerts version 2026.1.0 and newer.
>  
> Behavior and configuration may differ in earlier versions.

This page contains automation and dashboard examples for the Weather Alerts integration, including:
- Detecting API errors and outages using the sensor `error` array
- Notifying when new alerts appear using `alert_tracking`
- Displaying short alert summaries on dashboards
- Displaying full alert details (headline, description, instructions)

All examples assume your entity is named `sensor.weather_alerts`.
Replace this with your actual sensor entity_id as needed.

---

## Notes and Assumptions

The Weather Alerts sensor exposes these key attributes:

- `alerts`: List of alert objects
- `alert_tracking`: List tracking alert lifecycle status (`new`, `old`, `delete`)
- `alert_stats`: Computed counts by category
- `error`: Structured list containing recent success and failure entries

The `error` attribute is an array of objects. It typically includes:
- One entry for the most recent success (`type: success`)
- One entry for the most recent failure (`type: http_error` or `type: exception`), if applicable

---

## Automation Examples

### Persistent Notification and Cleanup (Auto-Dismiss) Blueprint

For a persistent notification automation that works like the YAML package automation/script combo, install the `weatheralerts_persistent_notification_original.yaml` blueprint from the repository blueprint directory. To install the blueprint:
1. Go to **Home Assistant → Settings → Automations & Scenes → Blueprints**
2. Click the **Import Blueprint** button
3. Copy the blueprint raw file URL from Github
   Example: https://github.com/custom-components/weatheralerts/raw/refs/heads/master/blueprints/weatheralerts_persistent_notification_original.yaml
4. Paste the URL into the Blueprint Address field in the **Import a Blueprint** dialog
5. Clicking **Preview** and then **Import Blueprint** will give you a `WeatherAlerts - Persistent Notification and Cleanup` blueprint
6. Click the three vertical dots for the blueprint and choose **Create Automation**
7. Set the WeatherAlerts Sensor option to the appropriate entity
That is all that is required. You can go back to **Settings → Automations & Scenes → Automations** and find the new automation and make any changes to the logic and alert format to suit your preferences. 

### Notify when the integration reports an error

```yaml
alias: WeatherAlerts - Notify on WeatherAlerts Error
description: ""
triggers:
  - entity_id:
      - sensor.weather_alerts
    trigger: state
conditions:
  - condition: template
    value_template: >
      {% set errs =
      state_attr('sensor.weather_alerts','error') %}

      {% if errs is not iterable or errs is string or errs is none %}
        false
      {% else %}
        {% set e0 = errs[0] if errs|length > 0 else none %}
        {{ e0 is mapping and e0.get('type') not in ['success'] }}
      {% endif %}
actions:
  - data:
      title: Weather Alerts Error
      message: >
        {% set errs =
        state_attr('sensor.weather_alerts','error') %}

        {% set e0 = errs[0] if errs|length > 0 else {} %} 

        **Type:** {{ e0.get('type', 'unknown') }}

        **Status:** {{ e0.get('status', 'unknown') }}

        **Message:** {{ e0.get('message', 'unknown') }}

        **Time:** {{ e0.get('timestamp', 'unknown') }}
      notification_id: weatheralerts_error_notification
    action: persistent_notification.create
mode: single
```
In this automation, the three places where you see `sensor.weather_alerts`, you should replace **weather_alerts** with your actual weatheralerts sensor entity_id.

This automation will create a persistent notification when an error occurs. If errors keep occuring, the next error notification will replace the existing notification. The notification will not auto-dismiss.

If you have more than one WeatherAlerts config entry and use more than one error notification automation, you may want to change the notification_id in the actions section of the automation so it is unique for the weatheralerts sensor it is tracking.

---

### Notify when the integration recovers after an error

```yaml
alias: WeatherAlerts - Notify on Recovery
description: ""
triggers:
  - entity_id: sensor.weather_alerts
    trigger: state
conditions:
  - condition: template
    value_template: >
      {% set cur =
      state_attr('sensor.weather_alerts','error')
      %}

      {% set prev = trigger.from_state.attributes.get('error') if
      trigger.from_state else none %}

      {% if cur is not iterable or cur is string or cur is none or cur|length ==
      0 %}
        false
      {% else %}
        {% set cur0 = cur[0] %}
        {% set prev0 = prev[0] if prev is iterable and prev is not string and prev is not none and prev|length > 0 else none %}
        {{ cur0.get('type') == 'success' and prev0.get('type') in ['http_error', 'exception'] }}
      {% endif %}
actions:
  - data:
      title: Weather Alerts Recovered From Error
      message: >
        The Weather Alerts integration has successfully updated after an error.

        {% set errs =
        state_attr('sensor.weather_alerts','error') %}

        {% set e0 = errs[0] if errs|length > 0 else {} %} 

        **Type:** {{ e0.get('type', 'unknown') }}

        **Status:** {{ e0.get('status', 'unknown') }}

        **Message:** {{ e0.get('message', 'unknown') }}

        **Time:** {{ e0.get('timestamp', 'unknown') }}
      notification_id: weatheralerts_notify_on_recovery
    action: persistent_notification.create
mode: single
```
In this automation, the three places where you see `sensor.weather_alerts`, you should replace `weather_alerts` with your actual weatheralerts sensor entity_id.

This automation will create a persistent notification when integration successfully updates after an error. The notification will not auto-dismiss.

If you have more than one WeatherAlerts config entry and use more than one error recovery notification automation, you may want to change the `notification_id` in the actions section of the automation so it is unique for the weatheralerts sensor it is tracking.

---

### Notify when all alerts clear (transition from >0 to 0)

This triggers only when alerts go from non-zero to zero.

```yaml
alias: WeatherAlerts - All Clear Notification
description: ""
triggers:
  - entity_id: sensor.weather_alerts
    trigger: state
conditions:
  - condition: template
    value_template: |-
      {% set prev = trigger.from_state.state if trigger.from_state else '0' %}
      {% set cur = trigger.to_state.state if trigger.to_state else '0' %}
      {{ (prev | int(0)) > 0 and (cur | int(0)) == 0 }}
actions:
  - data:
      title: Weather alerts cleared
      message: No active weather alerts remain.
      notification_id: weatheralerts_all_clear
    action: persistent_notification.create
mode: single
```
In this automation, the one place where you see `sensor.weather_alerts`, you should replace `weather_alerts` with your actual weatheralerts sensor entity_id.

This automation will create a persistent notification when all alerts are cleared from the sensor. The notification will not auto-dismiss.

If you have more than one WeatherAlerts config entry and use more than one error recovery notification automation, you may want to change the `notification_id` in the actions section of the automation so it is unique for the weatheralerts sensor it is tracking.

---

### Notify when specific event types appears

This checks `alerts` for the event name and triggers once when it first appears.

```yaml
alias: WeatherAlerts - Notify on Warnings
description: ""
triggers:
  - entity_id: sensor.weather_alerts
    trigger: state
conditions:
  - condition: template
    value_template: >
      {% set alerts =
      state_attr('sensor.weather_alerts','alerts') or []
      %}

      {% set events = alerts | map(attribute='event') | map('lower') | list %}

      {{ 'warning' in events or 'watch' in events or 'advisory' in events }}
actions:
  - data:
      title: Weather Warning
      message: >-
        A Weather Warning is active in your area. Review your alert details
        immediately.
      notification_id: weatheralerts_warning_notify
    action: persistent_notification.create
mode: single
```
In this automation, the two places where you see `sensor.weather_alerts`, you should replace `weather_alerts` with your actual weatheralerts sensor entity_id.

This automation will create a persistent notification when a warning alert event type appears in the sensor. The notification will not auto-dismiss.

If you have more than one WeatherAlerts config entry and use more than one error recovery notification automation, you may want to change the `notification_id` in the actions section of the automation so it is unique for the weatheralerts sensor it is tracking.

---

### Persistent Notification and Cleanup (Auto-Dismiss)

This is the WeatherAlerts - Persistent Notification and Cleanup blueprint if you'd rather copy the automation YAML instead of using the blueprint. There are two instances of `sensor.weather_alerts`, one near the top and one near the bottom of the automation YAML. Change `weather_alerts` to the entity ID if your weatheralerts sensor.

New alerts will show as full text alerts. If there are existing alerts in the persistent notification when new alerts come in, non-new alerts less than 30 minutes old will display as full text alerts and 30 minutes or older alerts will display the alert title only.
```yaml
alias: WeatherAlerts - Persistent Notification and Cleanup
triggers:
  - event: start
    trigger: homeassistant
  - event_type: component reload
    event_data:
      domain: weatheralerts
    trigger: event
  - trigger: state
    entity_id:
      - sensor.weather_alerts
    attribute: alert_tracking
actions:
  - choose:
      - conditions:
          - condition: template
            value_template: >-
              {% set new_ids = alert_ids | selectattr('status','eq','new') |
              map(attribute='id') | list %}

              {% set new_alerts_full = alerts | selectattr('id','in', new_ids) |
              list %}

              {% set ids =namespace(valid=[]) %}

              {% for item in alert_ids %}

                {% if item.status == 'old'
                   and item.sent is defined and item.sent not in ['null','',none]
                   and item.expires is defined and item.expires not in ['null','',none] %}
                  {% set sent_ts = as_timestamp(item.sent, default=0) %}
                  {% set exp_ts = as_timestamp(item.expires, default=0) %}
                  {% if exp_ts > now().timestamp() and (now().timestamp() - sent_ts) < 1800 %}
                    {% set ids.valid = ids.valid + [item.id] %}
                  {% endif %}
                {% endif %}
              {% endfor %}

              {% set old_alerts_full = alerts | selectattr('id','in', ids.valid)
              | list %}

              {% set ids2 = namespace(valid=[]) %} {% for item in alert_ids %}
                {% if item.status == 'old'
                   and item.sent is defined and item.sent not in ['null','',none]
                   and item.expires is defined and item.expires not in ['null','',none] %}
                  {% set sent_ts = as_timestamp(item.sent, default=0) %}
                  {% set exp_ts = as_timestamp(item.expires, default=0) %}
                  {% if exp_ts > now().timestamp() and (now().timestamp() - sent_ts) >= 1800 %}
                    {% set ids2.valid = ids2.valid + [item.id] %}
                  {% endif %}
                {% endif %}
              {% endfor %}

              {% set old_alerts_title = alerts | selectattr('id','in',
              ids2.valid) | list %}

              {{ new_alerts_full | length > 0 or old_alerts_full | length > 0 or
              old_alerts_title | length > 0 }}
        sequence:
          - data:
              notification_id: "{{ notif_id }}"
              title: Weather Alerts for {{ zone_name }}
              message: >
                {% set new_ids = alert_ids | selectattr('status','eq','new') |
                map(attribute='id') | list %}

                {% set new_alerts_full = alerts | selectattr('id','in', new_ids)
                | list %}

                {% set ids = namespace(valid=[]) %}

                {% for item in alert_ids %}
                  {% if item.status == 'old'
                     and item.sent is defined and item.sent not in ['null','',none]
                     and item.expires is defined and item.expires not in ['null','',none] %}
                    {% set sent_ts = as_timestamp(item.sent, default=0) %}
                    {% set exp_ts = as_timestamp(item.expires, default=0) %}
                    {% if exp_ts > now().timestamp() and (now().timestamp() - sent_ts) < 1800 %}
                      {% set ids.valid = ids.valid + [item.id] %}
                    {% endif %}
                  {% endif %}
                {% endfor %}

                {% set old_alerts_full = alerts | selectattr('id','in',
                ids.valid) | list %}

                {% set ids2 = namespace(valid=[]) %}

                {% for item in alert_ids %}
                  {% if item.status == 'old'
                     and item.sent is defined and item.sent not in ['null','',none]
                     and item.expires is defined and item.expires not in ['null','',none] %}
                    {% set sent_ts = as_timestamp(item.sent, default=0) %}
                    {% set exp_ts = as_timestamp(item.expires, default=0) %}
                    {% if exp_ts > now().timestamp() and (now().timestamp() - sent_ts) >= 1800 %}
                      {% set ids2.valid = ids2.valid + [item.id] %}
                    {% endif %}
                  {% endif %}
                {% endfor %}

                {% set old_alerts_title = alerts | selectattr('id','in',
                ids2.valid) | list %}

                {% for alert in new_alerts_full %}

                {# — Clean up title — #}

                {% set clean_title = alert.title
                   | replace('\n\n','<br>')
                   | replace('\n',' ')
                   | trim %}
                {# — Clean up headline — #}

                {% if alert.NWSheadline and alert.NWSheadline != 'null' %}
                  {% set clean_headline = alert.NWSheadline
                     | replace('\n\n','<br>')
                     | replace('\n',' ')
                     | trim %}
                {% else %}
                  {% set clean_headline = "" %}
                {% endif %}

                {# — Clean up description — #}

                {% set clean_description = alert.description
                   | replace('\n\n','<br>')
                   | replace('\n',' ')
                   | replace('<br>','<br>\n')
                   | regex_replace('([A-Z ]+?\\.\\.\\.)', '* <strong>\\1</strong>')
                   | replace('**','*')
                   | trim %}
                {# — Optional instruction — #}

                {% if alert.instruction and alert.instruction != 'null' %}
                  {% set clean_instruction = alert.instruction
                     | replace('\n\n','<br>')
                     | replace('\n',' ')
                     | trim %}
                {% else %}
                  {% set clean_instruction = "" %}
                {% endif %}

                {# — Area — #}

                {% set clean_area = alert.area
                   | replace('\n\n','<br>')
                   | replace('\n',' ')
                   | trim %}
                <font color="orange">
                  <ha-icon icon="{{ alert.icon }}"></ha-icon>
                </font>

                <strong>
                  <font color="red">{{ clean_title }}</font>
                </strong><br>

                {% if clean_headline and clean_headline != 'null' %}
                  {{ clean_headline }}<br>
                {% endif %}

                {{ clean_description }}<br>

                * <strong> AREA…</strong> {{ clean_area }}<br>

                {% if clean_instruction and clean_instruction != 'null' %}

                {{ clean_instruction }}<br><br>

                {% endif %}

                {% if alert.sent and alert.sent != 'null' %}

                <strong>Alert Sent:</strong> {{ alert.sent }}<br>

                {% endif %}

                {% if alert.effective and alert.effective != 'null' %}

                <strong>Effective:</strong> {{ alert.effective }}<br>

                {% endif %}

                {% if alert.expires and alert.expires != 'null' %}

                <strong>Expires:</strong> {{ alert.expires }}<br>

                {% endif %}

                {% if alert.onset and alert.onset != 'null' %}

                <strong>Onset:</strong> {{ alert.onset }}<br>

                {% endif %}

                {% if alert.ends and alert.ends != 'null' %}

                <strong>Ends:</strong> {{ alert.ends }}<br>

                {% endif %}

                {% if not loop.last %}
                  <hr>
                {% endif %}

                {% endfor %}


                {% if old_alerts_full %}
                  <hr>
                {% for alert in old_alerts_full %}

                {# — Clean up title — #}

                {% set clean_title = alert.title
                   | replace('\n\n','<br>')
                   | replace('\n',' ')
                   | trim %}
                {# — Clean up headline — #}

                {% if alert.NWSheadline and alert.NWSheadline != 'null' %}
                  {% set clean_headline = alert.NWSheadline
                     | replace('\n\n','<br>')
                     | replace('\n',' ')
                     | trim %}
                {% else %}
                  {% set clean_headline = "" %}
                {% endif %}

                {# — Clean up description — #}

                {% set clean_description = alert.description
                   | replace('\n\n','<br>')
                   | replace('\n',' ')
                   | replace('<br>','<br>\n')
                   | regex_replace('([A-Z ]+?\\.\\.\\.)', '* <strong>\\1</strong>')
                   | replace('**','*')
                   | trim %}
                {# — Optional instruction — #}

                {% if alert.instruction and alert.instruction != 'null' %}
                  {% set clean_instruction = alert.instruction
                     | replace('\n\n','<br>')
                     | replace('\n',' ')
                     | trim %}
                {% else %}
                  {% set clean_instruction = "" %}
                {% endif %}

                {# — Area — #}

                {% set clean_area = alert.area
                   | replace('\n\n','<br>')
                   | replace('\n',' ')
                   | trim %}
                <font color="orange">
                  <ha-icon icon="{{ alert.icon }}"></ha-icon>
                </font>

                <strong>
                  <font color="red">{{ clean_title }}</font>
                </strong><br>

                {% if clean_headline and clean_headline != 'null' %}
                  {{ clean_headline }}<br>
                {% endif %}

                {{ clean_description }}<br>

                * <strong>AREA…</strong> {{ clean_area }}<br>

                {% if clean_instruction and clean_instruction != 'null' %}

                {{ clean_instruction }}<br>

                {% endif %}

                {% if alert.sent and alert.sent != 'null' %}

                <strong>Alert Sent:</strong> {{ alert.sent }}<br>

                {% endif %}

                {% if alert.effective and alert.effective != 'null' %}

                <strong>Effective:</strong> {{ alert.effective }}<br>

                {% endif %}

                {% if alert.expires and alert.expires != 'null' %}

                <strong>Expires:</strong> {{ alert.expires }}<br>

                {% endif %}

                {% if alert.onset and alert.onset != 'null' %}

                <strong>Onset:</strong> {{ alert.onset }}<br>

                {% endif %}

                {% if alert.ends and alert.ends != 'null' %}

                <strong>Ends:</strong> {{ alert.ends }}<br>

                {% endif %}

                {% if not loop.last %}
                  <hr>
                {% endif %}

                {% endfor %}

                {% endif %}


                {% if old_alerts_title %}

                <hr>

                {% if new_alerts_full %}

                <strong>Other Active Alerts:</strong><br>

                {% else %}

                <strong>Active Alerts:</strong><br>

                {% endif %}

                {% for alert in old_alerts_title %}

                * <font color="orange">
                    <ha-icon icon="{{ alert.icon }}"></ha-icon>
                  </font>
                  <strong>{{ alert.title }}<strong><br>
                {% endfor %}

                {% endif %}
            action: persistent_notification.create
    default:
      - delay: "00:30:00"
      - data:
          notification_id: "{{ notif_id }}"
        action: persistent_notification.dismiss
mode: restart
variables:
  sensor_id: sensor.weatheralerts_outagamie_wiz038_wic087
  integration: "{{ state_attr(sensor_id, 'integration') or 'weatheralerts' }}"
  zone: "{{ state_attr(sensor_id, 'zone') or 'unknown' }}"
  zone_name: "{{ state_attr(sensor_id, 'zone_name') or 'unknown' }}"
  notif_id: "{{ integration }}_{{ zone | replace(',', '_') | lower }}"
  alert_ids: "{{ state_attr(sensor_id, 'alert_tracking') or [] }}"
  alerts: "{{ state_attr(sensor_id, 'alerts') or [] }}"
  now_ts: "{{ now().timestamp() | float }}"
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
- [Automation Examples](https://github.com/custom-components/weatheralerts/blob/master/documentation/examples_automations.md) **<-- You are here**
- [Dashboard Examples](https://github.com/custom-components/weatheralerts/blob/master/documentation/examples_dashboard.md)
- [Troubleshooting](https://github.com/custom-components/weatheralerts/blob/master/documentation/troubleshooting.md)
- [Migration from YAML](https://github.com/custom-components/weatheralerts/blob/master/documentation/migration.md)
- [Documentation Versioning Policy](https://github.com/custom-components/weatheralerts/blob/master/documentation/versioning.md)

## Support and Issues

- [Support Forum](https://github.com/custom-components/weatheralerts/discussions)
- [GitHub Repository Home](https://github.com/custom-components/weatheralerts)
- [View Issues/Feature Requests](https://github.com/custom-components/weatheralerts/issues)
- [Report an Issue/Feature Request](https://github.com/custom-components/weatheralerts/issues/new/choose)
