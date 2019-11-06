#
# api.py
#
# Copyright (c) 2018 Enio Carboni - Italy
# Copyright (C) 2019 Franco Masotti <franco.masotti@live.com>
#
# This file is part of fattura-pa-reader.
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
"""The main file."""

import subprocess
import shlex
import lxml.etree as ET
import hashlib
import requests
import base64
import pathlib
import tempfile
import shutil
import atomicwrites
import filetype
import appdirs
import configparser
from .exceptions import (InvoiceFileDoesNotHaveACoherentCryptographicalSignature,
                         InvoiceFileChecksumFailed, InvoiceFileNotAuthentic,
                         CannotExtractOriginalInvoiceFile,
                         MissingTagInMetadataFile, XMLFileNotConformingToSchema,
                         ExtractedAttachmentNotInExtensionWhitelist,
                         ExtractedAttachmentNotInFileTypeWhitelist)
from .constants import (XML, Paths, Downloads, Patch, File)

#######
# API #
#######

def is_xml_file_conforming_to_schema(xml_file: str, xml_schema_file: str) -> bool:
    r"""Check that the XML file follows its schema.

    :param xml_file: the path of the XML file.
    :param xml_schema_file: the path of the schema file.
    :type xml_file: str
    :type xml_schema_file: str
    :returns: ``True`` if the schema is followed, ``False`` otherwise.
    :rtype: bool
    :raises: an lxml or a built-in exception.
    """
    xmlschema_doc = ET.parse(xml_schema_file)
    xmlschema = ET.XMLSchema(etree=xmlschema_doc)
    return xmlschema.validate(ET.parse(xml_file))

def parse_xml_file(xml_file: str):
    r"""Parse the XML file.

    :param xml_file: the input XML file.
    :type xml_file: str
    :returns: the XML root as a data structure
    :rtype: ET.parse.getroot
    :raises: an lxml or a built-in exception.
    """
    tree = ET.parse(xml_file)
    return tree.getroot()

def get_invoice_filename(metadata_file_xml_root,
                         metadata_file_invoice_filename_xml_tag: str,
                         metadata_file_xml_namespace: str) -> str:
    r"""Return the file name of the invoice file.

    :param metadata_file_xml_root: the root of the metadata XML tree.
    :param metadata_file_invoice_filename_xml_tag: the tag name corresponding
        to the invoice filename.
    :param metadata_file_xml_namespace: the XML namespace of the metadata file.
    :type metadata_file_xml_root: lxml.etree._Element
    :type metadata_file_invoice_filename_xml_tag: str
    :type metadata_file_xml_namespace: str
    :returns: the element or ``None``, if no match is found.
    :rtype: str
    :raises: an lxml or a built-in exception.
    """
    return metadata_file_xml_root.find(metadata_file_invoice_filename_xml_tag,
                                       metadata_file_xml_namespace).text


def is_invoice_file_signed(invoice_file: str) -> bool:
    r"""Check if the invoice file is signed with a PKCS#7 signature.

    :param invoice_file: the path of the invoice file.
    :type invoice_file: str
    :returns: True if the file is signed, False otherwise.
    :rtype: bool
    :raises: a subprocess or a built-in exception.
    """
    command = 'openssl pkcs7 -print_certs -text -noout -inform DER -in {}'.format(
        shlex.quote(invoice_file))
    return True if subprocess.run(
        shlex.split(command)).returncode == 0 else False


def invoice_file_checksum_matches(metadata_file_xml_root, invoice_file: str,
                                  metadata_file_invoice_checksum_xml_tag: str,
                                  metadata_file_xml_namespace: str) -> bool:
    r"""Check if the invoice checksum matches the one in the metadata file.

    :param metadata_file_xml_root: the root of the metadata XML tree.
    :param invoice_file: the path of the invoice file.
    :param metadata_file_invoice_checksum_xml_tag: the XML tag name
        corresponding to the invoice file checksum.
    :param metadata_file_xml_namespace: the XML namespace of the metadata file.
    :type metadata_file_xml_root: lxml.etree._Element
    :type invoice_file: str
    :type metadata_file_invoice_checksum_xml_tag: str
    :type metadata_file_xml_namespace: str
    :returns: ``True`` if the checksum matches, ``False`` otherwise.
        The expected checksum is also returned.
    :rtype: tuple
    :raises: a hashlib, lxml or a built-in exception.
    """
    # Get the checksum from the metadata file.
    expected_checksum = metadata_file_xml_root.find(
        metadata_file_invoice_checksum_xml_tag,
        metadata_file_xml_namespace).text
    # Compute the checksum.
    m = hashlib.sha256()
    m.update(open(invoice_file, 'rb').read())
    computed_checksum = m.hexdigest()

    if computed_checksum == expected_checksum:
        return True, expected_checksum
    else:
        return False, expected_checksum


