## Inputs directory

This directory contains a number of documents and sub-directories with data, either related to the actual inventory or the indivudals that are mentioned in the documents in the archive.

### Individuals.json

This is the _main_ database of the individuals mentioned in the archive. It contains all information about all individuals as is currently known.

A JSON Schema for the database can be found at `./static/JSON/Indivudals.json`. This is a description of how the field and entries should be written and can be used to test if the database is "correct".

Here follows a short summary and example of each field for an indivdual entry (person).

<details>
<summary>Database description</summary>
Each entry has a unique identifier. This is often a `$` followed by the surname of the individual. Each entry has 15 fields.

    1) `ISNI:id`: 0000 0000 7777 905X
        The [`ISNI`](https://isni.org) id of the indidivual if it exists. Otherwise it is `null`.

    2) `comment_daniel`: ...
        A comment about the individual that is only relevant during the data collection process and should not be stored in the final database.

    3) `date_of_birth`: 1806-04-02
        Date of birth of the individual. Follows pattern yyyy-mm-dd. Don't forget to add leading 0's for month and day (see example).

    4) `date_of_death`: 1876-11-06
        Date of death of the individual. Follows pattern yyyy-mm-dd. Don't forget to add leading 0's for month and day (see example).

    5) `functions`: Pro-segretario di Stato e Presidente del Consiglio dei Ministri dello Stato Pontificio (1848-03-10/1848-04-29)
        Functions of individual in **Italian**. If dates are known those can be added. Don't forget to add a `/` if only one date is known. Words in italics in final inventory are between `_`, parentheses are indicated by `{}`.

    6) `images`: https://rkd.nl/explore/images/250221
        Links to images of the individual.

    7) `name`: Giacomo
        First name of individual.

    8) `person_type`: 0
        Each individual has a type, this indicates how finished their entry is.

        `0` is "important". A more detailed biographical note would be preferable. These should be stored in `inputs/Biographies.json`

        `1` is "finished" (or not likely that any additional sources will be found).

        Previous but now unused types:

        `2` is "unfinished". Additional sources need (or shoud be able) to be found.

        `3` is "waiting on others". A request for information has been sent to external parties.

        `4` is "question project lead". This person has a question that needs to be answered by the project lead. This question can (often) be found under the field `comment_from_daniel`

        `5` is "waiting on scan". Need additional information from archive to identify this individual.

    9)  `place_of_birth`: Sonnino
        Place of birth of individual in Italian.

    10) `place_of_death`: Roma
        Place of death of individual in Italian.

    11) `sources`: Aubert, Roger, 'Antonelli, Giacomo', in: Dizionario Biografico degli Italiani. Volume 3 (Rome, Treccani, 1961), found on: https://www.treccani.it/enciclopedia/giacomo-antonelli_(Dizionario-Biografico)
        Secondary or "good" sources relevant for the indidivual. Places are in English.

    12) `sources_other`: Osservatore del Trasimeno, Anno XIII, 29 (Perugia, 1838-04-10), 1
        Primary or "weak" sources relevant for the indidivual. Places are in English.

    13) `surname`: Antonelli
        Surname of individual.

    14) `title`: card. (1847-06-11/)
        Titles of individual in **Italian**. If dates are known those can be added. Don't forget to add a `/` if only one date is known.

    15) `wikidata:id`: Q712085
        [`WikiData`](https://www.wikidata.org/) ID of the indiviual if it exists. Otherwise it is `null`.

</details>

#### Adding a new individual to the database

 The most straight-forward method to add a new individual is to duplicate a previous entry and change the identifier to a new **unused** identifier. Subsequently, update all the fields to match the new individual. **Make sure to use the correct structure of the data fields**, even if fields are empty.

### Biographies.json

This file stores all biographies and biographical notes of all individuals that have one. They are stored in the `en_GB`, `it_IT` and `nl_NL` fields for the respective languages.

### SourcePatterns.json

`Json` file with regular expression patterns for used sources in the database that gets used to check if they conform to a certain standard of annotation.

### Translations

The directory Translations contains all translation of document titles, functions, places and titles in Dutch, Italian and English. JSON Schema's for the respective documents can be found in the `./static/JSON/` folder.

The `DocumentTitles`, `Functions` and `Titles` documents follow this structure:

- English translation
- Dutch translation

For `Titles` a fourth field is added which indicates whether the title should be placed `Before` (count Jan Jansen) of `After` (Jan Jansen, prince of Utrecht) the name.
The Italian translation in `DocumentTitles` is a regular expression pattern that matches the title used in the `excel` _griglie_ file.

`Placenames` follows a similar structure, but also has the following fields:

- `geonames_id`: the [`Geonames`](https://www.geonames.org/) id for the place.
- `geonames_wikipedia`: a link to the wikipedia page of the place.
- `latitude`: the latitude of the place downloaded from `GeoNames`.
- `longitude`: the longitude of the place downloaded from `GeoNames`.

#### Regular expression example

Translation pair in file:

- _Copia di una lettera (di|del|della) (\$\w*) (a|al) (\$\w*) circa la morte (di|del|della) (\$\w\*)$_
- _Kopie van een brief van \2 aan \4 over de dood van \6_

Result in inventory:

- _Copia di una lettera di $VanNoord al $Jansen circa la morte della $Pietersen_
- _Kopie van een brief van $VanNoord aan $Jansen over de dood van $Pietersen_

(\$\w\*) corresponds to an identifier, for example $VanNoord. Because it is the second pattern in between parenthesis it is replaced by \2. The $ at the end of the line indicates a line-break.

Additional explanations of regular expressions can be found online.

### VolumesExcel

The folder `VolumcesExcel` contains a sub-directory `original`. These are all the _griglie_ without any changes as received from Rome.

The sub-directory _it_IT_ contains the modified _griglie_ in Italian. They use the identifiers as found in the individuals database and modified document titles where necessary. Important to note that individuals who get a title in front of their name need a preposition with article in Italian. For example: _“Lettera al $HoevenE”_ and _“Lettera a $DoderoG”_.

### Oud

This directory contains the original inventory in `.docx` and the translation of this in Dutch made at the start of the project.
