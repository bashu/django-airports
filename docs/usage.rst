=====
Usage
=====

To use django-airports in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'airports.apps.AirportsConfig',
        ...
    )

Add django-airports's URL patterns:

.. code-block:: python

    from airports import urls as airports_urls


    urlpatterns = [
        ...
        url(r'^', include(airports_urls)),
        ...
    ]
