#
# cli.py
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
"""Command line interface file."""

import argparse
import textwrap
import sys
from pkg_resources import (get_distribution, DistributionNotFound)
from .api import pipeline

PROGRAM_DESCRIPTION = 'fattura-elettronica-reader: Validate, extract, and generate printables\nof electronic invoice files received from the "Sistema di Interscambio"\nas well as other P7M files'
VERSION_NAME = 'fattura_elettronica_reader'
try:
    VERSION_NUMBER = str(
        get_distribution('fattura_elettronica_reader').version)
except DistributionNotFound:
    VERSION_NUMBER = 'vDevel'
VERSION_COPYRIGHT = 'Copyright (C) 2019 Franco Masotti, frnmst'
VERSION_LICENSE = 'License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>\nThis is free software: you are free to change and redistribute it.\nThere is NO WARRANTY, to the extent permitted by law.'
RETURN_VALUES = 'Return values: 0 ok, 1 error, 2 invalid command'
PROGRAM_EPILOG = RETURN_VALUES + '\n\n' + VERSION_COPYRIGHT + '\n' + VERSION_LICENSE


class CliToApi():
    r"""An interface between the CLI and API functions."""

    def run(self, args):
        r"""Run the pipeline."""
        common_data = {
            'patched':
            False,
            'configuration file':
            args.configuration_file,
            'write default configuration file':
            args.write_default_configuration_file,
            'ignore assets checksum':
            args.ignore_assets_checksum,
        }

        # Prepare the data structure.
        if args.source == 'invoice':
            data = {
                'extract attachments':
                args.extract_attachments,
                'metadata files':
                args.metadata_file,
                'invoice xslt type':
                args.invoice_xslt_type,
                'no invoice xml validation':
                args.no_invoice_xml_validation,
                'force invoice schema file download':
                args.force_invoice_schema_file_download,
                'generate html output':
                args.generate_html_output,
                'invoice filename':
                args.invoice_filename,
                'no checksum check':
                args.no_checksum_check,
                'force invoice xml stylesheet file download':
                args.force_invoice_xml_stylesheet_file_download,
                'ignore attachment extension whitelist':
                args.ignore_attachment_extension_whitelist,
                'ignore attachment filetype whitelist':
                args.ignore_attachment_filetype_whitelist,
            }
            if args.file_type == 'p7m':
                data['ignore signature check'] = args.ignore_signature_check
                data[
                    'ignore signers certificate check'] = args.ignore_signers_certificate_check
                data[
                    'force trusted list file download'] = args.force_trusted_list_file_download
                data['keep original file'] = args.keep_original_file
            elif args.file_type == 'plain':
                pass
        elif args.source == 'generic':
            if args.file_type == 'p7m':
                data = {
                    'p7m files': args.p7m_file,
                    'ignore signature check': args.ignore_signature_check,
                    'ignore signers certificate check':
                    args.ignore_signers_certificate_check,
                    'force trusted list file download':
                    args.force_trusted_list_file_download,
                    'keep original file': args.keep_original_file,
                }
        else:
            data = {'write default configuration file': True}

        # Merge the dicts.
        data = {**common_data, **data}

        if args.source == 'invoice':
            iterator = data['metadata files']
        elif args.source == 'generic':
            iterator = data['p7m files']
        else:
            # Write the config file and quit.
            iterator = ['config file']

        for i in iterator:
            # Patch data with single files.
            data['patched'] = True
            if args.source == 'invoice':
                data['metadata file'] = i
                source = args.source
                file_type = args.file_type
            elif args.source == 'generic':
                data['p7m file'] = i
                source = args.source
                file_type = args.file_type
            else:
                source = 'NOOP'
                file_type = 'NOOP'
            pipeline(source, file_type, data)


