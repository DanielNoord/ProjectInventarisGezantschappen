# Inputs directory

This directory contains a number of documents and sub-directories with data, either related to the actual inventory or the indivudals that are mentioned in the documents in the archive.

For the sake of usability most documents are included both in _.json_ and _.docx_ format. In case of conflicts between these documents the _.json_ files should be seen as _leading_. For future updates, it is preferable to use the _.json_ format.

## Individuals.json/docx

This is the _main_ database of the individuals mentioned in the archive. It contains all information about all individuals as is currently known.

A JSON Schema for the database can be found at `./static/JSON/Indivudals.json`. This is a description of how the field and entries should be written and can be used to test if the database is "correct".

Here follows a short summary and example of each field for an indivdual entry (person). It is important to follow the JSON Schema and structure of each field, as otherwise data will be lost on conversion from _.json_ and _.docx_ to other databases.

<details>
<summary>Database description</summary>
Each entry has a unique identifier. This is often a `$` followed by the surname of the individual. Each entry has 13 fields. In the .docx document each field is represented by the name of the field, a `:`, a space and the data of that field.

    1) Type: 1
    Each individual has a type, this indicate how finished their entry is.

        0 is "important". A more detaild biographical note would be preferable.

        1 is "finished" (or not likely that any additional sources will be found).

        2 is "unfinished". Additional sources need (or shoud be able) to be found.

        3 is "waiting on others". A request for information has been sent to external parties.

        4 is "question project lead". This person has a question that needs to be answered by the project lead. This question can be found under the field “Comment from Daniël”

        5 is "waiting on scan". Need additional information from archive to identify this individual.

    2) Surname: Alewijn
    Surname of the individual.

    3) Name: Henrick
    First name of individual.

    4) Date of birth: 1785-08-22
    Date of birth of the individual. Follows pattern yyyy-mm-dd. Don't forget to add leading 0's (see example).

    5) Place of birth: Amsterdam
    Place of birth of individual in Italian.

    6) Date of death: 1850-02-24
    Date of death of the individual. Follows pattern yyyy-mm-dd. Don't forget to add leading 0's (see example).

    7) Place of death: Genova
    Place of death of individual in Italian.

    8) Titles: jhr. (1821-09-01/1847-08-21)| ridder| baron (1847-08-22/)| hertog (/1860)
    Titles of individual in Dutch. Multiple titles are seperated by `| `. If dates are known those can be added. Don't forget to add a `/` if only one date is known.

    9) Functions: _Governatore_ {gouverneur} van Rome, vice-camerlengo van de Rooms-Katholieke Kerk en directeur-generaal van de politie van Rome (1842/)
    Functions of individual in Dutch. Multiple titles are seperated by `| `. If dates are known those can be added. Don't forget to add a `/` if only one date is known. Words in italics in final inventory are between `_`, parentheses are indicated by `{}` (see example).

    10) Comment: Louis Bosch represented a lady referred to as 'the widow Henriette Natalie Sturbaut' in the dispute surrounding the inheritance of Francesco Cornelio Verbruggen.
    Short biographical note or remark in English.

    11) Comment from Daniël: How do we write this name?
    Comment from Daniël, often containing a question for the project lead.

    12) Sources: Beth, J.C., De archieven van het Departement van Buitenlandsche Zaken (L'Aia, 1918), 356| van Santen, Cornelis Willem, Het internationale recht in Nederlands buitenlands beleid: een onderzoek in het archief van het Ministerie van Buitenlandse Zaken (L'Aia, 1955), 644, 670| Stadsarchief Amsterdam, Amsterdam, inventory number: 2.10.2.6
    Sources. Multiple sources are separeted by "| ". Places are in Italian. Links cannot be hyperlinks in .docx to prevent data loss.

    13) Images: https://rkd.nl/explore/images/144618| https://rkd.nl/explore/images/144620| https://rkd.nl/explore/images/144623| https://rkd.nl/explore/images/144637
    Images of the individual. Multiple sources are separeted by "| ". Places are in Italian. Links cannot be hyperlinks in .docx to prevent data loss.
</details>

### Adding a new individual to the database

Adding a new individual to the database is possible both in the _.docx_ and _.json_ files. The most straight-forward method is to duplicate a previous entry and change the identifier to a new **unused** identifier. Subsequently, update all the fields to match the new individual. **Make sure to use the correct structure of the data fields**, even if fields are empty. For the _.docx_ version the means to always add a single space after the `:`, so "Surname: " and **not** "Surname:". Otherwise conversion to _.json_ is impossible and the errors will need to fixed at a later time.

## Translations

The directory Translations contains all translation of document titles, functions, places and titles in Dutch, Italian and English. Copies in _.docx_ can be found in the same directory. Make sure to only add updates to either the _.docx_ or _.json_ files. JSON Schema's for the respective documents can be found in the `./static/JSON/` folder.

The `TranslatedFunctions` en `TranslatedTitles` documents follow this structure:

- Dutch translation
- Italian translation
- English translation

For `TranslatedTitles` a fourth field is added which indicates whether the title should be placed `Before` (graaf Jan Jansen) of `After` (Jan Jansen, prins van Utrecht) the name..

`TranslatedPlacenames` follows this structure:

- Italian translation
- Dutch translation
- English translation

`TranslatedDocumentTitles` follows the same structure as `TranslatedPlacenames`. However, it uses _regular expression_ pattern matching to make the translations more flexible.

### Regular expression example

Translation pair in file:

- _Copia di una lettera (di|del|della) (\$\w*) (a|al) (\$\w*) circa la morte (di|del|della) (\$\w*)$_
- _Kopie van een brief van \2 aan \4 over de dood van \6_

Result in inventory:

- _Copia di una lettera di $VanNoord al $Jansen circa la morte della $Pietersen_
- _Kopie van een brief van $VanNoord aan $Jansen over de dood van $Pietersen_

(\$\w*) corresponds to an identifier, for example $VanNoord. Because it is the second pattern in between parenthesis it is replaced by \2. The $ at the end of the line indicates a line-break.

Additional explanations of regular expressions can be found online.</details>

## VolumesExcel

The folder `VolumcesExcel` contains a sub-directory `original`. These are all the _griglie_ without any changes as received from Rome.

The sub-directory _it\_IT_ contains the modified _griglie_ in Italian. They use the identifiers as found in the individuals database and modified document titles where necessary. Important to note that individuals who get a title in front of their name need a preposition with article in Italian. For example: _“Lettera al $HoevenE”_ and _“Lettera a $DoderoG”_.

To facilitate searching in the archive the directory also contains a file `Paesi Bassi ALL FILES.xlsx`. This is a collection of all original _griglie_ as received from Rome, without any modifications.

## Oud

This directory contains the original inventory in _.docx_ and the translation of this in Dutch made at the start of the project.
