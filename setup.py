import glob
import os
from setuptools import setup

import offlinecdn

# read in the description from README
with open("README.rst") as stream:
    long_description = stream.read()

github_url = 'https://github.com/gabegaster/django-offlinecdn'

# read in the dependencies from the virtualenv requirements file
dependencies = []
filename = os.path.join("requirements", "python")
with open(filename, 'r') as stream:
    for line in stream:
        package = line.strip().split('#')[0]
        if package:
            dependencies.append(package)

setup(
    name=offlinecdn.__name__,
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
        'django-offlinecdn',
    ],
    install_requires=dependencies,
    zip_safe=False,
)
