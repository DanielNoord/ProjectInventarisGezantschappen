[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DanielNoord/ProjectInventarisGezantschappen/main.svg)](https://results.pre-commit.ci/latest/github/DanielNoord/ProjectInventarisGezantschappen/main)

# Archives of the Dutch Legations in Turin and Rome

This repository contains several `python` programs and data files used during the translation of and research for the archives of the Dutch Legations in Turin and Rome.

## Data overview

Some descriptive statistics about the data in the individuals database.

<details>
<summary>Individuals with data fields:</summary>

Updated as of 29-06-2022

> | Field | n | % |
> | :-: | :-: | :-: |
> | ISNI id |  314 | 38.34% |
> | 'Daniel' comment |  114 | 13.92% |
> | Birth dates |  531 | 64.84% |
> | Death dates |  545 | 66.54% |
> | Functions |  698 | 85.23% |
> | Images |  176 | 21.49% |
> | Name |  796 | 97.19% |
> | Place of birth |  502 | 61.29% |
> | Place of death |  501 | 61.17% |
> | Sources |  500 | 61.05% |
> | Sources other |  306 | 37.36% |
> | Surname |  819 | 100.00% |
> | Titles |  394 | 48.11% |
> | Wikidata id |  420 | 51.28% |

</details>

<details>
<summary>Individuals of type:</summary>

Updated as of 31-10-2021

> | Type |  n |   % |
> | :--: | :-: | :----: |
> |  0 | 80 | 9.77% |
> |  1 | 739 | 90.23% |
> |  2 |  0 |  0.0% |
> |  3 |  0 |  0.0% |
> |  4 |  0 |  0.0% |
> |  5 |  0 |  0.0% |

</details>

## Project structure

#### ./inputs and ./outputs

Location of relevant data files and _griglie_.

Both of these directories contain a `README.md` with additional details about their content.

#### ./python

Contains all `Python` programs that have been used to record, extract, control and translate data.

Further documentation can be found in the included `README.md`.

#### ./static

Contains `json` schema's for the various `.json` files in the inputs directory. Such files can be used by text-editors to check `.json` files for basic rules (e.g., Is field `surname` only letters? Is `date of birth` a date?).

## To-do list

Only some small editorial tasks remain to be done before creation of the final portal. These do not relate to the metadata of the actual archive, but rather to the additional database of individuals and places.

Editorial tasks:

| Done | Person | Task |
| :--- | :----- | :---- |
| | | Translate biographies fields starting with `From Koelman`. These are directly copied from the biographies as found in the Koelman book |
| | | Check the images currently linked to individuals for usability, some images are not as relevant (photos of individuals when they were a child, etc.) |
| | | Update sources that start with "https://notes9.senato.it/", "https://storia.camera.it/presidenti/", "https://storia.camera.it/deputato/" and "https://www.britannica.com/biography/". These links are not persistent so currently not sure how to refer to them |
| | | Look up individuals in _Dizionario bibliografico dell'Armata Sarda seimila biografie_. Relevant indivduals have _Dizionario bibliografico dell'Armata Sarda seimila biografie_ listed among their sources |
| | | Write biographical notes of individuals (or translate existing ones from biographic dictionaries) |
