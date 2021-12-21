django-airports
===============

.. image:: https://img.shields.io/pypi/v/django-airports.svg
    :target: https://pypi.python.org/pypi/django-airports/

.. image:: https://img.shields.io/pypi/dm/django-airports.svg
    :target: https://pypi.python.org/pypi/django-airports/

.. image:: https://img.shields.io/github/license/bashu/django-airports.svg
    :target: https://pypi.python.org/pypi/django-airports/

.. image:: https://app.travis-ci.com/bashu/django-airports.svg?branch=develop
    :target: https://app.travis-ci.com/bashu/django-airports

Provides airports' related models and data (from `OurAirports <http://ourairports.org/>`_) that can be used in  django projects, inspired by `django-cities <https://github.com/coderholic/django-cities>`_

Authored by `Basil Shubin <https://github.com/bashu>`_,  and some great
`contributors <https://github.com/bashu/django-airports/contributors>`_.

.. raw:: html

    <p align="center">
        <img src="https://raw.githubusercontent.com/bashu/django-airports/develop/logo.png">
    </p>

Installation
------------

First install the module, preferably in a virtual environment. It can be installed from PyPI:

.. code-block:: shell

    pip install django-airports

Requirements
~~~~~~~~~~~~

You must have *django-cities* installed and configured, see the
`django-cities <https://github.com/coderholic/django-cities>`_ documentation for details and setup instructions.

Setup
-----

First make sure the database support spatial queries, see the `GeoDjango documentation <https://docs.djangoproject.com/en/dev/ref/contrib/gis/>`_ for details and setup instructions.

You'll need to add ``airports`` to ``INSTALLED_APPS`` in your projects ``settings.py`` file:

.. code-block:: python

    INSTALLED_APPS += [
        'airports',
    ]

Then run ``./manage.py migrate`` to create the required database tables.

Import data
-----------

After you have configured all settings, run

.. code-block:: shell

    python manage.py airports

The ``airports`` manage command has options, see ``airports --help`` output.

Second run will update the DB with the latest data from the source csv file.

Contributing
------------

If you like this module, forked it, or would like to improve it, please let us know!
Pull requests are welcome too. :-)

License
-------

``django-airports`` is released under the MIT license.
