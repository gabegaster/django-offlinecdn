import glob
import os
from setuptools import setup

import offlinecdn


github_url = 'https://github.com/gabegaster/django-offlinecdn'

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

# read in the description from README
long_description = read("README.rst")

# read in the dependencies from the virtualenv requirements file
dependencies = [
    "Django==1.8",
    "beautifulsoup4",
    "requests",
]

setup(
    name="django-offlinecdn",
    version=offlinecdn.VERSION,
    description=("A nice way to allow for online-offline development,"
                 " but also use cdn's for package dependencies."),
    long_description=long_description,
    url=github_url,
    download_url="%s/archives/master" % github_url,
    author='Gabe Gaster',
    author_email='gabe.gaster@datascopeanalytics.com',
    license='MIT',
    packages=[
        'offlinecdn',
    ],
    install_requires=dependencies,
    zip_safe=False,
)
