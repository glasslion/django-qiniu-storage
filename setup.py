from setuptools import setup, find_packages
import codecs
import os
import re

if os.environ.get('USER','') == 'vagrant':
    del os.link


# Get the long description from the relevant file
try:
    with codecs.open('DESCRIPTION.rst', encoding='utf-8') as f:
        long_description = f.read()
except IOError:
    # When travis install the package from the github clone,
    # it cant's find DESCRIPTION.rst
    long_description = ""

setup(
    name="django-qiniu-storage",
    version='2.3.1',
    description="Django storage for Qiniu Cloud Storage",
    long_description=long_description,

    # The project URL.
    url='https://github.com/glasslion/django-qiniu-storage',

    # Author details
    author='Lijian Zhou',
    author_email='glasslion@gmail.com',

    # Choose your license
    license='MIT',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Framework :: Django',
        'Environment :: Plugins',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='qiniu django',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages.
    packages=find_packages(exclude=["contrib", "docs", "tests*","demo-project"]),

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed.
    install_requires = ['qiniu>=7.1.0', 'six', 'requests'],
)
