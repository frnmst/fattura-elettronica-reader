#
# exceptions.py
#
# Copyright (c) 2018 Enio Carboni - Italy
# Copyright (C) 2019-2020 Franco Masotti <franco.masotti@live.com>
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
"""Exceptions file."""


class P7MFileDoesNotHaveACoherentCryptographicalSignature(Exception):
    """Not a PKCS#7 signature."""


class InvoiceFileChecksumFailed(Exception):
    """Checksum of the invoice file does not match the one in the metadata file."""


class P7MFileNotAuthentic(Exception):
    """An error with the signature or the signers certificate of the invoice."""


class CannotExtractOriginalP7MFile(Exception):
    """The cryptographical signature from the invoice file cannot be removed."""


class MissingTagInMetadataFile(Exception):
    """A necessary element is missing from the metadata file."""


class XMLFileNotConformingToSchema(Exception):
    """XML file is not-conforming to the XML schema."""


class ExtractedAttachmentNotInExtensionWhitelist(Exception):
    """An extracted attachment is not in the extension whitelist."""


class ExtractedAttachmentNotInFileTypeWhitelist(Exception):
    """An extracted attachment is not in the filetype whitelist."""


class AssetsChecksumDoesNotMatch(Exception):
    """A downloaded file might make this program malfuncioning."""
