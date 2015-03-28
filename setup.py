import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-airports',
    version='0.1.1',
    packages=['airports'],
    include_package_data=True,
    license='MIT License',
    description='Airport models and worldwide airport data for Django',
    long_description=README,
    url='http://github.com/bashu/django-airports',
    author='Basil Shubin',
    author_email='basil.shubin@gmail.com',
    install_requires=[
        'requests',
        'django-cities',
    ],    
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    zip_safe=False,
)
