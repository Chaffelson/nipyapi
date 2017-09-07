=======
History
=======

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
