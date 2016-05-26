# socorro-collector

[![Build Status](https://travis-ci.org/mozilla/socorrolib.svg?branch=master)](https://travis-ci.org/mozilla/socorro-collector)

Collector is an application that runs under Apache using mod-python.
Its task is accepting crash reports from remote clients and saving
them in a place and format usable by further applications.

Raw crashes are accepted via HTTP POST. The form data from the POST is
then arranged into a JSON and saved into the local file system. The
collector is responsible for assigning an ooid? (Our Own ID) to the
crash. It also assigns a Throttle? value which determines if the crash
is eventually to go into the relational database.

Should the saving to a local file system fail, there is a fallback
storage mechanism. A second file system can be configured to take the
failed saves. This file system would likely be an NFS mounted file
system.


## installing dependencies

Using virtualenvwrapper and pip:

    mkvirtualenv collector
    # use peep for production
    pip install -r requirements.txt
    # use "python setup.py install" for production
    python setup.py develop


## running

Collector requires the ProductName and Version fields to be set. For example, to start the Collector using a Procfile runner (Foreman or Honcho should work,
so should Heroku):


    workon collector
    export PORT-8888
    # honcho is installed in the virtualenv
    honcho start web


Alternatively, you can run Collector using a standalone built-in webserver (CherryPy):

    workon collector
    export web_server__port='8888'
    socorro collector


## production web service

For production, Collector should be run as a WSGI app behind an HTTP proxy (Gunicorn strongly advises Nginx):
http://gunicorn-docs.readthedocs.org/en/latest/deploy.html


## configuration

Collector supports a number of configuration formats.

Environment variables are recommended.

To see a list of all keys:


    socorro collector --admin.print_conf-env


You can set these in the environment or put then in a `.env` file.

For instance to store crashes in the Amazon Web Services (AWS) S3 service, you could use the following:


    # Store the crash in S3
    storage__crashstorage_class='socorro.external.boto.crashstorage.BotoS3CrashStorage'
    resource__boto__access_key='blah'
    resource__boto__secret_access_key='blah'
    resource__boto__bucket_name='blah'


To generate an INI-style configuration file (with commented-out documentation):


    socorro collector --admin.print_conf-ini


If you want to read a configuration file instead of using environment variables:


  socorro collector --admin.conf-ini


## submitting crashes

The minimum permissible crash report contains the ProductName and Version fields:


  curl -F 'ProductName-Blah' -F 'Version-1.0' 'http://localhost:8888/submit'


You can specify any other form fields you like. A "CrashID" should be returned, and you can find your data in the `./crashes/` directory.


## running tests

    pip install -r requirements

    # all them tests
    nosetests collector

    # with coverage
    nosetests collector --with-coverage --cover-html --cover-package=collector

    # to run a specific test
    nostests collector.unittests.test_submitter_app:TestCase.TestSubmitterApp


## making a release

todo: travis automation to make a release
