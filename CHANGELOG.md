All notable changes to this project will be documented in this file.

* This project adheres to [Semantic Versioning](http://semver.org/).
* This project follows the guidelines outlined on [keepachangelog.com](http://keepachangelog.com/).

## [Unreleased]
## [0.6.0] - 2016-08-02
### Added
- Send temp updates using data parsed from heat bed/nozzle + wait messages
- Delete files from frontend

### Fixed
- Broken final update on print completion for dummy printer
- Heat bed/nozzle + wait message has incorrect regex and was not matching

## [0.5.1] - 2016-07-02
### Changed
- Deal with split messages by always popping from the buffer on unparsed

### Added
- Final progress_update message on print completion to dummy printer 

## [0.5.0] - 2016-07-02
### Added
- delete_gcode_file API method
- Final progress_update message on print completion 

### Fixed
- Print hang bug by adding regex to match split "ok" message from Marlin
- Single-nozzle regex too permissive and matching dual-nozzle lines

## [0.4.0] - 2016-05-02
### Added
- Frontend auto-reconnect on disconnect

### Changed
- Marlin serial buffer increased from 4 to 5
- Long log messages now trunacted to max 75 chars

## [0.3.0] - 2016-04-02
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
