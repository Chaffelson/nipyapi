.. highlight:: shell

=================
Development Notes
=================

A collection point for information about the development process for future collaborators


Decision Points
---------------

* Using Swagger 2.0 instead of OpenAPI3.0 as it (currently as of Aug2017) has wider adoption and completed codegen tools


Docker Test Environment
-----------------------

There is an Apache NiFi image available on Dockerhub::

    docker pull apache/nifi:1.2.0

There is a configuration file for launching it in ./test_env_config for convenience when working in Pycharm

Testing on OSX
--------------

There is a known issue with testing newer versions of Python on OSX.
You may receive an error reporting [SSL: CERTIFICATE_VERIFY_FAILED] when trying to install packages from Pypi

You can fix this by running the following commands::

    export PIP_REQUIRE_VIRTUALENV=false
    /Applications/Python\ 3.6/Install\ Certificates.command

Generate Swagger client
-----------------------

1. build relevant version of NiFi from source
2. retrieve swagger.json from NiFi build::

    cp ./nifi/nifi-nar-bundles/nifi-framework-bundle/nifi-framework/nifi-web/nifi-web-api/target/swagger-ui/swagger.json /tmp

3. download swagger-codegen-cli of relevant version::

    wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.2.3/swagger-codegen-cli-2.2.3.jar -O /tmp/swagger-codegen-cli.jar

4. run codegen for appropriate language to a convenient working directory::

    java -jar /tmp/swagger-codegen-cli.jar generate -i /tmp/swagger.json -l python -o /tmp/nifi-python-swagger-client

Release Process
---------------

This assumes you have virtualenvwrapper, git, and appropriate python versions installed, as well as the necessary test environment:

- update History.rst
- check setup.py
- check requirements.txt and requirements_dev.txt
- Commit all changes
- in bash::

    cd ProjectDir
    source ./my_virtualenv/bin/activate
    bumpversion patch|minor|major
    python setup.py develop
    tox
    python setup.py test
    python setup.py build_sphinx
    # check docs in build/sphinx/html/index.html
    python setup.py sdist bdist_wheel
    mktmpenv
    pip install pip install path/to/nipyapi-0.3.1-py2.py3-none-any.whl  # for example
    # Run appropriate tests, such as usage tests etc.
    deactivate
    # You may have to reactivate your original virtualenv
    twine upload dist/*
    # You may get a file exists error, check you're not trying to reupload an existing version
    git push --follow-tags

- check build in TravisCI
- check docs on ReadTheDocs
- check release published on Github and PyPi
