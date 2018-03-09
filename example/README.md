# Example

To run the example application, make sure you have the required
packages installed.  You can do this using following commands :

```shell
virtualenv -p python3.6 .venv
source .venv/bin/activate
pip install -r example/requirements.txt
```

This assumes you already have ``virtualenv`` and ``virtualenvwrapper``
installed and configured.

Next, you can setup the django instance using :

```shell
python example/manage.py check
python example/manage.py migrate
python example/manage.py createsuperuser --username=admin --email=admin@example.com
python example/manage.py cities --import=all
python example/manage.py airports
```

And run it :
```shell
python example/manage.py runserver
```


