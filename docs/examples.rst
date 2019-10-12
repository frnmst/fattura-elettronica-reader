Examples
========

CLI
---

You want everything, you trust nothing
``````````````````````````````````````


::


$ fattura_elettronica_reader -A ${metadata_file}


which is the same as


::


$ fattura_elettronica_reader -H -a -o ${metadata_file}


You want everything, you trust everything
`````````````````````````````````````````


::


$ fattura_elettronica_reader -SsAkwW ${metadata_file}


which is the same as


::


$ fattura_elettronica_reader -H -a -o -S -s -w -W ${metadata_file}


You need to extract a plain (non-signed) invoice file
`````````````````````````````````````````````````````


::


$ fattura_elettronica_reader -b -H ${metadata_file}
