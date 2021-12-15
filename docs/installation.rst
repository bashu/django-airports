============
Installation
============
Requirements (Ubuntu 16.04)::

    sudo apt-get install -y libsqlite3-mod-spatialite binutils libproj-dev gdal-bin


    $ easy_install django-airports

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv django-airports
    $ pip install django-airports

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

