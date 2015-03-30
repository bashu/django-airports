django-airports
===

### Airport models and worldwide airport data for Django

----

django-airports provides you with airport related model and data (from [OpenFlights](http://openflights.org/)) that can be used in your django projects.

Authored by [Basil Shubin](http://resume.github.io/?bashu), inspired by [django-cities](https://github.com/coderholic/django-cities)

[![Latest Version](https://pypip.in/version/django-airports/badge.svg)](https://pypi.python.org/pypi/django-airports/)
[![Downloads](https://pypip.in/download/django-airports/badge.svg)](https://pypi.python.org/pypi/django-airports/)
[![License](https://pypip.in/license/django-airports/badge.svg)](https://pypi.python.org/pypi/django-airports/)

----

### Requirements

You must have *django-cities* installed and configured, see the [django-cities documentation](https://github.com/coderholic/django-cities) for details and setup instructions.

### Setup

Either clone this repository into your project, or install with ```pip install django-airports```

You'll need to add ```airports``` to ```INSTALLED_APPS``` in your projects ```settings.py``` file:

```python
INSTALLED_APPS = (
    ...
    'airports',
)
```

Then run ```./manage.py syncdb``` to create the required database tables, and ```./manage.py airports``` to import all of the airports data. **NOTE:** This can take some time.


### Examples

Please see `example` application. This application is used to manually test the functionalities of this package. This also serves as a good example.

### Notes

The ```airports``` manage command has options, see ```airports --help``` output.  Verbosity is controlled through LOGGING.

