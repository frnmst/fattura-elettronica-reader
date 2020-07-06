Developer Interface
===================

.. module:: fattura_elettronica_reader

Main Interface
--------------

Examples for the most relevant api functions can be viewed in the test
file. fattura_elettronica_reader's API uses `type hints`_ instead of assertions to check input and 
output types.

.. _type hints: https://docs.python.org/3/library/typing.html

.. autofunction:: is_xml_file_conforming_to_schema
.. autofunction:: parse_xml_file
.. autofunction:: get_invoice_filename
.. autofunction:: is_p7m_file_signed
.. autofunction:: invoice_file_checksum_matches
.. autofunction:: get_remote_file
.. autofunction:: get_ca_certificates
.. autofunction:: is_p7m_file_authentic
.. autofunction:: remove_signature_from_p7m_file
.. autofunction:: extract_attachments_from_invoice_file
.. autofunction:: get_invoice_as_html
.. autofunction:: patch_invoice_schema_file
.. autofunction:: create_appdirs
.. autofunction:: define_appdirs_user_data_dir_file_path
.. autofunction:: define_appdirs_user_config_dir_file_path
.. autofunction:: write_configuration_file
.. autofunction:: load_configuration
.. autofunction:: assert_data_structure
.. autofunction:: pipeline

Exceptions
----------

.. autoexception:: P7MFileDoesNotHaveACoherentCryptographicalSignature
.. autoexception:: InvoiceFileChecksumFailed
.. autoexception:: P7MFileNotAuthentic
.. autoexception:: CannotExtractOriginalP7MFile
.. autoexception:: MissingTagInMetadataFile
.. autoexception:: XMLFileNotConformingToSchema
.. autoexception:: ExtractedAttachmentNotInExtensionWhitelist
.. autoexception:: ExtractedAttachmentNotInFileTypeWhitelist
