# Documentation Versioning Policy

> This documentation applies to Weather Alerts version 2026.1.0 and newer.
>  
> Behavior and configuration may differ in earlier versions.

> This document describes how documentation is maintained across Weather Alerts versions.

## Supported Documentation Versions

Documentation in this repository applies to the current major release series only.

As of this writing:
- Documentation applies to Weather Alerts version 2026.1.0 and newer

Earlier versions are not actively documented.

---

## When Documentation Must Be Updated

Documentation should be reviewed and updated when any of the following occur:

- Configuration flow changes
- Sensor attributes are added, removed, or renamed
- Alert processing logic changes
- Default behavior changes
- Breaking changes are introduced

---

## Handling Breaking Changes

When a breaking change is introduced:

1. Update the version notice header in all documentation files
2. Update `CHANGELOG.md` with a clear Breaking Changes section
3. Update README.md and documentation to reflect the new baseline behavior
4. Remove or clearly mark legacy behavior as deprecated

---

## Maintaining Older Documentation (Optional)

If older documentation must be preserved:

- Tag the repository at the last supported version
- Do not attempt to maintain multiple documentation sets in the same branch
- Refer users to tagged releases when needed

---

## Version Notice Updates

When releasing a new major or minor series:

- Update all version notice headers consistently
- Use a single version range (for example: 2027.1.0 and newer)
- Avoid ambiguous phrasing such as “latest” or “current”

---

## Documentation Philosophy

Documentation should describe actual runtime behavior, not intended behavior.

If the code and the documentation disagree, the code is considered authoritative and documentation must be updated.

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
- [Troubleshooting](https://github.com/custom-components/weatheralerts/blob/master/documentation/troubleshooting.md)
- [Migration from YAML](https://github.com/custom-components/weatheralerts/blob/master/documentation/migration.md)
- [Documentation Versioning Policy](https://github.com/custom-components/weatheralerts/blob/master/documentation/versioning.md)  **<-- You are here**

## Support and Issues

- [Support Forum](https://github.com/custom-components/weatheralerts/discussions)
- [GitHub Repository Home](https://github.com/custom-components/weatheralerts)
- [View Issues/Feature Requests](https://github.com/custom-components/weatheralerts/issues)
- [Report an Issue/Feature Request](https://github.com/custom-components/weatheralerts/issues/new/choose)