class CliInterface():
    r"""The interface exposed to the final user."""

    def __init__(self):
        r"""Set the parser variable that will be used instead of using create_parser."""
        self.parser = self.create_parser()

    def create_parser(self):
        r"""Create the CLI parser."""
        parser = argparse.ArgumentParser(
            description=PROGRAM_DESCRIPTION,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(PROGRAM_EPILOG))

        source_required = '--write-default-configuration-file' not in sys.argv and '-C' not in sys.argv
        source_subparsers = parser.add_subparsers(title='source',
                                                  dest='source',
                                                  required=source_required)

        ###########
        # Sources #
        ###########
        invoice_parser = source_subparsers.add_parser('invoice',
                                                      help='invoice file')
        generic_parser = source_subparsers.add_parser('generic',
                                                      help='generic file')

        invoice_xslt_type_help = 'select the XML stylesheet file for the invoice. Defaults to "ordinaria". This option is ignored if "-H" is not set'
        invoice_parser.add_argument(
            '-X',
            '--invoice-xslt-type',
            choices=['ordinaria', 'PA'],
            default='ordinaria',
            help=invoice_xslt_type_help,
        )

        invoice_parser.add_argument(
            '-V',
            '--no-invoice-xml-validation',
            action='store_true',
            help='do not perform XML validation of the invoice file')

        invoice_parser.add_argument('-a',
                                    '--extract-attachments',
                                    action='store_true',
                                    help='extract embedded attachments')

        force_invoice_schema_file_download_help = 'force download of the XML schema necessary for the validation of the invoice file'
        invoice_parser.add_argument(
            '-E',
            '--force-invoice-schema-file-download',
            action='store_true',
            help=force_invoice_schema_file_download_help,
        )

        invoice_parser.add_argument('-H',
                                    '--generate-html-output',
                                    action='store_true',
                                    help='generate the HTML output')

        invoice_parser.add_argument(
            '-i',
            '--invoice-filename',
            default=str(),
            help='override the invoice file name specified in the metadata file'
        )

        invoice_parser.add_argument(
            '-k',
            '--no-checksum-check',
            action='store_true',
            help='do not perform a file integrity check of the invoice file')

        invoice_parser.add_argument(
            '-y',
            '--force-invoice-xml-stylesheet-file-download',
            action='store_true',
            help='force download of the XML stylesheet file')

        ignore_attachment_extension_whitelist_help = 'do not perform file extension checks for the attachments. This option is ignored if "-a" is not set'
        invoice_parser.add_argument(
            '-w',
            '--ignore-attachment-extension-whitelist',
            action='store_true',
            help=ignore_attachment_extension_whitelist_help,
        )

        ignore_attachment_filetype_whitelist_help = 'do not perform filetype checks for the attachments. This option is ignored if "-a" is not set'
        invoice_parser.add_argument(
            '-W',
            '--ignore-attachment-filetype-whitelist',
            action='store_true',
            help=ignore_attachment_filetype_whitelist_help,
        )

        ###########
        # Invoice #
        ###########
        invoice_subparsers = invoice_parser.add_subparsers(title='file type',
                                                           dest='file_type',
                                                           required=True)

        invoice_p7m_parser = invoice_subparsers.add_parser('p7m', help='p7m')

        ignore_signature_check_help = 'avoids checking the cryptographic signature of the invoice file'
        invoice_p7m_parser.add_argument(
            '-s',
            '--ignore-signature-check',
            default=False,
            action='store_true',
            help=ignore_signature_check_help,
        )

        invoice_p7m_parser.add_argument(
            '-S',
            '--ignore-signers-certificate-check',
            action='store_true',
            help='avoids checking the cryptographic certificate')

        invoice_p7m_parser.add_argument(
            '-t',
            '--force-trusted-list-file-download',
            action='store_true',
            help='force download of the trusted list file')

        invoice_p7m_parser.add_argument('-o',
                                        '--keep-original-file',
                                        action='store_true',
                                        help='keep the original file')

        invoice_p7m_parser.add_argument('metadata_file',
                                        nargs='+',
                                        help='the metadata file names')

        invoice_plain_parser = invoice_subparsers.add_parser('plain',
                                                             help='plain')

        invoice_plain_parser.add_argument('metadata_file',
                                          nargs='+',
                                          help='the metadata file names')

        ###########
        # Generic #
        ###########
        generic_subparsers = generic_parser.add_subparsers(title='file type',
                                                           dest='file_type',
                                                           required=True)

        generic_p7m_parser = generic_subparsers.add_parser('p7m', help='p7m')

        generic_p7m_parser.add_argument(
            '-s',
            '--ignore-signature-check',
            default=False,
            action='store_true',
            help='avoids checking the cryptographic signature of the p7m file')

        generic_p7m_parser.add_argument(
            '-S',
            '--ignore-signers-certificate-check',
            action='store_true',
            help='avoids checking the cryptographic certificate')

        generic_p7m_parser.add_argument(
            '-t',
            '--force-trusted-list-file-download',
            action='store_true',
            help='force download of the trusted list file')

        generic_p7m_parser.add_argument('-o',
                                        '--keep-original-file',
                                        action='store_true',
                                        help='keep the original file')

        generic_p7m_parser.add_argument('p7m_file',
                                        nargs='+',
                                        help='the p7m file names')

        ###########
        # Common  #
        ###########
        parser.add_argument('-c',
                            '--configuration-file',
                            default=str(),
                            help='the path of the configuration file')

        parser.add_argument('-C',
                            '--write-default-configuration-file',
                            action='store_true',
                            help='write the default configuration file')

        parser.add_argument('-k',
                            '--ignore-assets-checksum',
                            action='store_true',
                            help='avoid running checksums for the downloadable assets')

        parser.add_argument('-v',
                            '--version',
                            action='version',
                            version=VERSION_NAME + ' ' + VERSION_NUMBER)

        parser.set_defaults(func=CliToApi().run)

        return parser
