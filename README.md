django-airports
===

### Airport model and worldwide airport data for Django

----

django-airports provides you with airport related model and data (from [OpenFlights](http://openflights.org/)) that can be used in your django projects.

Authored by [Basil Shubin](https://github.com/bashu), inspired by [django-cities](https://github.com/coderholic/django-cities)

[![Latest Version](https://img.shields.io/pypi/v/django-airports.svg)](https://pypi.python.org/pypi/django-airports/)
[![Downloads](https://img.shields.io/pypi/dm/django-airports.svg)](https://pypi.python.org/pypi/django-airports/)
[![License](https://img.shields.io/github/license/bashu/django-airports.svg)](https://pypi.python.org/pypi/django-airports/)
[![Code Health](https://landscape.io/github/bashu/django-airports/develop/landscape.svg?style=flat)](https://landscape.io/github/bashu/django-airports/develop)

----

### Requirements

You must have *django-cities* installed and configured, see the [django-cities documentation](https://github.com/coderholic/django-cities) for details and setup instructions.

### Setup
On Ubuntu, install gdal library:
```bash
sudo apt-get install gdal-bin
```

Either clone this repository into your project, or install with ```pip install django-airports```

You'll need to add ```airports``` to ```INSTALLED_APPS``` in your project's ```settings.py``` file:

```python
import django

INSTALLED_APPS = (
    ...
    'airports',
)

if django.VERSION < (1, 7):
    INSTALLED_APPS += (
        'south',
    )
```

Then run ```./manage.py syncdb``` to create the required database tables, and ```./manage.py airports``` to import all of the airports data. **NOTE:** This can take some time.

Please see ``example`` application. This application is used to manually test the functionalities of this package. This also serves as a good example.

You need Django 1.4 or above to run that. It might run on older versions but that is not tested.

### Notes

The ```airports``` manage command has options, see ```airports --help``` output.  Verbosity is controlled through LOGGING.

### Development:
Look at the example folder.