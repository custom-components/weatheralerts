# Lovelace UI Examples

  * [Detailed Instructions](DOCUMENTATION.md)
  * [Troubleshooting](TROUBLESHOOTING.md)
  * [YAML Package Info](YAML_PACKAGES_DOCS.md)
  * **Lovelace UI Examples**
  * [GitHub Repository](https://github.com/custom-components/weatheralerts)
  * [View Issues/Feature Requests](https://github.com/custom-components/weatheralerts/issues)
  * [Report an Issue/Feature Request](https://github.com/custom-components/weatheralerts/issues/new/choose)
  * [Changelog](/CHANGELOG.md)


## Examples (no YAML package required)

(coming soon)


## Examples (YAML package required)

These examples of Lovelace card configurations will require the weatheralerts_1.yaml package file.

**Simple Entities Card with basic information:**<br>
This entity card displays the number of active alerts for the `weatheralerts_1_active_alerts` sensor. This sensor takes into account the alert ends time, expires time, and the main sensor availability to only count currently active alerts. The card also displays a Yes or No for the `weatheralerts_1_alerts_are_active` sensor.
```yaml
  - entities:
      - entity: sensor.weatheralerts_1_active_alerts
      - entity: sensor.weatheralerts_1_alerts_are_active
    show_header_toggle: false
    title: Outagamie County Weather Alerts
    type: entities
```
<br><br>

For the following cards, use the **Add Card** button in the Home Assistant web UI, scroll to the bottom of the card list, and select **Manual**. Then delete the default card code and paste in the card code from the examples below. 

A tip for using these conditional cards: Use **Vertical Stack** cards to organize your weather info and alerts. Place these conditional cards at the top of the vertical stack so your alerts are at the top of the weather info. When there are no weather alerts, these conditional cards will be hidden and won't distract from, or get in the way of, the main weather info.

**Conditional Card w/Markdown Card (only visible when there are weather alerts):**<br>
This conditional card will display alerts in a markdown card only if there are active alerts. It will also highlight the alert title with red text if the alert title text contains *warning* or *severe*.
```yaml
card:
  content: >
    <hr>  {% set alerts = [
      "sensor.weatheralerts_1_alert_1",
      "sensor.weatheralerts_1_alert_2",
      "sensor.weatheralerts_1_alert_3",
      "sensor.weatheralerts_1_alert_4",
      "sensor.weatheralerts_1_alert_5"] %}
    {% for alert in alerts if is_state(alert, 'on') %} {% if 'warning' or
    'severe' in state_attr( alert, 'display_title')|lower() %} <font
    color="red">  {% endif %} <b>{{ state_attr( alert, 'display_title')
    }}</b>  {%- if 'warning' or 'severe' in state_attr( alert,
    'display_title')|lower() -%} </font> {%- endif %} <br>{{ state_attr(
    alert, 'display_message') }} {% if loop.last %} {% else %} <hr> {% endif
    %} {% endfor %}
  title: Weather Alerts
  type: markdown
conditions:
  - entity: sensor.weatheralerts_1_alerts_are_active
    state: 'Yes'
type: conditional
```
<br><br>

**Conditional Card w/Markdown Card (only visible when there are weather alerts):**<br>
This Conditional Card will display alert types in a Markdown Card if there are active alerts. Warning message is displayed with red text, watch and advisory messages with orange text, and everything else in default text color.
```yaml
card:
  content: >-
    {% if (state_attr( 'sensor.weatheralerts_1_active_alerts', 'warning_count')|int > 1) %}
       <font color="red"><center><h2>****** WEATHER WARNINGS ******
       ** ARE ACTIVE FOR YOUR AREA **</h2></center></font>
    {% endif %}
    {% if (state_attr( 'sensor.weatheralerts_1_active_alerts', 'warning_count')|int == 1) %}
       <font color="red"><center><h2>****** A WEATHER WARNING ******
       <br>*** IS ACTIVE FOR YOUR AREA ***</h2></center></font>
    {% endif %}
    {% if (state_attr( 'sensor.weatheralerts_1_active_alerts', 'watch_count')|int > 1) %}
       <font color="orange"><center><h2>******* WEATHER WATCHES *******
       <br>** ARE ACTIVE FOR YOUR AREA **</h2></center></font>
    {% endif %}
    {% if (state_attr( 'sensor.weatheralerts_1_active_alerts', 'watch_count')|int == 1) %}
       <font color="orange"><center><h2>******* A WEATHER WATCH *******
       <br>*** IS ACTIVE FOR YOUR AREA ***</h2></center></font>
    {% endif %}
    {% if (state_attr( 'sensor.weatheralerts_1_active_alerts', 'advisory_count')|int > 1) %}
       <font color="orange"><center><h2>***** WEATHER ADVISORIES *****
       <br>** ARE ACTIVE FOR YOUR AREA ** </h2></center></font>
    {% endif %}
    {% if (state_attr( 'sensor.weatheralerts_1_active_alerts', 'advisory_count')|int == 1) %}
       <font color="orange"><center><h2>***** A WEATHER ADVISORY *****
       <br>*** IS ACTIVE FOR YOUR AREA ***</h2></center></font>
    {% endif %}
    {% if (state_attr( 'sensor.weatheralerts_1_active_alerts', 'statement_count')|int > 1) %}
       <center><h2>***** WEATHER STATEMENTS *****
       <br>** ARE ACTIVE FOR YOUR AREA **</h2></center>
    {% endif %}
    {% if (state_attr( 'sensor.weatheralerts_1_active_alerts', 'statement_count')|int == 1) %}
       <center><h2>***** A WEATHER STATEMENT *****
       <br>*** IS ACTIVE FOR YOUR AREA ***</h2></center>
    {% endif %}
    {% if (state_attr( 'sensor.weatheralerts_1_active_alerts', 'outlook_count')|int > 1) %}
       <center><h2>****** WEATHER OUTLOOKS ******
       <br>** ARE ACTIVE FOR YOUR AREA **</h2></center>
    {% endif %}
    {% if (state_attr( 'sensor.weatheralerts_1_active_alerts', 'outlook_count')|int == 1) %}
       <center><h2>****** A WEATHER OUTLOOK ******
       <br>*** IS ACTIVE FOR YOUR AREA ***</h2></center>
    {% endif %}
    {% if (state_attr( 'sensor.weatheralerts_1_active_alerts', 'alert_count')|int > 1) %}
       <center><h2>******* WEATHER ALERTS *******
       <br>** ARE ACTIVE FOR YOUR AREA **</h2></center>
    {% endif %}
    {% if (state_attr( 'sensor.weatheralerts_1_active_alerts', 'alert_count')|int == 1) %}
       <center><h2>******* A WEATHER ALERT *******
       <br>*** IS ACTIVE FOR YOUR AREA ***</h2></center>
    {% endif %}
    {% if (state_attr( 'sensor.weatheralerts_1_active_alerts', 'message_count')|int > 1) %}
       <center><h2>****** WEATHER MESSAGES ******
       <br>** ARE ACTIVE FOR YOUR AREA **</h2></center>
    {% endif %}
    {% if (state_attr( 'sensor.weatheralerts_1_active_alerts', 'message_count')|int == 1) %}
       <center><h2>****** A WEATHER MESSAGE ******
       <br>*** IS ACTIVE FOR YOUR AREA ***</h2></center>
    {% endif %}
    {% if (state_attr( 'sensor.weatheralerts_1_active_alerts', 'important_count')|int > 1) %}
       <center><h2>** IMPORTANT WEATHER ALERTS **
       <br>** ARE ACTIVE FOR YOUR AREA **</h2></center>
    {% endif %}
    {% if (state_attr( 'sensor.weatheralerts_1_active_alerts', 'important_count')|int == 1) %}
       <center><h2>** AN IMPORTANT WEATHER ALERT **
       <br>*** IS ACTIVE FOR YOUR AREA ***</h2></center>
    {% endif %}
    {% if (state_attr( 'sensor.weatheralerts_1_active_alerts', 'test_count')|int > 1) %}
       <center><h2>**** WEATHER ALERT TESTS ****
       <br>** ARE ACTIVE FOR YOUR AREA **</h2></center>
    {% endif %}
    {% if (state_attr( 'sensor.weatheralerts_1_active_alerts', 'test_count')|int == 1) %}
       <center><h2>**** A WEATHER ALERT TEST ****
       <br>*** IS ACTIVE FOR YOUR AREA ***</h2></center>
    {% endif %}
  type: markdown
conditions:
  - entity: sensor.weatheralerts_1_alerts_are_active
    state: 'Yes'
type: conditional
```
