# Archives of the Dutch Legations in Turin and Rome

This repository contains a number of python programs and data files used during the translation of and research for the archives of the Dutch Legations in Turin and Rome.

## Project structure

### /ead2pdf

Contains a submodule found on github that converts _.xml_ files to _.pdf_ files based on a _.xsl_ file.

This particular submodule was mainly used during the initial phase of the project. For the final inventory a program made by the _Nationaal Archief_ will be used. This creates a _.pdf_ that is checked for compliancy with EAD standard.

### EADFiles

Contains the _.dtd_ and _.xsl_ files needed for the ead2pdf submodule. Additional information about these file types can be found online.

### /inputs and /outputs

Location of relevant data files and.

Both of these directories contain a `README.md` with addiational details about their content.

### /python

Contains all Python programs that have been used to record, extract, control and translate data.
Further documentation can be found in the included `README.md`.

### /static

Contains JSON Schema's for the various _.json_ files in the inputs directory.
