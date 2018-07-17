=============================
django-airports
=============================

.. image:: https://badge.fury.io/py/django-airports.svg
    :target: https://badge.fury.io/py/django-airports

.. image:: https://travis-ci.org/eracle/django-airports.svg?branch=master
    :target: https://travis-ci.org/eracle/django-airports

.. image:: https://codecov.io/gh/eracle/django-airports/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/eracle/django-airports

Provides airports' related models and data (from [OpenFlights](http://openflights.org/)) that can be used in  django projects, inspired by [django-cities](https://github.com/coderholic/django-cities)

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
