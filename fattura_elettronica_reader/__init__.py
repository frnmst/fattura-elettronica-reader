#
# __init__.py
#
# Copyright (c) 2018 Enio Carboni - Italy
# Copyright (C) 2017-2019 Franco Masotti <franco.masotti@live.com>
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
"""Python discovery file."""

from .api import (
    is_xml_file_conforming_to_schema, parse_xml_file, get_invoice_filename,
    is_invoice_file_signed, invoice_file_checksum_matches, get_remote_file,
    get_ca_certificates, is_invoice_file_authentic, remove_signature_from_invoice_file,
    extract_attachments_from_invoice_file, get_invoice_as_html, patch_invoice_schema_file,
    create_appdirs, define_appdirs_user_data_dir_file_path, define_appdirs_user_config_dir_file_path,
    write_configuration_file, load_configuration, pipeline)
from .cli import (CliInterface)
from .exceptions import (InvoiceFileDoesNotHaveACoherentCryptographicalSignature,
                         InvoiceFileChecksumFailed, InvoiceFileNotAuthentic,
                         CannotExtractOriginalInvoiceFile, MissingTagInMetadataFile,
                         XMLFileNotConformingToSchema, ExtractedAttachmentNotInExtensionWhitelist,
                         ExtractedAttachmentNotInFileTypeWhitelist)
