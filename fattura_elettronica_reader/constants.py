#
# constants.py
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
"""A file that contains all the global constants."""

from pathlib import Path

common_defaults = dict()
common_defaults = {'home directory': Path.home()}

XML = dict()
XML['metadata file'] = dict()
XML['trusted list file'] = dict()
XML['invoice file'] = dict()

XML['metadata file']['namespaces'] = {
    'default':
    'http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fattura/messaggi/v1.0'
}

XML['metadata file']['tags'] = {
    'invoice checksum': 'Hash',
    'invoice filename': 'NomeFile',
    'system id': 'IdentificativoSdI'
}

XML['trusted list file']['namespaces'] = {
    'default': 'http://uri.etsi.org/02231/v2#'
}

XML['trusted list file']['tags'] = {'certificate': 'X509Certificate'}

XML['invoice file']['namespaces'] = {
    'default': 'http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2'
}

XML['invoice file']['tags'] = {
    'attachment': 'Attachment',
    'attachment filename': 'NomeAttachment'
}

XML['invoice file']['XPath'] = {
    'attachment': './FatturaElettronicaBody/Allegati'
}

# See:
# https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.2.1/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd
XML['invoice file']['proprieties'] = {'text encoding': 'UTF-8'}

# Download urls.
Downloads = dict()

Downloads['invoice file']=dict()
Downloads['invoice file']['XSLT'] = {
    # Pubblica Amministrazione.
    'PA':
    'https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.2.1/fatturaPA_v1.2.1.xsl',
    'ordinaria':
    'https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.2.1/fatturaordinaria_v1.2.1.xsl'
}
Downloads['invoice file']['XSD'] = {
    'default': 'https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.2.1/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd',
    'W3C Schema for XML Signatures': 'https://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd'
}

Downloads['trusted list file'] = {
    'default': 'https://eidas.agid.gov.it/TL/TSL-IT.xml'
}

# File Patches.
Patch=dict()
Patch['invoice file']=dict()
Patch['invoice file']['XSD']=dict()
Patch['invoice file']['XSD']['line']=dict()
Patch['invoice file']['XSD']['line'][0] = {
    'offending': 2 * ' ' + '<xs:import namespace="http://www.w3.org/2000/09/xmldsig#" schemaLocation="http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd"/>\n',
    'fix': 2 * ' ' + '<xs:import namespace="http://www.w3.org/2000/09/xmldsig#" schemaLocation="xmldsig-core-schema.xsd"/>\n'
}

# Relative paths.
Paths = dict()
Paths['trusted list file'] = 'trusted_list.xml'
Paths['CA certificate pem file'] = 'CA.pem'
Paths['invoice file']=dict()
# Invoice stylesheet files.
Paths['invoice file']['XSLT'] = {
    'PA': 'invoice_stylesheet_PA.xslt',
    'ordinaria': 'invoice_stylesheet_ordinaria.xslt'
}
# Invoice schema files.
Paths['invoice file']['XSD'] = {
    'default': 'invoice_schema.xsd',
    'W3C Schema for XML Signatures': 'xmldsig-core-schema.xsd'
}
Paths['configuration file'] = 'fattura_elettronica_reader.conf'

# Stuff related generically to files.
File=dict()
File['invoice'] = dict()
File['invoice']['attachment'] = {
    'extension whitelist': ['PDF', 'pdf'],
    # Uses mimes.
    'filetype whitelist': ['application/pdf']
}

if __name__ == '__main__':
    pass