def get_remote_file(destination: str, url: str):
    r"""Download and save a remote file.

    :param destination: the local path of the downloaded file.
    :param url: the remote path of the file.
    :type destination: str
    :type url: str
    :returns: None
    :rtype: None
    :raises: a built-in exception or a requests error.

    .. note: requests also checks that the url is in a valid form.
    """
    r = requests.get(url)
    if r.ok:
         with atomicwrites.atomic_write(destination, mode='wb', overwrite=True) as f:
            f.write(r.content)
    else:
        r.raise_for_status()

def get_ca_certificates(trusted_list_xml_root: str,
                        ca_certificate_pem_file: str,
                        trusted_list_file_xml_namespace: str,
                        trusted_list_file_xml_certificate_tag: str,
                        eol: str = '\n'):
    r"""Write the CA certificates file using the trusted list file.

    :param trusted_list_file: the input file.
    :param ca_certificate_pem_file: the destination file.
    :param trusted_list_file_xml_namespace: the XML namespace of the
        trusted list file.
    :param trusted_list_file_xml_certificate_tag: the XML tag name corresponding
        to the certificates in the trusted list file.
    :param eol: the end of line character to be used in the PEM file.
    :type trusted_list_xml_root: str
    :type ca_certificate_pem_file: str
    :type trusted_list_file_xml_namespace: str
    :type trusted_list_file_xml_certificate_tag: str
    :type eol: str
    :returns: None
    :rtype: None
    :raises: an atomicwrites, an lxml or a built-in exception.

    .. note: See https://tools.ietf.org/html/rfc7468
    """
    preeb = '-----BEGIN CERTIFICATE-----'
    posteb = '-----END CERTIFICATE-----'
    max_line_len = 64
    with atomicwrites.atomic_write(ca_certificate_pem_file, mode='w', overwrite=True) as f:
        # See https://lxml.de/tutorial.html#elementpath
        # for the exception that gets raised.
        for e in trusted_list_xml_root.iter(
                '{' + trusted_list_file_xml_namespace + '}' +
                trusted_list_file_xml_certificate_tag):
            # This tries to follow RFC7468 even in the variable naming.
            # See https://tools.ietf.org/html/rfc7468#section-3
            base64fullline = str()
            for i in range(0, len(e.text), max_line_len):
                _64base64char = e.text[i:i + max_line_len]
                base64fullline = base64fullline + _64base64char + eol
            strictbase64finl = str()
            strictbase64text = base64fullline + strictbase64finl
            stricttextualmsg = preeb + eol + strictbase64text + posteb + eol
            f.write(stricttextualmsg)


def is_invoice_file_authentic(invoice_file: str,
                              ca_certificate_pem_file: str,
                              ignore_signature_check: bool = False,
                              ignore_signers_certificate_check: bool = False):
    r"""Check authenticity of the invoice file on various levels.

    :param invoice_file: the path of the signed invoice file.
    :param ca_certificate_pem_file: the certificates file in PEM format.
    :param ignore_signature_check: avoid checking the signature.
        Defaults to ``False``.
    :param ignore_signers_certificate_check: avoid checking the signer's
        certificate. Defaults to ``False``.
    :type invoice_file: str
    :type ca_certificate_pem_file: str
    :type ignore_signature_check: bool
    :type ignore_signers_certificate_check: bool
    :returns: ``True`` if the operation is successful, ``False`` otherwise.
    :rtype: bool
    :raises: a subprocess or built-in exception.
    """
    pre = str()
    post = str()
    if ignore_signature_check:
        pre = '-nosigs'
    if ignore_signers_certificate_check:
        post = '-noverify'
    command = (
        'openssl smime ' + pre + ' -verify ' + post + ' -CAfile {}'.format(
            shlex.quote(ca_certificate_pem_file)) + ' -in {}'.format(
                shlex.quote(invoice_file)) + ' -inform DER -out /dev/null')
    return True if subprocess.run(
        shlex.split(command)).returncode == 0 else False


