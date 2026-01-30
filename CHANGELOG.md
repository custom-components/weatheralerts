# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project follows calendar-based versioning.

---

## [2026.1.0] - 2026-01-30

### Breaking Changes

- YAML-based configuration is deprecated and no longer supported for new setups.
- All configuration must now be performed through the Home Assistant UI.
- Existing YAML platform configurations are automatically imported into UI-based config entries on startup.
- The YAML package should be considered deprecated and will no longer be supported or updated. See the documenation for instructions on using the automation blueprint and dashboard examples.

### Added

- Persistent alert lifecycle tracking (`alert_tracking`) with support for `new`, `old`, and `delete` states.
- Alert tracking state is preserved across Home Assistant restarts.
- Support for National Weather Service marine zones.
- Configurable sensor update interval (30–600 seconds).
- Configurable API request timeout (10–60 seconds).
- Validation to ensure API timeout is always less than the update interval.
- Optional alert deduplication based on alert description.
- Customizable alert icons by alert event type.
- Default fallback icon for unknown or unmapped alert events.
- Improved structured error reporting via sensor attributes.
- Automatic pruning of stale alerts during API outages.
- Human-readable zone name resolution from the NWS API.
- Combined feed support for zone, county, and marine alerts in a single sensor.

### Changed

- Sensor state now strictly represents the number of active alerts.
- Alert data is normalized and sorted consistently by recency.
- API failures now fall back to the last known good data instead of failing silently.
- Alert expiration handling has been made more robust during outages.
- Entity naming and unique ID generation have been standardized.

### Fixed

- Incorrect handling of expired alerts during temporary API failures.
- Configuration validation failure due to alerts.weather.gov shutting down.
- Zone and county code validation edge cases.

### Internal

- Refactored alert processing and sorting logic.
- Added RestoreEntity support for persistent sensor attributes.
- Improved coordinator-based update handling.
- Centralized default alert event icon mappings.
- Added translation coverage for configuration and options flows.
- Improved logging for debugging and troubleshooting.
- Additional validation and error handling improvements.

---

## Other Changes

- Documentation updates and clarifications.
- Added automation blueprint for persistent notifications.
- Added automation and dashboard examples.
