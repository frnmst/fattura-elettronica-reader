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
~~~~~~~~~~~~~~~~~~

I decided to use lxml because it supports XML stylesheets (XSLT).
Infact, defusedxml does not support XSLT.

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


::


    defusedxml==0.5.0


Official documentation
----------------------

- https://www.fatturapa.gov.it/export/fatturazione/it/normativa/f-1.htm
- https://www.fatturapa.gov.it/export/fatturazione/it/normativa/f-2.htm
- https://www.fatturapa.gov.it/export/fatturazione/it/normativa/f-3.htm

XML schemas for document validations
````````````````````````````````````

Most of XML schemas seem to be non-existing. Only the one for the
invoice file was found, and was reported by lxml as incorrect,
but according to the server the schema was last modified on
``Tue, 25 Jun 2019 10:16:31 GMT``, so they fixed an offending ``xsd`` typo:

- https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.2.1/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd

Not having access to all schema file is a problem since there is no way to tell if

- the metadata file,
- the trusted list file,
- the XML stylesheet file

are correct and conforming to specifications.

If you find these files please let me know and/or open a pull request.

Downloading of the W3C file
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The W3C schema file is a dependency for the invoice schema file and it needs to be downloaded 
separately. For some reason the downloading of this file takes a few seconds.

Technical differences between "Fattura PA", "Fattura B2B" and other
```````````````````````````````````````````````````````````````````

Digital signature
~~~~~~~~~~~~~~~~~

Some websites say that digital signature of the "Fattura PA" is compulsory and 
in other cases it is not.

If you find any official source please let me know and/or open a pull request.

Support for non-signed invoice files has been added because of at least one 
reported case.

Closing note
------------

Although this whole system has its merits, it has been put into production
with lots of missing pieces (see notes above). Given the importance of it I think this
is unacceptable. I will not make any more comments because I may risk legal actions...
