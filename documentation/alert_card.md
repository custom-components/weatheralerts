# WeatherAlerts Alert Card

> This documentation applies to Weather Alerts version 2026.5.0 and newer.
>  
> Behavior and configuration may differ in earlier versions.

The WeatherAlerts Alert Card is a bundled Lovelace custom card for displaying active alerts from a weatheralerts sensor. It reads the `alerts` attribute array from the configured sensor entity. This card is currently a work-in-progress inspired by [AlertTicker-Card](https://github.com/djdevil/AlertTicker-Card).

## Dashboard Resource

The integration auto-registers the bundled card as a Lovelace dashboard resource when Home Assistant is using storage-mode dashboards. The registered resource URL includes the integration version for browser cache busting:

```yaml
url: /weatheralerts_static/weatheralerts-alert-card.js?v=<integration_version>
type: module
```

After installing or updating the integration, refresh the browser before adding the card. If Home Assistant is configured for YAML-mode dashboards, resources cannot be managed through the UI, so add the resource manually under the `lovelace:` section of `configuration.yaml`:

```yaml
lovelace:
  resources:
    - url: /weatheralerts_static/weatheralerts-alert-card.js?v=<integration_version>
      type: module
```

### Dashboard Resource Recovery

Weather Alerts automatically registers the Weather Alerts Alert Card dashboard resource when the integration is set up. If the dashboard resource is manually deleted while Home Assistant is still running, restart Home Assistant to allow the integration to register the resource again.

## Basic Rotating Card

```yaml
type: custom:weatheralerts-alert-card
entity: sensor.weatheralerts_outagamie_wiz038_wic087
display_mode: rotating
content_mode: compact
show_icon: true
show_alert_count: true
rotation_interval: 7
rotation_pause: 1
rotation_type: fold
```

## Rotating Animation Examples

Use `rotation_type` to change how alerts rotate.

```yaml
type: custom:weatheralerts-alert-card
entity: sensor.weatheralerts_outagamie_wiz038_wic087
display_mode: rotating
content_mode: compact
rotation_interval: 7
rotation_pause: 1
rotation_type: twirl_left
```

Supported rotation types:

- `none`
- `fade`
- `slide_left`
- `slide_right`
- `slide_up`
- `slide_down`
- `fold`
- `flip`
- `zoom`
- `bounce`
- `blur`
- `roll`
- `twirl_left`
- `twirl_right`

## Ticker Banner Example

```yaml
type: custom:weatheralerts-alert-card
entity: sensor.weatheralerts_outagamie_wiz038_wic087
display_mode: ticker
content_mode: compact
ticker_pixels_per_second: 70
ticker_loop_gap: half
ticker_start_position: visible
show_icon: true
```

The ticker measures the card viewport and the full alert track, then calculates the animation duration from `ticker_pixels_per_second`. This keeps the visual speed consistent regardless of how many alerts are shown.

Use `ticker_loop_gap` to control how much empty space appears between ticker loops:

```yaml
ticker_loop_gap: none   # next loop starts almost immediately
ticker_loop_gap: small  # small 24px gap
ticker_loop_gap: half   # gap equals half the visible card width
ticker_loop_gap: full   # gap equals the full visible card width
ticker_loop_gap: 80px   # explicit pixel gap
ticker_loop_gap: 25%    # percentage of visible card width
```

## List Display Example

```yaml
type: custom:weatheralerts-alert-card
entity: sensor.weatheralerts_outagamie_wiz038_wic087
display_mode: list
content_mode: summary
show_icon: true
max_alerts: 10
```

## Full Alert Display Example

```yaml
type: custom:weatheralerts-alert-card
entity: sensor.weatheralerts_outagamie_wiz038_wic087
display_mode: rotating
content_mode: full
rotation_interval: 10
rotation_pause: 1
rotation_type: slide_left
show_icon: true
show_navigation: true
```

## All-Clear Card Example

```yaml
type: custom:weatheralerts-alert-card
entity: sensor.weatheralerts_outagamie_wiz038_wic087
show_when_empty: true
empty_message: No active weather alerts
no_alert_color: "#55cc00"
no_alert_text_color: "#ffffff"
no_alert_muted_text_color: "rgba(255,255,255,0.82)"
```

## Options

| Option | Default | Available options | Description |
| --- | --- | --- | --- |
| `entity` | Required | Weatheralerts sensor entity ID | Weatheralerts sensor entity to read. |
| `display_mode` | `rotating` | `rotating`, `ticker`, `list`, `full` | Overall card layout. |
| `content_mode` | `compact` | `compact`, `summary`, `full` | Amount of alert detail to show. |
| `headline_source` | `title` | Any alert attribute name, usually `title`, `event`, or `NWSheadline` | Attribute used for the primary alert text. |
| `rotation_interval` | `7` | Number, seconds | Time each alert remains visible before the next rotation is scheduled. |
| `rotation_pause` | `0` | Number, seconds | Extra pause added before rotating to the next alert. |
| `rotation_type` | `fold` | `none`, `fade`, `slide_left`, `slide_right`, `slide_up`, `slide_down`, `fold`, `flip`, `zoom`, `bounce`, `blur`, `roll`, `twirl_left`, `twirl_right` | Rotation animation type. |
| `rotation_animation_duration` | `450ms` | Time value such as `450ms`, `900ms`, or `1s` | Duration of the visible rotation animation. |
| `ticker_pixels_per_second` | `70` | Number, pixels per second | Ticker scroll speed. Higher values scroll faster. |
| `ticker_start_position` | `visible` | `visible`, `offscreen` | First ticker pass starts visible or enters from offscreen right. |
| `ticker_loop_gap` | `full` | `none`, `small`, `half`, `full`, pixel values like `80px`, percentage values like `25%`, or a plain number of pixels | Empty space between ticker loops. |
| `ticker_pause_on_hover` | `true` | `true`, `false` | Pause ticker scrolling while hovering. |
| `show_title` | `false` | `true`, `false` | Show the card title row. |
| `title` | `Weather Alerts` | Text | Card title text. |
| `show_icon` | `true` | `true`, `false` | Show each alert icon. |
| `show_alert_count` | `true` | `true`, `false` | Show active alert count. |
| `show_navigation` | `true` | `true`, `false` | Show previous and next buttons in rotating mode. |
| `show_when_empty` | `false` | `true`, `false` | Show an all-clear card when no alerts are active. |
| `empty_message` | `No active weather alerts` | Text | Message shown when there are no active alerts and `show_when_empty` is true. |
| `max_alerts` | `10` | Number; use `0` to show all alerts | Maximum number of alerts to display. |
| `warning_color` | `#ff2020` | CSS color | Background color for warning alerts. |
| `watch_color` | `#ff8800` | CSS color | Background color for watch alerts. |
| `advisory_color` | `#ff8800` | CSS color | Background color for advisory alerts. |
| `other_color` | `#efbf00` | CSS color | Background color for all other active alerts. |
| `no_alert_color` | `#55cc00` | CSS color | Background color for the all-clear card. |
| `warning_text_color` | `#ffffff` | CSS color | Primary text color for warning alerts. |
| `watch_text_color` | `#ffffff` | CSS color | Primary text color for watch alerts. |
| `advisory_text_color` | `#ffffff` | CSS color | Primary text color for advisory alerts. |
| `other_text_color` | `#ffffff` | CSS color | Primary text color for all other active alerts. |
| `no_alert_text_color` | `#ffffff` | CSS color | Primary text color for the all-clear card. |
| `warning_muted_text_color` | `rgba(255,255,255,0.82)` | CSS color | Secondary text color for warning alert summary/detail labels. |
| `watch_muted_text_color` | `rgba(255,255,255,0.82)` | CSS color | Secondary text color for watch alert summary/detail labels. |
| `advisory_muted_text_color` | `rgba(255,255,255,0.82)` | CSS color | Secondary text color for advisory alert summary/detail labels. |
| `other_muted_text_color` | `rgba(255,255,255,0.82)` | CSS color | Secondary text color for all other active alert summary/detail labels. |
| `no_alert_muted_text_color` | `rgba(255,255,255,0.82)` | CSS color | Secondary text color for the all-clear card. |
| `border_radius` | `12px` | CSS size | Alert section border radius. |
| `section_gap` | `6px` | CSS size | Gap between alert sections. |

## Color Rules

The card checks the alert event, title, and NWSheadline text:

- Alerts containing `warning` use `warning_color`, `warning_text_color`, and `warning_muted_text_color`.
- Alerts containing `watch` use `watch_color`, `watch_text_color`, and `watch_muted_text_color`.
- Alerts containing `advisory` use `advisory_color`, `advisory_text_color`, and `advisory_muted_text_color`.
- All other active alerts use `other_color`, `other_text_color`, and `other_muted_text_color`.
- The all-clear card uses `no_alert_color`, `no_alert_text_color`, and `no_alert_muted_text_color` when `show_when_empty` is true.

## Automatic Resource Registration Notes

For Home Assistant storage-mode dashboards, Weather Alerts attempts to add the card resource automatically when the integration loads and when a Weather Alerts config entry is set up. This covers both existing installations after restart and the case where all Weather Alerts config entries were removed before creating a new one.

If the card does not appear after installation, restart Home Assistant and check **Settings -> Dashboards -> Resources** for:

```yaml
url: /weatheralerts_static/weatheralerts-alert-card.js?v=2026.5.0
type: module
```

YAML-mode dashboards still require the resource to be added manually in YAML.

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
- [Alert Card](https://github.com/custom-components/weatheralerts/blob/master/documentation/alert_card.md) **<-- You are here**
- [Troubleshooting](https://github.com/custom-components/weatheralerts/blob/master/documentation/troubleshooting.md)
- [Migration from YAML](https://github.com/custom-components/weatheralerts/blob/master/documentation/migration.md)
- [Documentation Versioning Policy](https://github.com/custom-components/weatheralerts/blob/master/documentation/versioning.md)

## Support and Issues

- [Support Forum](https://github.com/custom-components/weatheralerts/discussions)
- [GitHub Repository Home](https://github.com/custom-components/weatheralerts)
- [View Issues/Feature Requests](https://github.com/custom-components/weatheralerts/issues)
- [Report an Issue/Feature Request](https://github.com/custom-components/weatheralerts/issues/new/choose)
