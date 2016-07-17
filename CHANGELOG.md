All notable changes to this project will be documented in this file.

* This project adheres to [Semantic Versioning](http://semver.org/).
* This project follows the guidelines outlined on [keepachangelog.com](http://keepachangelog.com/).

## [Unreleased]

## [0.22.3] - 2016-07-17
## Fixed
- Virtualenv now ues any available python 3
- move_head_absolute not passing rate to to_printer queue
- Tests updated for new rate parameter

## [0.22.2] - 2016-07-17
## Fixed
- Debian package version

## [0.22.1] - 2016-07-17
## Added
- Rates parameter to move_head_* docs

## [0.22.0] - 2016-07-17
## Added
- Limited logging of serial buffer full events
- Default absolute/relative movement rate of 300mm/sec

## Removed
- Internal use of jsonrpc printer -> server
- Internal use of jsonrpc server -> printer

## [0.21.0] - 2016-05-24
## Added
- Filament swap 
- Home x,y,z

## Changed:
- Settings page layout
- Controls page layout

## Fixed
- Redundant flag in init.d restart
- Default pi user not added to dialout group

## [0.20.0] - 2016-04-18
## Added
- Interface setup script

## Fixed
- Incorrect mock import in tests

## [0.19.0] - 2016-04-18
## Added
- Settings page
- Emergency stop button

## [0.18.0] - 2016-04-11
## Added
- Parse and store gcode meta data

## Fixed
- Confirm file delete
- Confirm print stop

## [0.17.0] - 2016-04-11
## Added
- API method get_filesystem_utilization
- Automatically-generated uploaded parameter to gcode files
- Option to configure lcd_gpio_pin for filament detection

## [0.16.1] - 2016-04-09
## Fixed
- Syntax error in Marlin printer

## [0.16.0] - 2016-04-09
## Added
- FILAMENT_SWAP state triggered by M600 from Marlin
- API method filament_swap_begin
- API method filament_swap_complete
- Frontend motors enable/disable slider
- Frontend fans enable/disable slider

## [0.15.0] - 2016-04-04
## Added
- API method set_extrude_override
- API event extrude_override_change
- API method set_speed_override
- API event speed_override_change
- API method set_fan_speed
- API event fan_speed_change

## [0.14.0] - 2016-03-30
## Added
- Metadata parameters to gcode files
- Thumbnail parameter to gcode files

## [0.13.0] - 2016-03-29
### Fixed
- Reconnect to printer when USB unplugged during execution
- Reset printer when hardware powered off during execution

## [0.12.1] - 2016-03-22
### Fixed
- Frontend directory missing from package

## [0.12.0] - 2016-03-22
### Added
- Enable/disable steppers functions
- UI improvements

## [0.11.0] - 2016-03-21
### Fixed
- Distinguish between nozzle 1 and 2 temps when heating for prints

## [0.10.0] - 2016-03-13
### Added
- Updated fonts
- Front page new look and feel
- Menu icons limited to what has options (no stats or file page)
- Controls page working (but without new layout)

## [0.9.0] - 2016-03-13
### Added
- Frontend tweaks

## [0.8.0] - 2016-03-11
### Added
- Frontend tweaks

## [0.7.2] - 2016-03-11
### Added
- Conversion of retract/unretract from mm/sec to mm/min for Marlin

## [0.7.1] - 2016-03-10
### Added
- Retract filament method to Dummy printer
- Unretract filament method to Dummy printer

## [0.7.0] - 2016-03-10
### Added
- Controls page
- Position Control
- Temperature Control
- Extruder retract/extrude buttons

### Changed
- Unparsed messages from Marlin should never happen so now raise ERROR

## [0.6.0] - 2016-03-08
### Added
- Send temp updates using data parsed from heat bed/nozzle + wait messages
- Delete files from frontend

### Fixed
- Broken final update on print completion for dummy printer
- Heat bed/nozzle + wait message has incorrect regex and was not matching

## [0.5.1] - 2016-03-07
### Changed
- Deal with split messages by always popping from the buffer on unparsed

### Added
- Final progress_update message on print completion to dummy printer 

## [0.5.0] - 2016-03-07
### Added
- delete_gcode_file API method
- Final progress_update message on print completion 

### Fixed
- Print hang bug by adding regex to match split "ok" message from Marlin
- Single-nozzle regex too permissive and matching dual-nozzle lines

## [0.4.0] - 2016-03-05
### Added
- Frontend auto-reconnect on disconnect

### Changed
- Marlin serial buffer increased from 4 to 5
- Long log messages now trunacted to max 75 chars

## [0.3.0] - 2016-03-04
### Added
- Home all button to home page
- File list hidden when print in progress
- Set temperatures on home page

### Fixed
- Error on frontend websocket disconnect
- Clear printer progress on frontend websocket disconnect
- Serial disconnect/reconnect not updating printer state
- Reconnection lag due to excessive debug log messages
- Gcode for setting temperature per nozzle
- Parsing of per-nozzle response to M105 temp request 

## [0.2.0] - 2016-03-02
### Added
- Frontend websocket disconnection error.
- Get printer status on connect.
- Queuing on websocket.
- More feedback to print status circle in form of "heating/printing" message
- Hide print status circle when file not selected

## [0.1.0] - 2016-03-01
### Added
- CHANGELOG.
- get_status method.
- formalised versioning.

### Removed
- Non-standard printer state event on initial connection

### Changed
- New UI from opengb-web.

## [0.0.1] - 2016-01-01
### Added
- Basic printer control functionality
- Documentation.
- Tests
- Opengb-web frontend built on Angular.js
