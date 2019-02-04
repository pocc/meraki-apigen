# Meraki API Code Generator
Generates a $language module out of the existing Meraki API docs webpage. 

## Problem
The Meraki API is constantly adding API calls. Projects exist in multiple
programming languages to access the API but do not get updated. Meraki-Apigen
generates code in your $language with the most recent API docs so that every
supported language has the most recent API call accessors available.

## Description
The module generated will have methods for any new API calls.
For this reason, it may make sense to rerun meraki-apigen occasionally
to get an up-to-date script in your $language.

This is still under active development.

## Features
### CLI options
####--classy (python only)
Aggregate functions into classes based on their API section. 

####--lint (python only)
Use the linting utility for $language to verify code quality for 
generated code.

* Python: pylint
* Ruby: rubocop

####--textwrap
Wrap text according to the style guide for $language.

**Max Line Length**
* Python: 79
* Ruby: 120
* Powershell: 100

**Indentation**
* Python: 4 spaces
* Ruby: 2 spaces
* Powershell: 4 spaces

####--sample-resp
Add the sample response to the function docstring.

### Languages
**Supported**
* python
* ruby

**In Progress**
* powershell

**Planned**
* go
* node

## Usage
### Powershell
import-module merakygen

## Similar Projects
Check out https://github.com/CiscoDevNet/awesome-merakiapis.
Most projects have functionality, but some have been abandoned for years.