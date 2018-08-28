=======
History
=======

0.10.3 (2018-08-28)
-------------------

| Minor bugfix for versioning/deploy_flow_version to resolve additional edge case for version number type


0.10.2 (2018-08-27)
-------------------

| BugFix for Issue #66 in security/get_access_policy_for_resource where NiFi Api is not expecting a resource_id to be submitted

0.10.1 (2018-08-21)
-------------------

| Minor bugfix for versioning/deploy_flow_version where version number should be a str instead of int


0.10.0 (2018-08-03)
-------------------

| Updated NiFi client for 1.7.1 release
| Updated NiFi-Registry client for 0.2.0 release

**Key Changes**

* Reworked NiFi-Registry pytest setup to support multiple versions
* Changed schedule_processor to use component. rather than status. tests as they are more reliable
* Swtiched Docker configs to use explicit versions instead of latest for more consistent behavior across environents

**Version Changes**

* Deprecated testing against NiFi-1.5.0 due to host headers issue - recommend users to upgrade to at least NiFi-1.6.0
* Deprecated testing against NiFi-1.4.0 as superfluous
* Added testing for NiFi-1.7.1 and NiFi-Registry-0.2.0


0.9.1 (2018-05-18)
------------------

| Updated Demos for 0.9 release

**New Features**

* Added a new demo for Flow Development LifeCycle which illustrates the steps a user might automate to promote Versioned Flows between NiFi environments
* Check out nipyapi.demo.fdlc to see more details

0.9.0 (2018-05-16)
------------------

| Updated NiFi client to 1.6.0 release

**Potentially Breaking Changes**

*Users should check the updated documentation and ensure their tests pass as expected*

* Several NiFi client API calls were inconsistently CamelCase'd and have been renamed in the upstream NiFi release, I have honoured those changes in this release. If you use them please check your function names if you get an error

**New Features**

* Added functionality to Deploy a versioned flow to the canvas. This was an oversight from the 0.8.0 release. Function is creatively named ./versioning/deploy_flow_version

**Other Notes**

* Updated the Issue Template to also ask how urgent the problem is so we can priortise work
* Where possible we have switched to using the Apache maintained Docker containers rather than our own, there should be no impact to this unless you were relying on some edge part of our test compose files


0.8.0 (2018-03-06)
------------------

| Introducing Secured environment support, vastly expanded Versioning support including import/export.
| Fixed Templates, better documentation, more demos, and NiFi version backtesting.

**Potentially Breaking Changes**

*Users should check the updated documentation and ensure their tests pass as expected*

* Import/Export of Flow Versions was reworked significantly and renamed to correct bugs and remove coding complications and be generally more obvious in its behavior
* Template upload/download reworked significantly to remove direct reliance on requests and correct bugs in some environments
* Reworked many list/get functions to be more standardised as we stabilise the approaches to certain tasks. This should not change again in future
* Standardised bad user submission on AssertionError, bad API submission errors on ValueError, and general API errors on ApiException. This standard should flow forwards
* Switched ruamel.yaml from >15 to <15 as advised in the project documentation, as >15 is not considered production ready

**Known Issues**

* Python2 environments with older versions of openssl may run into errors like 'SSLV3_ALERT_HANDSHAKE_FAILURE' when working in secured environments. This is not a NiPyApi bug, it's a problem with py2/openssl which is fixed by either upgrading openssl or moving to Python3 like you know you should

**New Features**

* Added support for working with secured NiFi environments, contributed by KevDoran
    * Added demo compatibility between secured_connection and console to produce a rich secured and version-controlled demo environment
    * Added many secured environment convenience functions to security.py
    * Integrated tokenAuth support throughout the low-level clients
* Added simple Docker deployment support in utils module for test, demo, and development
* Standardised all documentation on more readable docstrings and rst templates across the entire codebase
* Significantly expanded versioning support, users should consult the refreshed documentation
* Added experimental support for cleaning queues, process_groups, and setting scheduling of various components
* Many calls now have an auto-refresh before action option to simplify applying changes
* Implemented short and long wait controls for relevant functions to allow more deterministic changes
* Implemented generic object-list-filtering-for-a-string-in-a-field for many response get/list types
* Standardised many responses to conform to a common response contract: None for none, object for single, and list-of-objects for many
* Implemented import/export to json/yaml in versioning
* Added regression/backtesting for many functions going back through major release versions to NiFi-1.1.2. More details will be obvious from reading tests/conftest.py
* Test suites now more reliably clean up after themselves when executed on long-running environments
* Apparently logging is popular, so standard Python logging is now included

