# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
* Change output of make_powershell_module from one file to a folder of 
functions (most Powershell projects use this project structure style.)

## [0.2.1] - 2019-02-04
### Added
* Added this Changelog

## [0.2.0] - 2019-01-31
### Added
* Created toy ruby script to verify functionality
* Added some content to make_ruby_script as well based upon it.
* Ruby generated script works

### Changed
* Refactored Main function: Added line for cli options in preamble
* This will allow users to see what options were used to generate this
    specific file.

## [0.1.1] - 2019-01-30
### Added
* Add --add-sample-resp option: Added the ability to add the sample 
    response from the API docs to the function. 
    This can help with understanding what will be returned.
        
## [0.1.0] - 2019-01-30
### Added
* Added support for classes, pylint, func descriptions
* Python script working
* Initial tests have also been written.

## [0.0.0] - 2019-01-27
### Added
* Project Structure

<!---
CHANGELOG TYPES

Added:      for new features. 
Changed:    for changes in existing functionality.
Deprecated: for soon-to-be removed features.
Removed:    for now removed features.
Fixed:      for any bug fixes.
Security:   for vulnerability fixes.
-->

[Unreleased]: https://github.com/pocc/merakygen/compare/v0.2.1...HEAD
[0.2.0]: https://github.com/pocc/merakygen/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/pocc/merakygen/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/pocc/merakygen/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/pocc/merakygen/compare/v0.0.0...v0.1.0
[0.0.0]: https://github.com/pocc/merakygen/commit/36e4cefbafadba3999870bcbcd46bdd8fc7ca351