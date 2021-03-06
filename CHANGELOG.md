# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [1.1.0] - 2017-06-30
### Added
- Units translation frame.
- In converter frame units are translated if applicable.

### Changed
- Elements grid in frames are now visually more appealing.
- Datafile (ver. 2) now supports multilingual unit names.
- Many similar variables moved to the one dict variable.

### Fixed
- In converter frame result field is not cleared after units list selection.

## [1.0.2] - 2017-06-13
### Added
- Active language name to the main frame.

### Fixed
- Logical error in function `run()`.

## [1.0.1] - 2017-06-12
### Added
- Ability to change program language in main frame (saves automatically).

## [1.0.0] - 2017-06-07
### Added
- Multilanguage support

### Changed
- Total rewrite of program, parts are moved to module `puc`.

## [0.2.0] - 2017-05-21
### Added
- Program has now icon.
– On close program now informs user about unsaved data, if there is any.
– Program has now about dialog (message box).
– Frames have now titles.
– Some more minor changes.

### Changed
- Some functions used in different frames are moved to the main program object class.

### Fixed
- Error in Conversion frame, when clicking on `Calc`-button.

## [0.1.0] - 2017-05-18
Initial release as a project of MOOC.
