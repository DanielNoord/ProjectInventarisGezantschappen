## Python directory

The python directory contains a number of programs used during the project. Most functions are part of a module that is then loaded by any of the files in the base directory. The files in the base directory are scripts that should be run from the project's root.

_All programs are intended to be run from the project's root._

### data_parsing

Module with functions that can 1) load all translations and data files and 2) create the "filled in" name string. Based on the (translation) data provided these functions return a string with the full name and function and titles of individuals in Italian, English and Dutch.

### database_controls

Module with functions that are used to check the `Individuals.json` file for inconsistencies such as unknown titles or placenames, incorrect ISNI's or nonsensical dates.

### database_searches

Module with functions used to perform automatic database searches. We currently support searching in `Biografisch Portaal van Nederland`, `Dizionario storico biografico della Tuscia`, `ISNI`, an upcoming book about `Johan Koelman`, `Nationaal Archief`, `RKD` and `WikiData`. Results are printed to standard output so should ideally by piped to a file to allow checking of actual corrects hits.

### date_functions

Module with functions related to checking and comparing dates. These are used throughout the project for example to control that we don't refer to the `31st of February`.

### deprecated_functions

Non-functional module which contains all files that were used in previous stages of the project. These functions or script can't be expected to work anymore, but are kept for later reference.

### docx_functions

Module with functions used to write, read and parse `docx` files. With the switch to only using `json` these functions tend to get outdated quickly, but should in theory still work.

### typing_utils

Module that stores some of our typing aliases.

### write_files

Module with functions that homogenizes the process of writing files. For example, throughout the project writing a `json` file is done using the same functions and thus goes through the same checks.

### xlsx_functions

Module with functions used to write, read and parse `xlsx` files. As the project is evolving to only using `xml` for the final database the writing of `xlsx` files for the final database can become outdated. However, sanitization and parsing of base data is still done with this module.

### xml_functions

Module with functions used to write the final `xml` file. We use `lxml` to create an EAD-compliant `xml` file.

### Scripts

- `ci_script_check_making_database`: Script that uses the `excel` _griglie_ and tries to create a `xml` database from them. Used in the CI on GitHub.
- `docx_make_controls_translations`: Transforms the `json` files of our data and translations into `docx` files which are easier to read during the control process.
- `json_control_database`: Main script used to control the database on inconsistencies and errors. Also used in the CI.
- `json_create_descriptive_stats`: Script to print some stats about the database.
- `json_geonames`: Script used to add geonames identifiers to `Placenames.json` and update that file based on already present identifiers.
- `json_load_translations`: Script to write `json` files from translations files in `docx` format.
- `json_perform_database_searches`: Script to perform some of the searches included in the `database_searches` module.
- `json_save_load_database`: Script that can write `Individuals.json` to `docx` and vice-versa, as well as merge a `docx` and `json` version.
- `json_sort_database`: Script to sort `Individuals.json` and the data of the fields of the individuals within it.
- `rename_scans`: Script to quickly rename a directory of scans.
- `xlsx_make`: Script to make the final database in `xslx` format.
- `xml_check_document_numbers`: Script to check if the files discussed in the `xml` EAD database correspond with the scans found in a certain directory (or hard drive).
- `xml_make_ead`: Script to make the final database in `xml` format.
