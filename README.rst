=============================
django-airports
=============================

.. image:: https://img.shields.io/pypi/v/django-airports.svg
    :target: https://pypi.python.org/pypi/django-airports/

.. image:: https://img.shields.io/pypi/dm/django-airports.svg
    :target: https://pypi.python.org/pypi/django-airports/

.. image:: https://img.shields.io/github/license/bashu/django-airports.svg
    :target: https://pypi.python.org/pypi/django-airports/

.. image:: https://app.travis-ci.com/bashu/django-airports.svg?branch=develop
    :target: https://app.travis-ci.com/bashu/django-airports

Provides airports' related models and data (from [OurAirports](http://ourairports.org/)) that can be used in  django projects, inspired by [django-cities](https://github.com/coderholic/django-cities)

Documentation
-------------

The full documentation is at https://django-airports.readthedocs.io.

Quickstart
----------
Requirements (Ubuntu 16.04)::

    sudo apt-get install -y libsqlite3-mod-spatialite binutils libproj-dev gdal-bin

Install django-airports::

    pip install django-airports

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'cities',
        'airports',
        'django.contrib.gis',
        ...
    )


Features
--------

The ```airports``` manage command has options, see ```airports --help``` output.
Second run will update the DB with the latest data from the source csv file.

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
