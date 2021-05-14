# Outputs directory

After running any of the programs in the `python` directory their outputs will be put in this directory. Most importantly, it contains directories with the the modified and translated _griglie_.

## Griglie

`VolumesExcelSanitized` contains the Italian _griglie_ with identifiers and some sanitizations such as removal of double spaces, comma's at the end of document titles and adding missing capital letters. The directory is based on the `it_IT` folder as found in the `inputs` directory.

`VolumesExcelTranslated` contains the English and Dutch _griglie_ with identifiers. It is based on `VolumesExcelSanitized`.

`VolumesExcelFinal` contains the final _griglie_ where identifiers have been replaced with full names, titles and functions. The _griglie_ are stored in all three languages and are based on `VolumesExcelSanitized` (for the Italian version) and `VolumesExcelTranslated`. Titles in blue are not currently recognized by the automatic translation program and need to be added to `./inputs/Translations/DocumentTitles.json`. Titles in red are also red in the original _griglie_ from Rome.

`VolumesExcelControl` is an additional directory where the _griglie_ from `VolumesExcelFinal` are combined with the original _griglie_ as received from Rome. This makes checking translations, titles and changes across all languages easier. Note that **colours** as described above are not copied due to limitations of _.xlsx_ files.

## Other outputs

Other outputs besides the _griglie_ include the _.pdf_ of the inventory and updates individuals databases after certain programs have been run on it.
