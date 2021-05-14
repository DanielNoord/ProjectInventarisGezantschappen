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

## Project overview

Some descriptive statistics about the data in the individuals database, as of 2021-05-04.

Individuals with data fields:
>|Field|n|%|
>|:---:|:---:|:---:|
>|Comments|82|17.41%
>|'Daniël' comments|72|15.29%
>|Birth date|288|61.15%
>|Death date|294|62.24%
>|Functions|377|80.04%
>|Images|50|10.62%
>|Name|448|95.12%
>|Place of birth|279|59.24%
>|Place of death|281|59.66%
>|Sources|380|80.68%
>|Surname|471|100%
>|Titles|210|44.59%

Individuals of type:
>|Type|n|%
>|:---:|:---:|:---:
>|0|30|6.37%
>|1|367|77.92%
>|2|20|4.25%
>|3|1|0.21%
>|4|20|4.25%
>|5|33|7.01%

## To-do list

### Before end of project

Individuals database:

>1) Translate "Comment" fields starting with `From Koelman`. These are directly copied from the biographies as found in the Koelman book
>2) Check if indivduals of type 2 can be found or "finished"
>3) Check if individuals of type 5 can be found or "finished" when their respective _griglie_ have been sent
>4) Check the images currently linked to individuals for usability, some images are not as relevant (photos of individuals when they were a child, etc.)
>5) Update sources that start with "https://notes9.senato.it/", "https://storia.camera.it/presidenti/", "https://storia.camera.it/deputato/" and "https://www.britannica.com/biography/". These links are not persistent so currently not sure how to refer to them
>6) Look up individuals in _Dizionario bibliografico dell’Armata Sarda seimila biografie_. Relevant indivduals have _Dizionario bibliografico dell’Armata Sarda seimila biografie_ listed among their sources
>7) _See if other databases might be relevant to be linked to database, and if so do so. For example Italian SBN/ICCU database and Cultura Italia. Contact Daniël to see if this can be automated_

Additional information:

>1) Write biographical notes of individuals (or translate existing ones from biographic dictionaries)
>2) Write short summary/introduction to archive, for example describe how the Legation at Rome also served as Legation for Turin. See an example at: "https://www.nationaalarchief.nl/onderzoeken/archief/2.05.12?page=1"
>    Relevant sources: Wels, Santen
>3) Find additional information about Dutch diplomatic represenatives, current information is quite minimal

Translation:

>1) Convert additional _griglie_ from Rome into standard that is compatible with python programs (change names into identifiers, check for new individuals, etc.). Contact Daniël before doing so for some useful tips!
>2) Write additional translation or titles which are not recognized yet (contact Daniël about regular expressions)
>3) Control current translations

Daniël:

>1) Contact Nationaal Archief about EAD and _.pdf_ conversion
>2) If needed, translate individuals database into all languages (dependent on requirements of site)
>3) Find a way to apply _italics_ in titles and functions (indicated by `_text_`) to _.xlsx_ documents
>4) Final check of code and annotation

Project lead:

>1) **Check if the numbering of documents in _griglie_ corresponds to scans.** Currently there are discrepancies between the document numbers in _griglie_ and in the directories uploaded by the scanners (see missing ms280\_94b). It is unclear what this "b" document refers to. Daniël has created controls to see if _griglie_ and numbers in directories with scans correspond, currently this produces numerous errors/warnings
>2) **Contact Rome about inconsistent document number suffixes.** Interchangeable use of "b", "v", "V" "bis", etc. See for example differences between ms279 and ms280 (for Daniël: see related commented code in `./python/functions/xlsx_sanitize.py`). Daniël has created checks to see if numbers in _griglie_ are successive (including "bis"), but this can't currently handle these suffixes as it is unclear what they signify and therefore if their numbering can indeed be considered "successive". This and point 1 are especially important with the knowledge that later volumes also contains "inserted documents" > how do we number those?
>3) Related to point 7 of _Individuals database_ list: do we want to link the database to international identification databases? (for example, see <https://en.wikipedia.org/wiki/International\_Standard\_Name\_Identifier>). Such databases often do not contain much additional information themselves but help link to other relevant sources, similar to _Biografisch Portaal_
