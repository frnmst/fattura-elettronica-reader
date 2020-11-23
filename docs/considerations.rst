Considerations
==============

Purpose
-------

This software aims at:

- correctness

  - XML files are validated whenever possible

- integrity

  - a checksum is performed on the invoice file

- security

  - all cryptographical signature and certificates must be valid
  - invoice attachments are examined before saving them permanently

- privacy

  - works offline once you have downloaded the necessary files

Pipeline
--------

See the definition of pipeline:

- https://en.wikipedia.org/wiki/Pipeline_(software)

In this software, a pipeline is a sequence of steps that given the signed invoice file
and its metadata file makes it possible to obtain:

- various integrity and authenticity verifications
- the html output of the invoice file
- the extraction of embedded attachments

Description
```````````

Without entering in too much detail (you can read the source code for that),
we can divide the pipeline into three main steps:

===========     ===================================================
Step number     Actions
===========     ===================================================
1               compare metadata file content with the invoice file
2               check invoice signature and signer's certificate
3               generate outputs
===========     ===================================================

Software dependencies
---------------------

OpenSSL
```````

Support
~~~~~~~

Due to the lack of support for most of the PKCS#7 functionality in
PyOpenSSL, all OpenSSL operations are performed using the ``subprocess``
module which calls the ``openssl`` binary installed on the system.

See also:

- https://stackoverflow.com/questions/45104923/pyopenssls-pkcs7-object-provide-very-little-information-how-can-i-get-the-sha1/45111623#45111623
- https://stackoverflow.com/questions/45782506/is-there-any-python-package-for-parsing-pkcs7?rq=1

Bug
~~~

There are problems with recent versions of OpenSSL concerning PKCS#7 file decoding:

- https://github.com/eniocarboni/p7m/issues/4
- https://github.com/eniocarboni/p7m/issues/7
- https://www.mail-archive.com/openssl-users@openssl.org/msg85901.html

A possible solution it use an older system. If you really trust the file you can
disable signature checking with the appropriate option. I strongly discourage
the latter solution since if you cannot prove its authenticity the invoice has no legal
value.

lxml vs defusedxml
``````````````````

I decided to use lxml because it supports XML stylesheets (XSLT) as
defusedxml does not.

At first, using defusedxml seemed the best bet because of
the increased security:

- https://github.com/tiran/defusedxml#python-xml-libraries

There is the possibility to use defusedxml anyway by simply
editing the API file like this:


::


    import defusedxml.ElementTree as ET


instead of:


::


    import lxml.etree as ET


You must also add defusedxml and re-install the requirements as described
in the contributing section.


Official documentation
----------------------

========================================  =========================================================================  =======================================================================
Type                                      Current                                                                    Obsolete
========================================  =========================================================================  =======================================================================
Nomativa                                  https://www.fatturapa.gov.it/it/norme-e-regole/normativa/                  - https://www.fatturapa.gov.it/export/fatturazione/it/normativa/f-1.htm
Documentazione fatturaPA                  https://www.fatturapa.gov.it/it/norme-e-regole/documentazione-fatturapa/   - https://www.fatturapa.gov.it/export/fatturazione/it/normativa/f-2.htm
Documentazione Sistema d'Interscambio     https://www.fatturapa.gov.it/it/norme-e-regole/DocumentazioneSDI/          - https://www.fatturapa.gov.it/export/fatturazione/it/normativa/f-3.htm
========================================  =========================================================================  =======================================================================

Considerations
``````````````

Not having access to all schema files is a problem since there is no way to tell if

- the metadata file,
- the trusted list file,
- the XML stylesheet file

are correct and conforming to specifications.

If you find these files please let me know and/or open a pull request.

Downloading of the W3C file
```````````````````````````

The W3C schema file is a dependency for the invoice schema file and it needs to be cached
because the XML resolver can go in timeout.

Sometimes it takes more than one minute to download this file.

Fattura PA vs Fattura B2B
``````````````````````````

Digital signature
~~~~~~~~~~~~~~~~~

Some websites say that digital signature of the *Fattura PA* is compulsory and
in other cases it is not.

- https://www.agendadigitale.eu/documenti/fatturazione-elettronica/fattura-elettronica-e-firma-come-garantire-autenticita-dellorigine-e-integrita-del-contenuto/

If you find any official source please let me know and/or open a pull request.

Support for non-signed invoice files has been added because of at least one
reported case.

Closing note
------------

Although this whole system has its merits, it has been put into production
with lots of missing pieces (see notes above). Given the importance of it I think this
is unacceptable. I will not make any more comments because I may risk legal actions...
