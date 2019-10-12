#
# cli.py
#
# Copyright (c) 2018 Enio Carboni - Italy
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
"""Command line interface file."""

import argparse
import textwrap
from pkg_resources import (get_distribution, DistributionNotFound)
from .api import pipeline
from .constants import File

PROGRAM_DESCRIPTION = 'fattura-elettronica-reader: Validate, extract, and generate printables\nof electronic invoice files received from the "Sistema di Interscambio"'
VERSION_NAME = 'fattura_elettronica_reader'
try:
    VERSION_NUMBER = str(get_distribution('fattura_elettronica_reader').version)
except DistributionNotFound:
    VERSION_NUMBER = 'vDevel'
VERSION_COPYRIGHT = 'Copyright (C) 2019 Franco Masotti, frnmst'
VERSION_LICENSE = 'License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>\nThis is free software: you are free to change and redistribute it.\nThere is NO WARRANTY, to the extent permitted by law.'
RETURN_VALUES = 'Return values: 0 ok, 1 error, 2 invalid command'
PROGRAM_EPILOG = RETURN_VALUES + '\n\n' + VERSION_COPYRIGHT + '\n' + VERSION_LICENSE


class CliToApi():
    """An interface between the CLI and API functions."""

    def run(self, args):
        """Run the pipeline."""
        if args.keep_all:
            args.extract_attachments = True
            args.generate_html_output = True
            args.keep_original_invoice = True
        for metadata_file in args.metadata_file:
            pipeline(
                metadata_file=metadata_file,
                configuration_file=args.configuration_file,
                invoice_filename=args.invoice_filename,
                ignore_signature_check=args.ignore_signature_check,
                ignore_signers_certificate_check=args.ignore_signers_certificate_check,
                no_checksum_check=args.no_checksum_check,
                extract_attachments=args.extract_attachments,
                generate_html_output=args.generate_html_output,
                keep_original_invoice = args.keep_original_invoice,
                force_trusted_list_file_download=args.force_trusted_list_file_download,
                force_invoice_xml_stylesheet_file_download=args.force_invoice_xml_stylesheet_file_download,
                force_invoice_schema_file_download=args.force_invoice_schema_file_download,
                no_invoice_xml_validation=args.no_invoice_xml_validation,
                invoice_xslt_type=args.invoice_xslt_type,
                ignore_attachment_extension_whitelist=args.ignore_attachment_extension_whitelist,
                ignore_attachment_filetype_whitelist=args.ignore_attachment_filetype_whitelist,
                write_default_configuration_file=args.write_default_configuration_file,
                invoice_file_is_not_p7m=args.invoice_file_is_not_p7m)


class CliInterface():
    """The interface exposed to the final user."""

    def __init__(self):
        """Set the parser variable that will be used instead of using create_parser."""
        self.parser = self.create_parser()

    def create_parser(self):
        """Create the CLI parser."""
        parser = argparse.ArgumentParser(
            description=PROGRAM_DESCRIPTION,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(PROGRAM_EPILOG))

        parser.add_argument(
            'metadata_file',
            nargs='+',
            help='the metadata file names')

        parser.add_argument(
            '-c',
            '--configuration-file',
            help='the path of the configuration file')

        parser.add_argument(
            '-C',
            '--write-default-configuration-file',
            action='store_true',
            help='write the default configuration file')

        parser.add_argument(
            '-i',
            '--invoice-filename',
            help='defaults to the one specified in the metadata file')

        parser.add_argument(
            '-A',
            '--keep-all',
            action='store_true',
            help='keep all extracted and generated files. This is the same as "-Hao"')

        parser.add_argument(
            '-H',
            '--generate-html-output',
            action='store_true',
            help='generate the HTML output of the invoice file')

        parser.add_argument(
            '-a',
            '--extract-attachments',
            action='store_true',
            help='extract embedded attachments')

        parser.add_argument(
            '-o',
            '--keep-original-invoice',
            action='store_true',
            help='keep the original invoice XML file')

        parser.add_argument(
            '-X',
            '--invoice-xslt-type',
            choices=['ordinaria','PA'],
            default='ordinaria',
            help='select the XML stylesheet file for the invoice. Defaults to "ordinaria". This option is ignored if "-H" is not set')

        parser.add_argument(
            '-V',
            '--no-invoice-xml-validation',
            action='store_true',
            help='do not perform XML validation of the invoice file')

        parser.add_argument(
            '-E',
            '--force-invoice-schema-file-download',
            action='store_true',
            help='force download of the XML schema necessary for the validation of the invoice file')

        parser.add_argument(
            '-b',
            '--invoice-file-is-not-p7m',
            default=False,
            action='store_true',
            help='avoids running any type of cryptographical signature and certificate checks. This is useful for certain B2B invoice files.')

        parser.add_argument(
            '-s',
            '--ignore-signature-check',
            default=False,
            action='store_true',
            help='avoids checking the cryptographic signature of the invoice file')

        parser.add_argument(
            '-S',
            '--ignore-signers-certificate-check',
            action='store_true',
            help='avoids checking the cryptographic certificate')

        parser.add_argument(
            '-k',
            '--no-checksum-check',
            action='store_true',
            help='do not perform a file integrity check of the invoice file')

        parser.add_argument(
            '-t',
            '--force-trusted-list-file-download',
            action='store_true',
            help='force download of the trusted list file')

        parser.add_argument(
            '-y',
            '--force-invoice-xml-stylesheet-file-download',
            action='store_true',
            help='force download of the XML stylesheet file')

        parser.add_argument(
            '-w',
            '--ignore-attachment-extension-whitelist',
            action='store_true',
            help='do not perform file extension checks for the attachments. This option is ignored if "-a" is not set')

        parser.add_argument(
            '-W',
            '--ignore-attachment-filetype-whitelist',
            action='store_true',
            help='do not perform filetype checks for the attachments. This option is ignored if "-a" is not set')

        parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=VERSION_NAME + ' ' + VERSION_NUMBER)

        parser.set_defaults(func=CliToApi().run)

        return parser
