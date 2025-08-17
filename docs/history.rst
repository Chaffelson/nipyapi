=======
History
=======

 

1.0.0 (2025-01-15)
-------------------

| Major migration to Apache NiFi/Registry 2.x (tested against 2.5.0). Drops 1.x support on main.

- Build system and workflow improvements:

  - Added comprehensive ``rebuild-all`` Makefile target for complete project regeneration from clean slate
  - Enhanced ``clean-all`` target to remove ALL artifacts: build, clients, docs, coverage, temporary files
  - Optimized rebuild flow to avoid unnecessary infrastructure cycling during client generation
  - Streamlined client generation workflow using existing scripts in ``resources/client_gen/``
  - Smart certificate regeneration: ``make certs`` auto-detects and stops running containers to prevent SSL timing issues

- Documentation modernization and restructuring:

  - Complete overhaul of Sphinx documentation generation with custom structured approach
  - Replace monolithic API reference pages with modular, navigable structure addressing GitHub issue #376
  - Flat API structure with individual pages for all 39 NiFi APIs and 13 Registry APIs for optimal navigation
  - Comprehensive models documentation with all 394 NiFi and 85 Registry model classes auto-discovered
  - Individual documentation pages for each core module improving navigation and maintainability
  - Template-level docstring formatting fixes ensuring Sphinx-compliant generated client code
  - Enhanced generated docstrings with proper Google-style formatting, primitive type handling, and method distinction
  - Added client architecture documentation explaining base vs _with_http_info methods, callbacks, and error handling
  - Direct GitHub source code links for all functions and classes with line-level precision
  - Modern installation guide with current best practices, virtual environments, and dependency management
  - Auto-generated dependencies documentation from actual requirements files eliminating maintenance burden
  - Zero Sphinx warnings achieved through systematic docstring and formatting improvements
  - Enhanced Sphinx configuration with modern extensions and improved navigation depth

- Client generation improvements:

  - Fix Mustache template formatting to produce clean, Sphinx-compliant docstrings in generated code
  - Correct parameter documentation spacing and structure in API templates
  - Remove invalid template syntax causing generation errors

- Core: switch low-level clients to NiFi/Registry 2.5.0 OpenAPI 3 specs (swagger-codegen 3.0.68)
- Remove Templates feature (deprecated in NiFi 2.x): delete `nipyapi/templates.py`, related tests/resources; remove imports; adapt fixtures
- Docker: update images to NiFi/Registry 2.5.0
  - Secure docker setups (secure-ldap, secure-mtls) now use generated PKCS12 keystore/truststore via certs.env
- OperationIds: adopt upstream suffixed names from OAS 3 (e.g., `update_run_status1`)

- Generator: consolidate NiFi/Registry generation (`resources/client_gen/generate_api_client.sh`); add JSON enum normalizer (`resources/client_gen/normalize_openapi_enums.py`) as temporary workaround for upstream enum issues
- Templates: `api_client.mustache` use raw regex strings to avoid DeprecationWarnings; `model.mustache` fix enum allowed_values; skip None-checks for required readOnly fields; remove callback/threading artifacts and vendor regex modifiers
- Dependencies: replace ruamel.yaml with PyYAML (reduces dependency count while maintaining full compatibility)
- Build: modernize build system using python -m build instead of deprecated setup.py; add comprehensive make targets (dist, wheel, sdist, check-dist, test-dist) with proper validation; add distribution import validation script for release process; remove legacy 1.x API definitions and temporary files (saves ~13MB)
- Testing: add Codecov integration with pytest-cov for modern coverage reporting; add GitHub Actions CI workflow with full Docker NiFi integration tests and coverage upload

