.. highlight:: shell

=================
Development Notes
=================

A collection point for information about the development process for future collaborators


Decision Points
---------------

* Using Swagger 2.0 instead of OpenAPI3.0 as it (currently as of Aug2017) has wider adoption and completed codegen tools
* We use Google style Docstrings to better enable Sphinx to produce nicely readable documentation


Testing Notes
-------------

When running tests on new code, you are advised to run 'test_default' first, then 'test_regression', then finally 'test_ldap' and/or 'test_mtls'.
Because of the way errors are propagated you may have code failures which cause a teardown which then fails because of security controls, which can then obscure the original error.


Docker Test Environment
-----------------------

There is an Apache NiFi image available on Dockerhub::

    docker pull apache/nifi:latest

There are a couple of configuration files for launching various Docker environment configurations in resources/docker for convenience.

Remote testing on AWS:AL3 with Visual Studio Code on OSX
--------------------------------------------------------

Instructions::

    Deploy a t2.xlarge on EC2, preferably with an elastic IP
    Add the machine as a remote on Visual Studio Code and Connect
    Open up the console and install git so VSCode can clone the repo `sudo dnf install -y git`
    Use the VSCode Source Control plugin to clone nipyapi https://github.com/Chaffelson/nipyapi.git
    You can then open these notes in VSCode with the terminal for easy execution
    Now install dependencies `sudo dnf install -y docker && sudo dnf groupinstall "Development Tools" -y`
    Now ensure docker starts with the OS and gives your user access `sudo systemctl start docker && sudo systemctl enable docker && sudo usermod -a -G docker $USER`
    Restart your terminal, or run `newgrp docker` to get Docker access permissions active
    Install Pip `sudo dnf install python3-pip -y`
    Instal docker compose `sudo curl -L "https://github.com/docker/compose/releases/download/v2.26.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
    I recommend you install PyEnv to manage Python versions `sudo curl https://pyenv.run | bash`
    Follow the instructions to set up your .bashrc
    To build various versions of Python for testing you may also need `sudo dnf install bzip2-devel openssl-devel libffi-devel zlib-devel readline-devel sqlite-devel -y`
    Install the latest supported version of Python for your main dev environment `pyenv install 3.9 2.7 3.12`
    Set these versions as global in pyenv. Use the actual versions with the command `pyenv global 3.9.16 2.7.18 3.12.2`
    Stand up NiFi containers with docker compose profiles (`resources/docker/compose.yml`) and run tests via `make`:
    `PROFILE=single-user make test`, `PROFILE=secure-ldap make test`, `PROFILE=secure-mtls make test`.
    Python2 can be tested using the following steps within a Python2 virtualenv:
    1. Install requirements: pip install -r requirements.txt
    2. Install dev requirements: `pip install -r requirements_dev.txt`
    3. Install package in editable mode with test support: `pip install -e .[test]`
    4. Run tests: `pytest -v -s tests --tb=long -W ignore::urllib3.exceptions.InsecureRequestWarning`

Setup Code Signing
------------------

If you want to sign and push code from your EC2 instance, you'll need to set up code signing. 
Ensuring security of your keys is important, so please protect them with a good secret passphrase

Instructions::

    On your AL2023 instance, replace the default minimal gnupg package with the full one `sudo dnf install --allowerasing gnupg2-full`
    Generate signing keys `gpg --full-generate-key`
    Use the long key ID as your signingkey `git config --global user.signingkey <key here>`
    git config --global commit.gpgsign true
    Add the tty setting for gpg to your ~/.bashrc `export GPG_TTY=$(tty)`

Remote Testing on Centos7
-------------------------

**Deprecated. Instructions kept for legacy reference.**

Deploy a 4x16 or better on EC2 running Centos 7.5 or better, ssh in as root::

    yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    yum update -y
    yum install -y centos-release-scl yum-utils device-mapper-persistent-data lvm2
    yum install -y rh-python36 docker-ce docker-ce-cli containerd.io
    systemctl start docker
    scl enable rh-python36 bash
    sudo curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

