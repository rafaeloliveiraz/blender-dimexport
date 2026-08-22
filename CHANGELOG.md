# Changelog

All notable changes to this project are documented here.

## [2.0] - 2025-08-22

### Added
- **CSV** and **JSON** export formats (in addition to TXT).
- Optional **bounding-box volume** (W × H × D) column.
- Optional **unit suffix** (m/cm/mm) appended to values in TXT/CSV.
- File extension is now set **automatically** from the chosen format.
- Safe file writing with directory creation and clear error reporting.
- `doc_url` / `tracker_url` in add-on metadata.

### Changed
- Panel reorganized with grouped boxes for a cleaner UI.
- Values rounded to 4 decimals for consistency across formats.

## [1.2] - 2025-08-06

### Added
- Initial public release.
- Export Width / Height / Depth of selected mesh objects to TXT.
- Custom labels, unit conversion (m/cm/mm), selectable dimensions.
