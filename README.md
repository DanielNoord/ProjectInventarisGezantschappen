### Project Nederlandse Gezantschappen in Turijn en Rome
My task is to translate and correct the inventory of this archive. The code and files in this repo have helped me do this in an organized and consistent manner.
The executable file `Makepdf_nl_NL` can be used to generate a new `Inventaris_nl_NL.pdf` if `Fonds Nederlandse Gezantschappen.docx` is found in the `/inputs` directory.

### `/EADFiles`
Contains the stylesheets for the EAD specification and its translation into PDF.

### `/ead2pdf`
Contains a submodule found on github that translates .xml files to .pdf files based on a .xsl file.

### `/inputs` and `/outputs`
Input files should go in `/inputs` while output files will be placed in `/outputs`

### `/python`
Contains two related programs. `docx_to_xml.py` extracts the volumes from the archive inventory .docx file and translates them into a .xml file. `docx_to_names.py` extracts the list of names from the `Eigenamen.docx` file in `/inputs` and creates a file with a more readable list of individuals.
