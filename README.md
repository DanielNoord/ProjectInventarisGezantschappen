# Archives of the Dutch Legations in Turin and Rome

This repository contains several `python` programs and data files used during the translation of and research for the archives of the Dutch Legations in Turin and Rome.

## Data overview

Some descriptive statistics about the data in the individuals database.

<details>
<summary>Individuals with data fields:</summary>
  
  Updated as of 03-10-2021

  >|Field|n|%|
  >|:---:|:---:|:---:|
  >|Comments|82|17.01%
  >|'Daniel' comment|71|14.73%
  >|Birth dates|299|62.03%
  >|Death dates|305|63.28%
  >|Functions|389|80.71%
  >|Images|54|11.20%
  >|Name|459|95.23%
  >|Place of birth|290|60.17%
  >|Place of death|292|60.58%
  >|Sources|391|81.12%
  >|Surname|482|100.00%
  >|Titles|222|46.06%

</details>

<details>
<summary>Individuals of type:</summary>
  
  Updated as of 03-10-2021

  >|Type|n|%
  >|:---:|:---:|:---:
  >0|30|6.22%
  >1|379|78.63%
  >2|19|3.94%
  >3|1|0.21%
  >4|20|4.15%
  >5|32|6.64%
  >6|1|0.21%

</details>

## Project structure

#### ./ead2pdf

Contains a submodule found on [GitHub](https://github.com/archivesspace-labs/ead2pdf) that converts `.xml` files to `.pdf` files based on a `.xsl` file.

*Note: for the final inventory a more advanced program made by the Dutch Nationaal Archief will be used.*

#### ./EADFiles

Contains the `.dtd` and `.xsl` files needed for the `ead2pdf` submodule. Additional information about these file types can be found online.

*Note: files will become redundant after switch to the Nationaal Archief program.*

#### ./inputs and ./outputs

Location of relevant data files and *griglie*.

Both of these directories contain a `README.md` with additional details about their content.

#### ./python

Contains all `Python` programs that have been used to record, extract, control and translate data.

Further documentation can be found in the included `README.md`.

#### ./static

Contains `json` schema's for the various `.json` files in the inputs directory. Such files can be used by text-editors to check `.json` files for basic rules (e.g., Is field `surname` only letters? Is `date of birth` a date?).

## To-do list

Editorial tasks:

|Done|Person|Task|
|:---|:---|:---
||| Translate `Comment` fields starting with `From Koelman`. These are directly copied from the biographies as found in the Koelman book
||| Check if indivduals of type 2 can be found or "finished"
||| Check if individuals of type 5 can be found or "finished" when their respective _griglie_ have been sent
||| Check the images currently linked to individuals for usability, some images are not as relevant (photos of individuals when they were a child, etc.)
||| Update sources that start with "https://notes9.senato.it/", "https://storia.camera.it/presidenti/", "https://storia.camera.it/deputato/" and "https://www.britannica.com/biography/". These links are not persistent so currently not sure how to refer to them
||| Look up individuals in _Dizionario bibliografico dell’Armata Sarda seimila biografie_. Relevant indivduals have _Dizionario bibliografico dell’Armata Sarda seimila biografie_ listed among their sources
||| Write biographical notes of individuals (or translate existing ones from biographic dictionaries)
||| Write summary/introduction to archive. Possibly relevant sources: Wels, Santen
||| Find additional information about Dutch diplomatic represenatives, current information is quite minimal

Finished volumes:
1, 3, 5, 6, 7, 8, 9, 10, 22

Translation tasks:

|Done|Person|Task|
|:---|:---|:---
||| Convert additional _griglie_ from Rome into standard that is compatible with `python` programs (change names into identifiers, check for new individuals, etc.)
||| Write translations of titles which are not recognized yet using regular expression patterns

Data tasks:

|Done|Person|Task|
|:---|:---|:---
||| See if see `ms280_94b` has been uploaded yet. What does this "b" refer to? It is unclear what this "b" document refers to
||| **Contact Rome about inconsistent document number suffixes.** Interchangeable use of "b", "v", "V" "bis", etc. See for example differences between ms279 and ms280 (for Daniël: see related commented code in `./python/xlsx_functions/sanitize.py`)

Programming tasks:

|Done|Person|Task|
|:---|:---|:---
||Daniël| Explore use of [`PNV`](https://www.nationaalarchief.nl/archiveren/nieuws/person-name-vocabulary-nu-beschikbaar)
|x|Daniël| <s>Create integration with `WikiData` person database</s><br />All individuals have been looked for on [`WikiData`](https://www.wikidata.org/) and IDs have been added to the `wikidata:id` field<br />New searches can be done with `search_wikidata()` in `python/database_searches/search_wikidata.py`
|x|Daniël| <s>Explore integration with `SBN/ICCU` person database</s><br />Benefit [`SBN/ICCU`](https://www.iccu.sbn.it/) of integration is minimal as the database is not likely to have many new individuals. Furthermore, it does not have an accessible API
||Daniël| Explore integration with `Cultura Italia` person database
||Daniël| Finish integration with `ISNI` person database
|x|Daniël| <s>Create integration with [`Geonames`](https://www.geonames.org/) places database</s><br />All places have a Geonames ID, latitude, longitude and all locations in the EAD-XML are tagged with their ID
||Daniël| Contact Nationaal Archief about EAD and `.pdf` conversion
||Daniël| Create database with support of all three languages
|x|Daniël| <s>Italics in titles in EAD-XML</s><br />Functions and document titles can use `_` to indicate italic sections, which are stored in the XML file.<br />For example: `John _Pope_` -> John _Pope_
||Daniël| Create controls of document and volume numbering (consecutive, non-overlapping, suffixes)
||Daniël| Final check of code, annotation and documentation

End of project tasks:

|Done|Person|Task|
|:---|:---|:---
||Project lead| Control translations (`Functions`, `Titles`, `DocumentTitles`