def remove_signature_from_invoice_file(invoice_file: str,
                                       output_file: str) -> bool:
    r"""Remove signature from the signed invoice file and save the original one.

    :param invoice_file: the path of the invoice file.
    :param output_file: the path of the destination file.
    :type invoice_file: str
    :type output_file: str
    :returns: ``True`` if the operation is successful, ``False`` otherwise.
    :rtype: bool
    :raises: a subprocess or built-in exception.
    """
    command = ('openssl smime -nosigs -verify -noverify -in {}'.format(
        shlex.quote(invoice_file)) + ' -inform DER -out {}'.format(
            shlex.quote(output_file)))
    return True if subprocess.run(
        shlex.split(command)).returncode == 0 else False


def extract_attachments_from_invoice_file(
        invoice_file_xml_root, invoice_file_xml_attachment_xpath: str,
        invoice_file_xml_attachment_tag: str,
        invoice_file_xml_attachment_filename_tag: str,
        invoice_file_text_encoding: str,
        ignore_attachment_extension_whitelist: bool = False,
        ignore_attachment_filetype_whitelist: bool = False,
        attachment_extension_whitelist: list = list(),
        attachment_filetype_whitelist: list = list()):
    r"""Extract, decode and save possible attachments within the invoice file.

    :param invoice_file_xml_root: the original invoice file.
    :param invoice_file_xml_attachment_xpath: the full path, from the XML root,
        corresponding to the attachments.
    :param invoice_file_xml_attachment_tag: the XML tag name corresponding to the
        attachment content.
    :param invoice_file_xml_attachment_filename_tag: the XML tag name
        corresponing to the attachment filename.
    :param invoice_file_text_encoding: the text encoding used for the
        invoice file.
    :param ignore_attachment_extension_whitelist: avoid cheking file extensions.
        Defaults to ``False``.
    :param ignore_attachment_filetype_whitelist: avoid cheking file types.
        Defaults to ``False``.
    :param attachment_extension_whitelist: . Defaults to ``list()``.
    :param attachment_filetype_whitelist: . Defaults to ``list()``.
    :type invoice_file_xml_root: str
    :type invoice_file_xml_attachment_xpath: str
    :type invoice_file_xml_attachment_tag: str
    :type invoice_file_xml_attachment_filename_tag: str
    :type invoice_file_text_encoding: str
    :type ignore_attachment_extension_whitelist: bool
    :type ignore_attachment_filetype_whitelist: bool
    :type attachment_extension_whitelist: list
    :type attachment_filetype_whitelist: list
    :returns: None
    :rtype: None
    :raises: base64.binascii.Error, filetype, atomicwrites, or a built-in exception.
    """
    for at in invoice_file_xml_root.findall(invoice_file_xml_attachment_xpath):
        attachment = at.find(invoice_file_xml_attachment_tag).text
        attachment_dest_path = at.find(
            invoice_file_xml_attachment_filename_tag).text

        if not ignore_attachment_extension_whitelist:
            if not attachment_dest_path.endswith(tuple(attachment_extension_whitelist)):
                raise ExtractedAttachmentNotInExtensionWhitelist

        # b64decode accepts any bytes-like object. There should not be any
        # character encoding problems since base64 characters are represented
        # using the same character ids on UTF-8 and ASCII.
        # Just in case that there are alien characters in the base64 string
        # (sic, it happened!) we use validate=False as an option to skip them.
        decoded = base64.b64decode(attachment.encode(invoice_file_text_encoding),validate=False)
        if not ignore_attachment_filetype_whitelist:
            # See https://h2non.github.io/filetype.py/1.0.0/filetype.m.html#filetype.filetype.get_type
            if filetype.guess(decoded).mime not in attachment_filetype_whitelist:
                raise ExtractedAttachmentNotInFileTypeWhitelist

        with atomicwrites.atomic_write(attachment_dest_path, mode='wb', overwrite=True) as f:
            f.write(decoded)