- Canvas (2.x API): use `ProcessGroupsApi.create_controller_service1(id=...)`; controller scheduling via `ControllerServicesApi.update_run_status1(...)`; update renamed APIs `FlowFileQueuesApi`, `FunnelsApi`
- Security (2.x): replace removed `AccessApi.get_access_status` with `FlowApi.get_current_user()`; Registry readiness via `AboutApi.get_version()`
 
 - Authentication and client generation:

   - Switch to spec-driven `bearerAuth`; removed template-injected `tokenAuth`; `set_service_auth_token()` now targets `bearerAuth` by default
   - Temporary augmentation scripts declare securitySchemes and per-operation security until upstream specs are fixed:

     - `resources/client_gen/augment_nifi_security.py`
     - `resources/client_gen/augment_registry_security.py`

   - Once upstream fixes land, augmentation scripts will be removed and clients regenerated without local workarounds
   - Upstream tracking for NiFi Core bearer scheme: [NIFI-14852](https://issues.apache.org/jira/browse/NIFI-14852)

- Utils: YAML dump now forces block style to avoid ruamel parsing of inline flow mappings; `dump`/`load` continue safe YAML

- Dependencies: explicitly include `urllib3`, `certifi`, `requests` used by generated clients
  - Prune template-era deps (e.g., `lxml`, `xmltodict`) as Templates are removed

- Tests: remove Templates tests; adapt for 2.x behavior; full suite green across profiles
  - single-user: 88 passed, 22 skipped
  - secure-ldap: 107 passed, 3 skipped
  - secure-mtls: 88 passed, 22 skipped

- Tests / Profiles:
  - Centralize profile configuration in `tests/conftest.py` with clear docstrings; env overrides respected.
  - Support `NIPYAPI_AUTH_MODE=single-user|secure-ldap|secure-mtls` with sensible defaults and repo-local TLS assets for secure profiles.
  - Remove duplicate TLS logic; consistent one-time setup and safe teardown.
  - `Makefile`: simplified `make test` runner; defers configuration to conftest; Docker targets use stable COMPOSE_PROJECT_NAME, quiet down with --remove-orphans.

- Client utils:
  - Remove ad-hoc env reads in `utils.set_endpoint`; rely on preconfigured values only.

- Examples and authentication improvements:
  - Modernized ``examples/fdlc.py`` with proper multi-environment workflow (single-user dev, secure-ldap prod)
  - Added security bootstrapping for both NiFi and Registry environments following test patterns
  - Enhanced authentication using proven conftest.py configurations for reliable connectivity
  - Added interactive mode support with clear step-by-step workflow guidance and exit instructions
  - Fixed SSL certificate handling for self-signed certificates using repo-local CA certificates
  - Standardized password consistency: ``password1234`` for single-user, ``password`` for secure-ldap
  - Improved error handling in ``nipyapi.versioning.save_flow_ver`` with type validation and descriptive messages
  - Removed deprecated ``examples/console.py`` (all code was commented out and superseded by modernized examples)

- Resource pruning:
  - Deleted legacy client-gen artifacts and old docker scaffolding under `resources/` no longer used in 2.x workflow.

- Pruning: removed deprecated docker and test scaffolding
  - Deleted `resources/docker/tox-full/` and `resources/test_setup/setup_centos7.sh`
  - Removed docker/localdev variant (upstream provides official images)
  - Consolidation to a single docker-compose with profiles is planned (current secure-ldap and secure-mtls updated)
  - Removed tox from development flow; deleted top-level `tox.ini`, replaced docs with Makefile-based testing
  - Removed legacy dev deps (nose, pluggy, coveralls, randomize, cryptography) from requirements_dev; dropped Coveralls badge from README

- Upstream: track enum inconsistencies in [NIFI-14850](https://issues.apache.org/jira/browse/NIFI-14850)
  - Track missing bearer security scheme in NiFi Core OpenAPI: [NIFI-14852](https://issues.apache.org/jira/browse/NIFI-14852)

0.22.0 (2025-03-25)
--------------------

| Updated low level clients for NiFi & Registry 1.28.1 release
| Updates to supported Python versions, handing Template deprecation in NiFi-2.x, and Windows development support
| Add support for mTLS for Nifi and Registry

0.21.0 (2024-07-14)
-------------------

| Updated client for NiFi & Registry 1.27.0 release

* Fix API model generator by @michaelarnauts in https://github.com/Chaffelson/nipyapi/pull/356
* issue-360: handle -9 error messages better by @ottobackwards in https://github.com/Chaffelson/nipyapi/pull/361
* Handle plain text response types so json values are correctly returned by @michaelarnauts in https://github.com/Chaffelson/nipyapi/pull/358
* update clients to 1.27.0 by @Chaffelson in https://github.com/Chaffelson/nipyapi/pull/365
* Simplified the use of setattr in recurse_flow, flatten, and list_all_by_kind methods in nipyapi/canvas.py. 
* Added support for key_password in the Configuration class and its usage in nipyapi/nifi/rest.py and nipyapi/registry/rest.py. 
* Fixed the method to retrieve HTTP headers in nipyapi/nifi/rest.py and nipyapi/registry/rest.py. 
* Fixed issue #326 where the latest flow version was not being deployed by default
* Updated pylintrc to match more modern python standards
* Fixes nipyapi.nifi.ProcessGroupsApi.upload_process_group_with_http_info() incomplete #310
* VersionedReportingTask added with appropriate functions
* Move docker requirement to extras to avoid dependency install during standard usage
* Set latest python3 version to 3.12
* Deprecate usage of py.test in favour of newer pytest.
* Update readme

0.20.0 (2024-04-14)
-------------------

| Updated client for NiFi & Registry 1.23.2 release

* Fix ruamel.yaml finally deprecating safe_loader
* Hexoplon added ReportingTaskEntity to registered filters
* ottobackwards fixed the root logger being setup by the libary
* Generally updated test setup and several updated libraries complaining since last release

0.19.1 (2022-08-08)
-------------------

| Updated client for NiFi & Registry 1.17.0 release

* Update docker resources to the latest 1.17 container image
* Fix issue in docker volume mounts where certificates were not readable in new versions of Docker
* Fix issue in test_get_processor_type where new Twitter processor broke existing logic assumptions
* Update readme to note issues with Python 3.10 and removing reference to python 3.5 testing

0.19.0 (2022-05-13)
-------------------

| Updated client for NiFi & Registry 1.16.0 release

* Modify utils.check_version to accept a default version to check against, and remove nested error when version check fails as it is overzealous
* Update test file paths in test_utils in case someone runs tests as root which actually can write to fake devices and therefore break the tests
* Added pylint exclusions for known but unimportant complaints
* Added workaround for NiFi 9470 by providing default inherited_parameter_contexts per advice from Chris Sampson in NiPyAPI Issue #305
* Updated NiFi and Registry versions in Docker compose configs to use latest 1.16.1 builds


0.18.0 (2021-11-29)
-------------------

| Updated client for NiFi & Registry 1.15.0 release

* Moved testing to secured single user by default for NiFi
* Consolidated clients to the 1.15.0 release version for both NiFi and Registry
* Updated logic to support changed working modes in tests
* Corrected minor functional issues for 1.15 in login handling, SSL certs, Parameter Updates and Testing
* Backwards compatibility and Regression tested as requiring no breaking changes

0.17.1 (2021-10-21)
-------------------

| Added gzip as default request header (PR from rsaggino)
| Update ruamel.yaml to 0.17.16
| Update file read/write to explicitly handle encoding, default to UTF8, configurable in nipyapi.config
| Linting and style changes to update to Python 3.9 standards, except where it would break backwards compatibility to Python 2.7
| Test support for Amazon Linux 2, mostly better error handling for filesystem responses

0.17.0 (2021-10-13)
-------------------

| Updated NiFi version and client to 1.13.2
| Updated NiFi-Registry version and client to 0.8.0

* Note that these are the last versions where NiFi and NiFi-Registry are separate codebases

0.16.3 (2021-10-11)
-------------------

| Removed force reset of configuration.password and configuration.username to empty string. This was not increasing security, and was causing unexpected errors for users connecting to multiple services in a single script.
| Add greedy control to versioning.get_registry_bucket and versioning.get_flow_in_bucket to avoid undesirable partial string match.

* Update readme to reflect switch from 'master' branch naming to 'main'.
* Update tox to pin testing to Python 3.8, as Python 3.9 is producing unexpected and unrelated SSL failures
* Minor lint formatting improvements

0.16.2 (2021-02-10)
-------------------

| NOTE: If you are using secured Registry, this release will enforce access controls for the swagger interface which is used to determine which version of Registry is connected in order to correctly provide features - you may have to update your authorizations

* Update requirements.txt to unpin future and lxml
* Update lxml to 4.6.2 or newer to resolve vulnerability
* Pin watchdog to <1.0.0 per their docs to maintain Python2.7 compatibility
* Revert 0.14.3 changes to Authentication handling which introduced basicAuth support but resulted in some NiFi connections appearing incorrectly as Anonymous
* Added simpler basicAuth control to force it via a config switch without changing tokenAuth and other Authorization header behavior during normal usage
* nipyapi.config.global_force_basic_auth is now available for use for this purpose
* Secured Registry users will now require the authorization policy to retrieve the swagger so we may use it to validate which version of
* Registry is in use for feature enablement
* Moved all Security controls in config.py to a common area at the foot of the file
* Removed auth_type from security.service_login as it is now redundant
* Added controls to handle certificate checking behavior which has become more strict in recently versions of Python3, ssl_verify and check_hostname are now handled
* security.set_service_auth_token now has an explicit flag for ssl host checking as well
* Fix oversight where improved model serialisation logic was not correctly applied to Registry
* Removed unusused parameter refresh from parameters.update_parameter_context
* Reduced unecessary complexity in utils.dump with no change in functionality
* Updated client gen mustache templates to reflect refactored security and api client code
* Minor linting and docstring and codestyle improvements
* Set pyUp to ignore Watchdog as it must stay between versions to statisfy py2 and py3 compatibility
* If Client is not instantiated, optimistically instantiate for version checking
* add socks proxy support

0.16.3 (2021-10-11)
-------------------

| Removed force reset of configuration.password and configuration.username to empty string. This was not increasing security, and was causing unexpected errors for users connecting to multiple services in a single script.
| Add greedy control to versioning.get_registry_bucket and versioning.get_flow_in_bucket to avoid undesirable partial string match.

* Update readme to reflect switch from 'master' branch naming to 'main'.
* Update tox to pin testing to Python 3.8, as Python 3.9 is producing unexpected and unrelated SSL failures
* Minor lint formatting improvements

0.16.2 (2021-02-10)
-------------------

| NOTE: If you are using secured Registry, this release will enforce access controls for the swagger interface which is used to determine which version of Registry is connected in order to correctly provide features - you may have to update your authorizations

* Update requirements.txt to unpin future and lxml
* Update lxml to 4.6.2 or newer to resolve vulnerability
* Pin watchdog to <1.0.0 per their docs to maintain Python2.7 compatibility
* Revert 0.14.3 changes to Authentication handling which introduced basicAuth support but resulted in some NiFi connections appearing incorrectly as Anonymous
* Added simpler basicAuth control to force it via a config switch without changing tokenAuth and other Authorization header behavior during normal usage
* nipyapi.config.global_force_basic_auth is now available for use for this purpose
* Secured Registry users will now require the authorization policy to retrieve the swagger so we may use it to validate which version of
* Registry is in use for feature enablement
* Moved all Security controls in config.py to a common area at the foot of the file
* Removed auth_type from security.service_login as it is now redundant
* Added controls to handle certificate checking behavior which has become more strict in recently versions of Python3, ssl_verify and check_hostname are now handled
* security.set_service_auth_token now has an explicit flag for ssl host checking as well
* Fix oversight where improved model serialisation logic was not correctly applied to Registry
* Removed unusused parameter refresh from parameters.update_parameter_context
* Reduced unecessary complexity in utils.dump with no change in functionality
* Updated client gen mustache templates to reflect refactored security and api client code
* Minor linting and docstring and codestyle improvements
* Set pyUp to ignore Watchdog as it must stay between versions to statisfy py2 and py3 compatibility
* If Client is not instantiated, optimistically instantiate for version checking
* add socks proxy support

0.15.0 (2020-11-06)
-------------------

| Updated NiFi client and helpers to 1.12.1, Registry client to 0.7.0
| Release to include new fixes and features in baseline, work continues on improving different Authentication methods


* Added new Parameter contexts API to docs
* Resolved bug where funnel position did not honour requested location (thanks @geocali)
* Fixed issue where users expected exact search by default but some functions were silently using greedy search (thanks @razdob15)
* Change deploy_template to use floats for deployment instead of int (thanks @bgeisberger)
* Fixed creation of empty user groups (thanks @razdob15)

0.14.0 (2019-11-06)
-------------------

| Updated NiFi client and helpers to 1.10.0


0.13.3 (2019-10-09)
-------------------

| Updated NiFi-Registry client for 0.5.0
| Several Issues closed as bugfixes
| Many canvas operations sped-up through refactoring of recursive code to fast iterators


0.13.0 (2019-04-22)
-------------------

| Updated NiFi client for 1.9.1
| Major rework of security.py to handle TLS and BasicAuth scenarios
| Major rework for test_security.py to cover Issues and common use cases
| Update 'set_endpoint' to easily handle TLS and BasicAuth scenarios if https is set

* Add default BasicAuth params to config
* Add default 'safe chars' to config for URL encoding bypass where '/' is in a string
* Add 'bypass_slash_encoding' to utils.py to simplify conditionally allowing '/' in a string
* Update Docker compose files for Secure and tox-full environments to latest NiFi versions
* Add global test controls to top of conftest for default, security, and regression test modes
* Add fixtures to conftest for user and usergroup testing in secure scenarios
* Update fixtures to better handle mixed secure and insecure test environments


0.12.0 (2018-12-20)
-------------------

| Updated NiFi client for 1.8.0
| Updated NiFi-Registry client for 0.3.0
| Added Controller Service Management (experimental)
| Added Connections Management (experimental)
| New Project Logo! Kindly provided by KDoran
| Fixed several bugs around how the special root Process Group is handled when listing all Project Groups for various methods

* Various backwards compatibility improvements for handling calls going back to NiFi-1.1.2
* Various speedups for NiFi-1.7+ using descendants functionality to recurse the canvas
* Ability for various methods to specify a Process Group to use as the parent instead of always using root
* Better username/password handling in security.py and config.py
* Support for global ssl_verify squashing in config.py
* Added swagger for 1.8.0 to project resources against potential future validation requirements
* Added versioned deployment convenience functions for finding sensitive and invalid processors, should make it easier to update properties when importing to a new canvas
* Added summary options to several calls to return simple objects suitable for quick processing rather than full objects that need to be parsed
* Added utils.infer_object_label_from_class to make it easier to create connections between objects
* Updated compound methods like delete_process_group to also handle connections and controllers elegantly if requested
* Various codestyle and testing improvements



0.11.0 (2018-10-12)
-------------------

| Added steps to fdlc demo to show sensitive and invalid processor testing and behavior during deployment
| Added list_sensitive_processors and list_invalid_processors to nipyapi.canvas
| Added simple caching capability for certain calls to nipyapi.config
| Added placeholder tests for new functionality against next refactoring and integration run
| Missing assertion test in get_process_group_status
| deprecated use of tests_require setup.py as current best-practice
| Update ruamel.yaml to support Python 3.7 with passing tests
| Added test for docker image already present to avoid excessive downloading
| Added option to recurse from a given pg_id, rather than always from root, to several canvas functions
| Added default verify_ssl and ssl error squashing to config for user convenience
| Added filter option to specify whether exact or greedy matching should be used, still greedy by default
| Added hard logout when changing endpoint to ensure tokens are refreshed
| Updated tests
| updating travis to build all branches
| Fix travis for Python 3.7 testing support
| Fix edge case in delete process group where templates stop the revision from being refreshed
| Fixed test case to decode string correctly in old python versions
| Fixed race condition in test where not all processors started before test executes
| bugfix for missing status value in Processor DTO
| Updating pylint to ignore import errors on standard packages
| added logging to docker image control
| Bump version: 0.10.3 → 0.11.0
| Install requirements reset

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
