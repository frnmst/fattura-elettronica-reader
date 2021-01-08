fattura-elettronica-reader
==========================

|pypiver|    |license|    |pyver|    |downloads|    |gitter|    |dependentrepos|    |buymeacoffee|

.. |pypiver| image:: https://img.shields.io/pypi/v/fattura-elettronica-reader.svg
               :alt: PyPI md-toc version

.. |license| image:: https://img.shields.io/pypi/l/fattura-elettronica-reader.svg?color=blue
               :alt: PyPI - License
               :target: https://raw.githubusercontent.com/frnmst/fattura-elettronica-reader/master/LICENSE.txt

.. |pyver| image:: https://img.shields.io/pypi/pyversions/fattura-elettronica-reader.svg
             :alt: PyPI - Python Version

.. |downloads| image:: https://pepy.tech/badge/fattura-elettronica-reader
                 :alt: Downloads
                 :target: https://pepy.tech/project/fattura-elettronica-reader

.. |gitter| image:: https://badges.gitter.im/fattura-elettronica-reader/community.svg
              :alt: Gitter
              :target: https://gitter.im/fattura-elettronica-reader/community

.. |dependentrepos| image:: https://img.shields.io/librariesio/dependent-repos/pypi/fattura-elettronica-reader.svg
                      :alt: Dependent repos (via libraries.io)
                      :target: https://libraries.io/pypi/fattura-elettronica-reader/dependents

.. |buymeacoffee| image:: assets/buy_me_a_coffee.svg
                   :alt: Buy me a coffee
                   :target: https://buymeacoff.ee/frnmst


Validate, extract, and generate printables of electronic invoice files received
from the "Sistema di Interscambio".

Documentation
-------------

http://frnmst.github.io/fattura-elettronica-reader

API examples
------------

fattura-elettronica-reader has a `public API`_.
This means for example that you can you easily read invoice files within another
Python program:


::

    >>> import fattura_elettronica_reader
    >>> data = {
            'patched': True,
            'configuration file': str(),
            'write default configuration file': False,
            'extract attachments': True,
            'metadata file': 'myfile.xml',
            'invoice xslt type': 'ordinaria',
            'no invoice xml validation': False,
            'force invoice schema file download': False,
            'generate html output': True,
            'invoice filename': str(),
            'no checksum check': False,
            'force invoice xml stylesheet file download': False,
            'ignore attachment extension whitelist': False,
            'ignore attachment filetype whitelist': False,
            'ignore signature check': False,
            'ignore signers certificate check': False,
            'force trusted list file download': False,
            'keep original file': True,
            'ignore assets checksum': False,
    }
    >>> fattura_elettronica_reader.assert_data_structure(source='invoice', file_type='p7m', data=data)
    >>> fattura_elettronica_reader.pipeline(
            source='invoice',
            file_type='p7m',
            data=data,
        )


Have a look at the `archive_invoice_files <https://raw.githubusercontent.com/frnmst/automated-tasks/master/src/archiving/archive_invoice_files.py>`_
script in the `automated tasks <https://github.com/frnmst/automated-tasks>`_ repository.

.. _public API: https://frnmst.github.io/fattura-elettronica-reader/api.html

CLI helps
---------


::


    $ fattura_elettronica_reader --help


License
-------

Copyright (c) 2018 Enio Carboni - Italy

Copyright (C) 2019-2021 frnmst (Franco Masotti) <franco.masotti@live.com>

fattura-elettronica-reader is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

fattura-elettronica-reader is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with fattura-elettronica-reader.  If not, see <http://www.gnu.org/licenses/>.

Trusted source
--------------

You can check the authenticity of new releases using my public key.

Instructions, sources and keys can be found at `frnmst.gitlab.io/software <https://frnmst.gitlab.io/software/>`_.