def get_invoice_as_html(
        invoice_file_xml_root, invoice_file_xml_stylesheet_root,
        html_output_file: str, invoice_file_text_encoding: str):
    r"""Transform the XML invoice file into a styled HTML file.

    :param invoice_file_xml_root: the XML tree root of the invoice file
    :param invoice_file_xml_stylesheet_root: the XML tree root of the stylesheet file
    :param html_output_file: the destination file.
    :param invoice_file_text_encoding: the text encoding used for the
        invoice file.
    :type invoice_file_xml_root: lxml.etree._Element
    :type invoice_file_xml_stylesheet_root: lxml.etree._Element
    :type html_output_file: str
    :type invoice_file_text_encoding: str
    :returns: None
    :rtype: None
    :raises: an lxml, atomicwrites, or a built-in exception.
    """
    transform = ET.XSLT(invoice_file_xml_stylesheet_root)
    newdom = transform(invoice_file_xml_root)
    with atomicwrites.atomic_write(html_output_file, mode='w', overwrite=True) as f:
        f.write(
            ET.tostring(newdom,
                        pretty_print=True).decode(invoice_file_text_encoding))


def patch_invoice_schema_file(invoice_schema_file: str, offending_line: str, fix_line: str):
    r"""Fix the error in the schema file.

    :param invoice_schema_file: the path of the schema file.
    :param offending_line: the string in the schema file that needs to be changed.
    :param fix_line: a string that replaces the offending line.
    :type invoice_schema_file: str
    :type offending_line: str
    :type fix_line: str
    :returns: None
    :rtype: None
    :raises: an atomicwrites, or a built-in exception.

    .. note: this cannot be patched with lxml because and exception is raised:
             lxml.etree.XMLSyntaxError: Namespace prefix xsd on import is not defined, line 7, column 154

    .. note: this sucks. A better solution needs to be found.
    """
    save = list()
    with open(invoice_schema_file, 'r') as f:
        for line in f:
            if line == offending_line:
                save.append(fix_line)
            else:
                save.append(line)
    with atomicwrites.atomic_write(invoice_schema_file, mode='w', overwrite=True) as f:
        for s in save:
            f.write(s)

##############################
# Pipeline related functions #
##############################

def create_appdirs(program_name: str):
    r"""Create user data and configuration directories.

    :param program_name: the name of the software.
    :type program_name: str
    :raises: a pathlib or a built-in exception.
    :returns: None
    :rtype: None

    .. note: for security reasons the directories have restrictive perimissions.
    """
    pathlib.Path(appdirs.user_data_dir(program_name)).mkdir(mode=0o700,parents=True,exist_ok=True)
    pathlib.Path(appdirs.user_config_dir(program_name)).mkdir(mode=0o700,parents=True,exist_ok=True)

def define_appdirs_user_data_dir_file_path(program_name: str, relative_path: str):
    r"""Get the full path of the input file in the users's data directory.

    :param program_name: the name of the software.
    :param relative_path: the relative path of the file, i.e: the file name.
    :type program_name: str
    :type relative_path: str
    :returns: a full path.
    :rtype: str
    """
    return str(pathlib.Path(appdirs.user_data_dir(program_name), relative_path))

def define_appdirs_user_config_dir_file_path(program_name: str, relative_path: str):
    r"""Get the full path of the input file in the user's cofiguration directory.

    :param program_name: the name of the software.
    :param relative_path: the relative path of the file, i.e: the file name.
    :type program_name: str
    :type relative_path: str
    :returns: a path.
    :rtype: str
    """
    return str(pathlib.Path(appdirs.user_config_dir(program_name), relative_path))

