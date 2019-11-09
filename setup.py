#
# setup.py
#
# Copyright (C) 2019 Franco Masotti <franco.masotti@live.com>
#
# This file is part of fattura-elettronica-reader.
#
# fattura-elettronica-reader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# fattura-elettronica-reader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fattura-elettronica-reader.  If not, see <http://www.gnu.org/licenses/>.
#

from setuptools import setup, find_packages

setup(
    name='fattura_elettronica_reader',
    version='0.1.0',
    packages=find_packages(exclude=['*tests*']),
    license='GPL',
    description='A utility that is able to check and extract electronic invoice received from the Sistema di Interscambio.',
    long_description=open('README.rst').read(),
    package_data={
        '': ['*.txt', '*.rst'],
    },
    author='Franco Masotti',
    author_email='franco.masotti@live.com',
    keywords='invoice reader SDI',
    url='https://github.com/frnmst/fattura-elettronica-reader',
    python_requires='>=3.5, <4',
    entry_points={
        'console_scripts': [
            'fattura_elettronica_reader=fattura_elettronica_reader.__main__:main',
        ],
    },
    test_suite='tests',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Utilities',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
    ],
    install_requires=['atomicwrites==1.3', 'filetype==1.0', 'appdirs==1.4', 'requests==2.21', 'lxml==4.3'],
)

