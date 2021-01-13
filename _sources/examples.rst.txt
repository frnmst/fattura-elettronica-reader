Examples
========

CLI
---

Invoices
````````

You want everything, you trust nothing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


::


    $ fattura_elettronica_reader invoice --extract-attachments --generate-html-output p7m --keep-original-file ${metadata_file}


You want everything, you trust everything
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


::


    $ fattura_elettronica_reader --ignore-assets-checksum invoice --extract-attachments --generate-html-output p7m --keep-original-file --ignore-signature-check --ignore-signers-certificate-check ${metadata_file}


You need to extract a plain (non-signed) invoice file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


::


    $ fattura_elettronica_reader invoice --extract-attachments --generate-html-output plain ${metadata_file}


Generic P7M files
`````````````````

You want everything, you trust nothing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::


    $ fattura_elettronica_reader generic --keep-original-file ${p7m_file}
