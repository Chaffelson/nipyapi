.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/Chaffelson/nipyapi/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Nipyapi could always use more documentation, whether as part of the
official Nipyapi docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/Chaffelson/nipyapi/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `nipyapi` for local development.

1. Fork the `nipyapi` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:Chaffelson/nipyapi.git

3. Create and activate a Python 3.9+ virtual environment (venv or conda), then install dev extras::

    # using venv
    $ python -m venv .venv && source .venv/bin/activate
    $ cd nipyapi/
    $ pip install -e ".[dev]"

    # or using conda
    $ conda create -n nipyapi-dev python=3.11 -y
    $ conda activate nipyapi-dev
    $ pip install -e ".[dev]"

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. You may want to leverage the provided Docker profiles for testing and development

 - Install the latest version of Docker
 - Use the provided Docker Compose configuration in `resources/docker/compose.yml` and run tests via Makefile::

    # generate local test certificates (run once or after cleanup)
    $ make certs

    # bring up single-user profile and wait for readiness
    $ make up NIPYAPI_PROFILE=single-user
    $ make wait-ready NIPYAPI_PROFILE=single-user
    # run tests (conftest resolves URLs, credentials, and TLS for the profile)
    $ make test
    # bring everything down when done
    $ make down


6. When you're done making changes, run the test suites for all profiles::

    # convenience shortcuts
    $ make test-all

7. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

8. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should pass lint and all three profile test suites (use `make lint` and `make test-su`, `make test-ldap`, `make test-mtls`).
   Exceptions (e.g., docs-only changes) should note why profile tests were skipped.
4. Pull requests should be created against 'main' branch for new features or work with NiFi-2.x, or maint-0.x for critical patches to NiFi-1.x featuers.
