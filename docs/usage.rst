=====
Usage
=====

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