def write_configuration_file(configuration_file: str):
    r"""Write the default configuration file.

    :param configuration_file: the path of the configuration file.
    :type configuration_file: str
    :returns: None
    :rtype: None
    :raises: a configparser or a built-in exception.
    """
    config = configparser.ConfigParser()
    config.optionxform = str
    config['metadata file'] = {
        'XML namespace': XML['metadata file']['namespaces']['default'],
        'XML invoice checksum tag': XML['metadata file']['tags']['invoice checksum'],
        'XML invoice filename tag': XML['metadata file']['tags']['invoice filename'],
        'XML system id tag': XML['metadata file']['tags']['system id']
    }
    config['trusted list file'] = {
        'XML namespace': XML['trusted list file']['namespaces']['default'],
        'XML certificate tag': XML['trusted list file']['tags']['certificate'],
        'download': Downloads['trusted list file']['default'],
    }
    config['invoice file'] = {
        'XML namespace': XML['invoice file']['namespaces']['default'],
        'XML attachment tag': XML['invoice file']['tags']['attachment'],
        'XML attachment filename tag': XML['invoice file']['tags']['attachment filename'],
        'XML attachment XPath': XML['invoice file']['XPath']['attachment'],
        'text encoding': XML['invoice file']['proprieties']['text encoding'],
        'XSD download': Downloads['invoice file']['XSD']['default'],
        'W3C XSD download': Downloads['invoice file']['XSD']['W3C Schema for XML Signatures'],
        'XSLT ordinaria download': Downloads['invoice file']['XSLT']['ordinaria'],
        'XSLT PA download': Downloads['invoice file']['XSLT']['PA'],
        'attachment extension whitelist': File['invoice']['attachment']['extension whitelist'],
        'attachment filetype whitelist': File['invoice']['attachment']['filetype whitelist']
    }

    with open(configuration_file, 'w') as configfile:
        config.write(configfile)

def load_configuration(configuration_file: str):
    r"""Attempt to load the configuration file.

    :param configuration_file: the path of the configuration file.
    :type configuration_file: str
    :returns: the configuration.
    :rtype: dict
    :raises: a configparser or a built-in exception.

    .. note: errors are not raised if the configuration file does not exist.
    """
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(configuration_file)

    configuration = dict()
    configuration['metadata file']=dict()
    configuration['trusted list file']=dict()
    configuration['invoice file']=dict()

    configuration['metadata file']['XML namespace'] = config.get('metadata file', 'XML namespace', fallback=XML['metadata file']['namespaces']['default'])
    configuration['metadata file']['XML invoice checksum tag'] = config.get('metadata file', 'XML invoice checksum tag', fallback=XML['metadata file']['tags']['invoice checksum'])
    configuration['metadata file']['XML invoice filename tag'] = config.get('metadata file', 'invoice filename tag', fallback=XML['metadata file']['tags']['invoice filename'])
    configuration['metadata file']['XML system id tag'] = config.get('metadata file', 'XML system id tag', fallback=XML['metadata file']['tags']['system id'])

    configuration['trusted list file']['XML namespace'] = config.get('trusted list file', 'XML namespace', fallback=XML['trusted list file']['namespaces']['default'])
    configuration['trusted list file']['XML certificate tag'] = config.get('trusted list file', 'XML certificate tag', fallback=XML['trusted list file']['tags']['certificate'])
    configuration['trusted list file']['download'] = config.get('trusted list file', 'download', fallback=Downloads['trusted list file']['default'])

    configuration['invoice file']['XML namespace'] = config.get('invoice file', 'XML namespace', fallback=XML['invoice file']['namespaces']['default'])
    configuration['invoice file']['XML attachment tag'] = config.get('invoice file', 'XML attachment tag', fallback=XML['invoice file']['tags']['attachment'])
    configuration['invoice file']['XML attachment filename tag'] = config.get('invoice file', 'XML attachment filename tag', fallback=XML['invoice file']['tags']['attachment filename'])
    configuration['invoice file']['XML attachment XPath'] = config.get('invoice file', 'XML attachment XPath', fallback=XML['invoice file']['XPath']['attachment'])
    configuration['invoice file']['text encoding'] = config.get('invoice file', 'text encoding', fallback=XML['invoice file']['proprieties']['text encoding'])
    configuration['invoice file']['XSD download'] = config.get('invoice file', 'XSD download', fallback=Downloads['invoice file']['XSD']['default'])
    configuration['invoice file']['W3C XSD download'] = config.get('invoice file', 'W3C XSD download', fallback=Downloads['invoice file']['XSD']['W3C Schema for XML Signatures'])
    configuration['invoice file']['XSLT ordinaria download'] = config.get('invoice file', 'XSLT ordinaria download', fallback=Downloads['invoice file']['XSLT']['ordinaria'])
    configuration['invoice file']['XSLT PA download'] = config.get('invoice file', 'XSLT PA download', fallback=Downloads['invoice file']['XSLT']['PA'])
    configuration['invoice file']['attachment extension whitelist'] = config.get('invoice file', 'attachment extension whitelist', fallback=File['invoice']['attachment']['extension whitelist'])
    configuration['invoice file']['attachment filetype whitelist'] = config.get('invoice file', 'attachment filetype whitelist', fallback=File['invoice']['attachment']['filetype whitelist'])

    return configuration