Set up remote execution environment to this server from your IDE, such as PyCharm.
Python3 will be in a path like /opt/rh/rh-python36/root/usr/bin/python
These commands are conveniently presented in /resources/test_setup/setup_centos7.sh

You will then want to open up the docker compose directory and run::

    docker compose -f resources/docker/compose.yml --profile single-user up -d

Testing on OSX
--------------

There is a known issue with testing newer versions of Python on OSX.
You may receive an error reporting [SSL: CERTIFICATE_VERIFY_FAILED] when trying to install packages from Pypi

You can fix this by running the following commands::

    export PIP_REQUIRE_VIRTUALENV=false
    /Applications/Python\ 3.6/Install\ Certificates.command

Generate Swagger Client
-----------------------

The NiFi and NiFi Registry REST API clients are generated using swagger-codegen, which is available via a variety of methods:

- the package manager for your OS
- github: https://github.com/swagger-api/swagger-codegen
- maven: https://repo1.maven.org/maven2/io/swagger/swagger-codegen-cli/2.3.1/swagger-codegen-cli-2.4.41.jar
- pre-built Docker images on DockerHub (https://hub.docker.com/r/swaggerapi/swagger-codegen-cli/)

In the examples below, we'll use Homebrew for macOS::

    brew install swagger-codegen

NiFi Swagger Client
~~~~~~~~~~~~~~~~~~~

1. build relevant version of NiFi from source
2. use swagger-codegen to generate the Python client::

    mkdir -p ~/tmp && \
    echo '{ "packageName": "nifi" }' > ~/tmp/swagger-nifi-python-config.json && \
    rm -rf ~/tmp/nifi-python-client && \
    swagger-codegen generate \
        --lang python \
        --config swagger-nifi-python-config.json \
        --api-package apis \
        --model-package models \
        --template-dir /path/to/nipyapi/swagger_templates \
        --input-spec /path/to/nifi/nifi-nar-bundles/nifi-framework-bundle/nifi-framework/nifi-web/nifi-web-api/target/swagger-ui/swagger.json \
        --output ~/tmp/nifi-python-client

3. replace the embedded clients::

    rm -rf /path/to/nipyapi/nipyapi/nifi && cp -rf ~/tmp/nifi-python-client/nifi /path/to/nipyapi/nipyapi/nifi

4. review the changes and submit a PR!

NiFi Registry Swagger Client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Fetch the definition from a running Registry instance at URI: /nifi-registry-api/swagger/swagger.json
2. use swagger-codegen to generate the Python client::


    mkdir -p ~/tmp && \
    echo '{ "packageName": "registry" }' > ~/tmp/swagger-registry-python-config.json && \
    rm -rf ~/tmp/nifi-registry-python-client && \
    swagger-codegen generate \
        --lang python \
        --config swagger-registry-python-config.json \
        --api-package apis \
        --model-package models \
        --template-dir /path/to/nipyapi/swagger_templates \
        --input-spec /path/to/nifi-registry/nifi-registry-web-api/target/swagger-ui/swagger.json \
        --output ~/tmp/nifi-registry-python-client

3. replace the embedded clients::

    rm -r /path/to/nipyapi/nipyapi/registry && cp -rf /tmp/nifi-registry-python-client/swagger_client /path/to/nipyapi/nipyapi/registry

4. review the changes and submit a PR!



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
    Run `make html` in the docs subdir
    # check docs in build/sphinx/html/index.html
    python setup.py sdist bdist_wheel
    mktmpenv  # or pyenv virtualenvwrapper mktmpenv if using pyenv
    pip install path/to/nipyapi-0.3.1-py2.py3-none-any.whl  # for example
    # Run appropriate tests, such as usage tests etc.
    deactivate
    Push changes to Github
    Check dockerhub automated build
    # You may have to reactivate your original virtualenv
    twine upload dist/*
    # You may get a file exists error, check you're not trying to reupload an existing version
    git push --tags

- check docs on ReadTheDocs
- check release published on Github and PyPi
