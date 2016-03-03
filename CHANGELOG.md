All notable changes to this project will be documented in this file.

* This project adheres to [Semantic Versioning](http://semver.org/).
* This project follows the guidelines outlined on [keepachangelog.com](http://keepachangelog.com/).

## [Unreleased]
### Added
- Error on frontend websocket disconnect
- Clear printer progress on frontend websocket disconnect
- Home all button to home page
- File list hidden when print in progress
- Set temperatures on home page

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
- Non-standard printer state event on initial connection.

### Changed
- New UI from opengb-web.

## [0.0.1] - 2016-01-01
### Added
- Basic printer control functionality.
- Documentation.
- Tests.
- Opengb-web frontend built on Angular.js.