**Other notes**

* Various low-level SDK bugfixes corrected in the swagger spec and updated in the provided client
* Enhanced Template and Flow Versioning to handle significantly more complex flows
* Significantly enhanced testing fixtures
* Refactored several common functions to utils.py, and moved several common configurations to config.py
* versioning.get_flow will now export the raw Registry object for convenience when serialising flows
* Significantly improved Py2/Py3 compatibility handling, and import management within the package
* Removed docs dependency on M2R by converting everything over to reStructuredText

0.7.0 (2018-01-30)
------------------

* Updated project to support NiFi-1.5.0 and NiFi-Registry-0.1.0
* Merged api clients into main codebase, deprecated external client requirement
* Created centralised project configuration and test configuration
* Updated automated test environment to consistent docker for local and Travis
* Removed procedurally generated boilerplate stub tests to improve readability
* Moved pytest fixtures into conftest and expanded dramatically
* Added limited support for processor and process group scheduling
* Added support for all common Nifi-Registry calls
* Added a demo package to provide an interactive test and demo console
* Significant readme, contribution, and other documentation refresh
* Expanded CRUD support for most processor, process group and related tasks


0.6.1 (2018-01-04)
------------------

* Added requested functions to find and list Processors on the canvas
* Fixed list all process groups to include the root special case properly


0.6.0 (2017-12-31)
------------------

* Refactored many functions to use native NiFi datatypes instead of generics
* Standardised several call names for consistency
* Updated examples
* Created additional tests and enhanced existing to capture several exceptions


0.5.1 (2017-12-07)
------------------

* Added template import/export with working xml parsing and tests
* Added a ton of testing and validation steps
* Cleared many todos out of code by either implementing or moving to todo doc


0.5.0 (2017-12-06)
------------------

* migrated swagger_client to separate repo to allow independent versions
* refactored wrapper Classes to simpler functions instead
* cleaned up documentation and project administrivia to support the split

0.4.0 (2017-10-29)
------------------

* Added wrapper functions for many common Template commands (templates.py)
* Added new functions for common Process Groups commands (canvas.py)
* Significant test framework enhancements for wrapper functions
* Many coding style cleanups in preparation for filling out test suite
* Added linting
* Cleaned up docs layout and placement within project
* Integrated with TravisCI
* Dropped Python2.6 testing (wasn't listed as supported anyway)
* Updated examples and Readme to be more informative

0.3.2 (2017-09-04)
------------------

* Fixed bug where tox failing locally due to coveralls expecting travis
* Fixed bug where TravisCI failing due to incorrectly set install requirements
* Fixed bug where swagger_client not importing as expected


0.3.1 (2017-09-04)
------------------

* Fixed imports and requirements for wheel install from PyPi

0.3.0 (2017-09-04)
------------------

* Created basic wrapper structure for future development
* Added simple usage functions to complete todo task
* Added devnotes, updated usage, and various sundry other documentation cleanups
* Split tests into subfolders for better management and clarity
* Added Coveralls and License Badge
* Removed broken venv that ended up in project directory, added similar to ignore file
* Changed default URL in the configuration to default docker url and port on localhost

0.2.1 (2017-08-26)
------------------

* Fixed up removal of leftover swagger client dependencies

0.2.0 (2017-08-25)
------------------

* Merge the nifi swagger client into this repo as a sub package
    * Restructured tests into package subfolders
    * Consolidate package configuration
    * Setup package import structure
    * Updated usage instructions
    * Integrate documentation

0.1.2 (2017-08-24)
------------------

* Created basic integration with nifi-python-swagger-client

0.1.1 (2017-08-24)
------------------

* Cleaned up base project and integrations ready for code migration

0.1.0 (2017-08-24)
------------------

* First release on PyPI.
