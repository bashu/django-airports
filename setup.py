import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

from airports import __version__

setup(
    name='django-airports',
    version=__version__,
    packages=find_packages(exclude=['example']),
    include_package_data=True,
    license='MIT License',
    description='Airport model and worldwide airport data for Django',
    long_description=README,
    url='http://github.com/bashu/django-airports',
    author='Basil Shubin',
    author_email='basil.shubin@gmail.com',
    install_requires=[
        'requests',
        'django-cities',
    ],    
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    zip_safe=False,
)
