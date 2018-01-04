=======
History
=======

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