def pipeline(metadata_file: str,
             configuration_file: str = None,
             invoice_filename: str = None,
             ignore_signature_check: bool = False,
             ignore_signers_certificate_check: bool = False,
             no_checksum_check: bool = False,
             extract_attachments: bool = False,
             generate_html_output: bool = False,
             keep_original_invoice: bool = False,
             force_trusted_list_file_download: bool = False,
             force_invoice_xml_stylesheet_file_download: bool = False,
             force_invoice_schema_file_download: bool = False,
             no_invoice_xml_validation: bool = False,
             invoice_xslt_type: str = 'ordinaria',
             ignore_attachment_extension_whitelist: bool = False,
             ignore_attachment_filetype_whitelist: bool = False,
             write_default_configuration_file: bool = False,
             invoice_file_is_not_p7m: bool = False):
    r"""Run the pipeline."""
    project_name = 'fattura_elettronica_reader'
    create_appdirs(project_name)
    if configuration_file is None:
        configuration_file = define_appdirs_user_config_dir_file_path(project_name, Paths['configuration file'])
    if write_default_configuration_file:
        write_configuration_file(configuration_file)

    config = load_configuration(configuration_file)

    # Define all the paths for the static elements.
    trusted_list_file = define_appdirs_user_data_dir_file_path(project_name, Paths['trusted list file'])
    ca_certificate_pem_file = define_appdirs_user_data_dir_file_path(project_name, Paths['CA certificate pem file'])
    invoice_schema_file = define_appdirs_user_data_dir_file_path(project_name,Paths['invoice file']['XSD']['default'])
    w3c_schema_file_for_xml_signatures = define_appdirs_user_data_dir_file_path(project_name,Paths['invoice file']['XSD']['W3C Schema for XML Signatures'])
    invoice_xslt_ordinaria_file =  define_appdirs_user_data_dir_file_path(project_name, Paths['invoice file']['XSLT']['ordinaria'])
    invoice_xslt_PA_file =  define_appdirs_user_data_dir_file_path(project_name, Paths['invoice file']['XSLT']['PA'])
    if invoice_xslt_type == 'ordinaria':
        invoice_xslt_file = invoice_xslt_ordinaria_file
    elif invoice_xslt_type == 'PA':
        invoice_xslt_file = invoice_xslt_PA_file
    else:
        invoice_xslt_file = invoice_xslt_ordinaria_file

    # See also:
    # https://www.fatturapa.gov.it/export/fatturazione/sdi/messaggi/v1.0/MT_v1.0.xsl
    metadata_root = parse_xml_file(metadata_file)
    if invoice_filename is None:
        invoice_filename = get_invoice_filename(
            metadata_root, config['metadata file']['XML invoice filename tag'],
            dict(default = config['metadata file']['XML namespace']))
        if invoice_filename is None:
            raise MissingTagInMetadataFile

    if not no_checksum_check:
        checksum_matches, checksum = invoice_file_checksum_matches(
            metadata_root, invoice_filename,
            config['metadata file']['XML invoice checksum tag'],
            dict(default = config['metadata file']['XML namespace']))
        if checksum is None:
            raise MissingTagInMetadataFile
        if not checksum_matches:
            raise InvoiceFileChecksumFailed

    # Apparently, invoices must be signed for 'PA' and not necessarly for
    # 'B2B' and other cases. I could not find official documentation
    # corroborating this but it happened at least one.
    if not invoice_file_is_not_p7m:
        if not is_invoice_file_signed(invoice_filename):
            raise InvoiceFileDoesNotHaveACoherentCryptographicalSignature

    if force_trusted_list_file_download or not pathlib.Path(
            trusted_list_file).exists():
        get_remote_file(trusted_list_file,
                              config['trusted list file']['download'])

    trusted_list_xml_root = parse_xml_file(trusted_list_file)

    get_ca_certificates(trusted_list_xml_root, ca_certificate_pem_file,
                        config['trusted list file']['XML namespace'],
                        config['trusted list file']['XML certificate tag'])

    if not invoice_file_is_not_p7m:
        if not is_invoice_file_authentic(invoice_filename, ca_certificate_pem_file,
                                         ignore_signature_check,
                                         ignore_signers_certificate_check):
            raise InvoiceFileNotAuthentic

    if not no_invoice_xml_validation:

        # This W3C file should not change any time soon so we can avoid the force download option.
        if not pathlib.Path(w3c_schema_file_for_xml_signatures).exists():
            get_remote_file(w3c_schema_file_for_xml_signatures,config['invoice file']['W3C XSD download'])

        if force_invoice_schema_file_download or not pathlib.Path(invoice_schema_file).exists():
            get_remote_file(
                    invoice_schema_file, config['invoice file']['XSD download'])

        patch_invoice_schema_file(invoice_schema_file, Patch['invoice file']['XSD']['line'][0]['offending'],Patch['invoice file']['XSD']['line'][0]['fix'])

    # Create a temporary directory to store the original XML invoice file.
    with tempfile.TemporaryDirectory() as tmpdirname:
        # invoice_original_file is the path of the non-signed invoice file. If an invoice file is signed,
        # the filename usually ends in '.p7m' so the destination file must end with '.xml'
        # to be transformed into an xml file. On the contrary, the filename of non-signed invoice files
        # already ends in '.xml'.
        if invoice_file_is_not_p7m:
            invoice_original_file = invoice_filename
        else:
            invoice_original_file = invoice_filename + '.xml'

        # In case absolute paths are passed to this function the concatenation of an absolute path
        # and a temporary directory name, which is also an absolue path, would not work as expected.
        invoice_original_file_relative = pathlib.Path(invoice_original_file).name

        if invoice_file_is_not_p7m:
            # There is no signature to extract but we need to copy the file in the temporary store.
            shutil.copyfile(invoice_original_file, str(pathlib.Path(tmpdirname, invoice_original_file_relative)))
        else:
            # Extract the original invoice and copy it in the temporary store.
            if not remove_signature_from_invoice_file(invoice_filename,
                                                      str(pathlib.Path(tmpdirname, invoice_original_file_relative))):
                raise CannotExtractOriginalInvoiceFile

        if not no_invoice_xml_validation:
            if not is_xml_file_conforming_to_schema(str(pathlib.Path(tmpdirname, invoice_original_file_relative)), invoice_schema_file):
                raise XMLFileNotConformingToSchema

        invoice_root = parse_xml_file(str(pathlib.Path(tmpdirname, invoice_original_file_relative)))

        if extract_attachments:
            extract_attachments_from_invoice_file(
                invoice_root, config['invoice file']['XML attachment XPath'],
                config['invoice file']['XML attachment tag'],
                config['invoice file']['XML attachment filename tag'],
                config['invoice file']['text encoding'],
                ignore_attachment_extension_whitelist,
                ignore_attachment_filetype_whitelist,
                config['invoice file']['attachment extension whitelist'],
                config['invoice file']['attachment filetype whitelist'])

        if generate_html_output:

            if force_invoice_xml_stylesheet_file_download or not pathlib.Path(
                invoice_xslt_file).exists():
                get_remote_file(
                    invoice_xslt_file, config['invoice file']['XSLT ' + invoice_xslt_type + ' download'])

            invoice_xslt_root = parse_xml_file(invoice_xslt_file)

            html_output = invoice_filename + '.html'

            get_invoice_as_html(invoice_root, invoice_xslt_root, html_output,
                                config['invoice file']['text encoding'])

        if keep_original_invoice:
            shutil.move(str(pathlib.Path(tmpdirname, invoice_original_file_relative)),  invoice_original_file)


if __name__ == '__main__':
    pass
