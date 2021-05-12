# Python directory

The python directory contains a number of programs used during the project. The sub-directory `functions` contains some auxiliary functions that can be imported by any of the other programs. The `depreciated` sub-directory contains programs that are no longer used, but are kept for the sake of reporting and showing the progress of the project.

## Database_searches

Contains a number of programs that search online database for the combination of names and surnames as found in the individuals database. Results are printed to the console and can be piped to a file using:

```bash
python3 program.py > file
```

## docx_ category

`docx_make_controls_translations.py` creates _.docx_ files from the _.json_ files containing translations.

`docx_make.py` contains auxiliary functions used to write _.docx_ files.

## json_ category

A number of functions related to the data files in _.json_. The documents starting with `json_check` contain checks for the individuals database and whether the data entered follows certain patterns. Running `json_control_database.py` loads all these programs and performs them and some additional checks.

`json_create_descriptive_stats.py` prints out some descriptive statistics about the individuals database.

`json_load_translations.py` contains functions that convert _.docx_ documents of the various translations to _.json_ files.

`json_save_load_database.py` can be used to convert the individuals _.json_ database to _.docx_, covert vice-versa and merge a _.docx_ and _.json_ file. During merging precedence is given to the _.docx_ file.

## xlsx_make.py

Based on the `./inputs` directory creates the sanitized, translated and filled _.xlsx_ documents of the _griglie_. Outputs can be found in `./outputs`.

## xml_make.py

Based on the _.xlsx_ documents of the _griglie_ in `./outputs` makes a _.xml_ file of the inventory. This file is EAD compliant. Running `./Makepdf_it_IT` (or the code inside that file) creates a test _.pdf_ file using the submodule `./ead2pdf`.
