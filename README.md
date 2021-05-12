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

## To-do list

### Before hand-off by Daniël

1) Finish persons with type 2
2) Clean last "incorrect" sources van laatste “incorrecte” bronvermeldingen
3) Create translation of individuals database
4) Add questions for Rome
5) Allow styling to be applied in excel
6) Write last document titles

### Before end of project

1) Translate "Comment" fields starting with `From Koelman`. These are directly copied from the biographies as found in the Koelman book
2) Write biographical notes of individuals (or translate existing ones)
3) Write short summary/introduction to archive, for example describe how the Legation at Rome also served as Legation for Turin. See an example at: "https://www.nationaalarchief.nl/onderzoeken/archief/2.05.12?page=1"

    Relevant sources: Wels, Santen

4) Find additional information about diplomatic represenative, current information is quite brief
5) Convert additional _griglie_ from Rome into standard that is compatible with programs (add identifiers, check for new individuals, etc.)
6) Write additional translation or titles which are not recognized yet (contact Daniël about regular expressions)
7) Check found images for usability
8) Update sources that start with "https://notes9.senato.it/", "https://storia.camera.it/presidenti/", "https://storia.camera.it/deputato/" and "https://www.britannica.com/biography/". These links are not persistent
9) Control translations
10) Contact Nationaal Archief about EAD and _.pdf_ conversion
11) Contact Rome about inconsistent document numbering. Use of "b", "v", "bis" (see commented code in `/python/functions/xlsx_sanitize.py`)
