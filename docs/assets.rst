Assets
======

fattura-elettronica-reader needs to download some files from the
*Agenzia delle Entrate* website.

Files cannot be included in this repository because of the website copyright.
See https://www.fatturapa.gov.it/it/copyright/index.html

For sake of completeness, the current supported versions
and the SHA-512 and SHA-256 checksums are reported in the following table:

======================================================  ================================================================================================================  ====================================================================================================================================  ====================================================================
Name                                                    URL                                                                                                               SHA-512                                                                                                                                SHA-256
======================================================  ================================================================================================================  ====================================================================================================================================  ====================================================================
XML schema for FatturaPA version 1.2                    https://www.fatturapa.gov.it/export/documenti/fatturapa/v1.2.1/Schema_del_file_xml_FatturaPA_versione_1.2.xsd     ``e1deab535099bfe9aef798c7d75a992f562c2ffa7648e446a8e1c6b894691feecba0cc9dceb02eba02243a951e1423adcac043a49bb8ab255a88b5b3ecf013d2``  ``fecdf8122fa86d80d4ab6901149a4e5390d9880c00de9987d180a2959d54c842``
XML schema for FatturaPA version 1.2.1                  https://www.fatturapa.gov.it/export/documenti/fatturapa/v1.2.1/Schema_del_file_xml_FatturaPA_versione_1.2.1a.xsd  ``2a7c3f2913ee390c167e41ae5618c303b481f548f9b2a8d60dddc36804ddd3ebf7cb5003e5cc6996480c67d085b82b438aff7cc0f74d7c104225449785cb575b``  ``1a14ecdc867a01f447052ff1613688deef6f88bbee522f120be060f68d251976``
XML stylesheet for Fattura Ordinaria version 1.2.1      https://www.fatturapa.gov.it/export/documenti/fatturapa/v1.2.1/Foglio_di_stile_fatturaordinaria_v1.2.1.xsl        ``849c4b50956b9e9eaccbbbffb04c1f345ff4abdc0dd191a14c54d48092c661984b1fcdb910c4c92291e158a62ecbb1c588d94e6bd6479e61ff6376746154df6c``  ``7e781d58f301055d3caa55aed2d1a8993185c60369004b418aec03a00ec2835a``
XML stylesheet for FatturaPA version 1.2.1              https://www.fatturapa.gov.it/export/documenti/fatturapa/v1.2.1/Foglio_di_stile_fatturaPA_v1.2.1.xsl               ``301db9da3c0715c0ab5db22c561bfb2812fea3cef150ff4a2124fe6141ebb3cb1c898d7ca3c931f716eff3b7b1946ebc86ca8bdd6d7561979f2f3a0cb95ff560``  ``ac278f980b84ae59a428544adf3eb52fc1685e381e441f5b8302cfffe902fc7d``
Public keys file                                        https://eidas.agid.gov.it/TL/TSL-IT.xml                                                                           ``96d2c7d04c8e7f84759a140a32d60471f5ce025831f87a69942433305355c54a2138200568db3df419583212d0d56df4895fbb4a704e6a7f5895118e3cc23ff4``  ``7b185145fc7ec28f6a01fa9f859e5029d2b02d676445f921d82582ba3c77babb``
======================================================  ================================================================================================================  ====================================================================================================================================  ====================================================================

.. warning:: fattura-elettronica-reader is guaranteed to work with these file versions only!

.. important:: The XML schema file for FatturaPA version 1.2.1 needs to be patched. fattura_elettronica_reader
                runs the SHA-512 checksum on the patched version of that file which corresponds to:

                ::


                    a1b02818f81ac91f35358260dd12e1bf4480e1545bb457caffa0d434200a1bd05bedd88df2d897969485a989dda78922850ebe978b92524778a37cb0afacba27


Some of these file are checked in the pipeline:
if the checksum does not match the ones present in the source code an exception is raised.
You can use the ``--ignore-assets-checksum`` option to override this behaviour.

Relevant Updates
----------------

October 2020
````````````

The original URL of the schema file dissapeared.

.. image:: assets/old_link.png
   :alt: Old link

A new URL points to the schema:

- https://www.fatturapa.gov.it/export/documenti/fatturapa/v1.2.1/Schema_del_file_xml_FatturaPA_versione_1.2.1a.xsd

This resource has been ``Last-Modified: Tue, 20 Oct 2020 19:29:21 GMT`` according to the HTTP headers.

.. image:: assets/page_information.png
   :alt: Page information

Same goes for the XML stylesheet files:

- FatturaPA: ``Last-Modified: Tue, 20 Oct 2020 18:00:14 GMT``
- Fattura Ordinaria: ``Last-Modified: Tue, 20 Oct 2020 18:08:05 GMT``

June 2019
`````````

According to the server the schema was last modified on
``Tue, 25 Jun 2019 10:16:31 GMT``, so they fixed an offending ``xsd`` typo:

- https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.2.1/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd

Before June 2019
````````````````

Initially the schema file was reported as incorrect by lxml because of a typo.
