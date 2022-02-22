# Archives of the Dutch Legations in Turin and Rome

This repository contains several `python` programs and data files used during the translation of and research for the archives of the Dutch Legations in Turin and Rome.

## Data overview

Some descriptive statistics about the data in the individuals database.

<details>
<summary>Individuals with data fields:</summary>

Updated as of 31-10-2021

> |      Field       |  n  |    %    |
> | :--------------: | :-: | :-----: |
> |       ISNI       | 216 | 41.06%  |
> | 'Daniel' comment | 78  | 14.83%  |
> |   Birth dates    | 340 | 64.64%  |
> |   Death dates    | 345 | 65.59%  |
> |    Functions     | 431 | 81.94%  |
> |      Images      | 75  | 14.26%  |
> |       Name       | 505 | 96.01%  |
> |  Place of birth  | 328 | 62.36%  |
> |  Place of death  | 329 | 62.55%  |
> |     Sources      | 337 | 64.07%  |
> |  Other sources   | 118 | 35.74%  |
> |     Surname      | 526 | 100.00% |
> |      Titles      | 247 | 46.96%  |
> |     Wikidata     | 287 | 54.56%  |

</details>

<details>
<summary>Individuals of type:</summary>

Updated as of 31-10-2021

> | Type |  n  |   %    |
> | :--: | :-: | :----: |
> |  0   | 74  | 14.07% |
> |  1   | 377 | 71.67% |
> |  2   | 13  | 4.37%  |
> |  3   |  0  |  0.0%  |
> |  4   | 20  | 3.80%  |
> |  5   | 32  | 6.08%  |

</details>

## Project structure

#### ./ead2pdf

Contains a submodule found on [GitHub](https://github.com/archivesspace-labs/ead2pdf) that converts `.xml` files to `.pdf` files based on a `.xsl` file.

_Note: for the final inventory a more advanced program made by the Dutch Nationaal Archief will be used._

#### ./EADFiles

Contains the `.dtd` and `.xsl` files needed for the `ead2pdf` submodule. Additional information about these file types can be found online.

_Note: files will become redundant after switch to the Nationaal Archief program._

#### ./inputs and ./outputs

Location of relevant data files and _griglie_.

Both of these directories contain a `README.md` with additional details about their content.

#### ./python

Contains all `Python` programs that have been used to record, extract, control and translate data.

Further documentation can be found in the included `README.md`.

#### ./static

Contains `json` schema's for the various `.json` files in the inputs directory. Such files can be used by text-editors to check `.json` files for basic rules (e.g., Is field `surname` only letters? Is `date of birth` a date?).

## To-do list

Editorial tasks:

| Done | Person | Task                                                                                                                                                                                                                                                            |
| :--- | :----- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|      |        | Translate biographies fields starting with `From Koelman`. These are directly copied from the biographies as found in the Koelman book                                                                                                                          |
|      |        | Check if indivduals of type 2 can be found or "finished"                                                                                                                                                                                                        |
|      |        | Check if individuals of type 5 can be found or "finished" when their respective _griglie_ have been sent                                                                                                                                                        |
|      |        | Check the images currently linked to individuals for usability, some images are not as relevant (photos of individuals when they were a child, etc.)                                                                                                            |
|      |        | Update sources that start with "https://notes9.senato.it/", "https://storia.camera.it/presidenti/", "https://storia.camera.it/deputato/" and "https://www.britannica.com/biography/". These links are not persistent so currently not sure how to refer to them |
|      |        | Look up individuals in _Dizionario bibliografico dell'Armata Sarda seimila biografie_. Relevant indivduals have _Dizionario bibliografico dell'Armata Sarda seimila biografie_ listed among their sources                                                       |
|      |        | Write biographical notes of individuals (or translate existing ones from biographic dictionaries)                                                                                                                                                               |
|      |        | Write summary/introduction to archive. Possibly relevant sources: Wels, Santen                                                                                                                                                                                  |
|      |        | Find additional information about Dutch diplomatic represenatives, current information is quite minimal                                                                                                                                                         |

Translation tasks:

| Done | Person | Task                                                                                                                                                            |
| :--- | :----- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|      |        | Convert additional _griglie_ from Rome into standard that is compatible with `python` programs (change names into identifiers, check for new individuals, etc.) |
|      |        | Write translations of titles which are not recognized yet using regular expression patterns                                                                     |

Programming tasks:

| Done | Person | Task                                                                                                                                                                                                                                                                                                      |
| :--- | :----- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| x    | Daniël | <s>Explore use of [`PNV`](https://www.nationaalarchief.nl/archiveren/nieuws/person-name-vocabulary-nu-beschikbaar)</s><br />Too difficult to do recursively and could create problems with other partners/formats                                                                                         |
| x    | Daniël | <s>Create integration with `WikiData` person database</s><br />All individuals have been looked for on [`WikiData`](https://www.wikidata.org/) and IDs have been added to the `wikidata:id` field<br />New searches can be done with `search_wikidata()` in `python/database_searches/search_wikidata.py` |
| x    | Daniël | <s>Explore integration with `SBN/ICCU` person database</s><br />Benefit [`SBN/ICCU`](https://www.iccu.sbn.it/) of integration is minimal as the database is not likely to have many new individuals. Furthermore, it does not have an accessible API                                                      |
| x    | Daniël | <s>Explore integration with `Cultura Italia` person database</s><br /> [`Cultura Italia`](http://www.culturaitalia.it) API is not easily accessible and difficult to connect to our database                                                                                                              |
| x    | Daniël | <s>Create integration with `ISNI` person database</s><br />All individuals have been looked for on [`ISNI`](https://isni.org) and IDs have been added to the `ISNI:id` field<br />New searches can be done with `search_isni_api()` in `python/database_searches/search_isni.py`                          |
| x    | Daniël | <s>Create integration with `Geonames` places database</s><br />All places have a [`Geonames`](https://www.geonames.org/) ID, latitude, longitude and all locations in the EAD-XML are tagged with their ID                                                                                                |
|      | Daniël | Contact Nationaal Archief about EAD and `.pdf` conversion                                                                                                                                                                                                                                                 |
|      | Daniël | Create database with support of all three languages                                                                                                                                                                                                                                                       |
| x    | Daniël | <s>Italics in titles in EAD-XML</s><br />Functions and document titles can use `_` to indicate italic sections, which are stored in the XML file.<br />For example: `John _Pope_` -> John _Pope_                                                                                                          |
| x    | Daniël | Final check of code, annotation and documentation                                                                                                                                                                                                                                                         |

End of project tasks:

| Done | Person       | Task                                                          |
| :--- | :----------- | :------------------------------------------------------------ |
|      | Project lead | Control translations (`Functions`, `Titles`, `DocumentTitles` |
