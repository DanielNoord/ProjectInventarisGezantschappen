# Outputs directory

After running any of the programs in the `python` directory their outputs will be put in this directory. Most importantly, it contains directories with the the modified and translated _griglie_.

## Griglie

`VolumesExcelSanitized` contains the Italian _griglie_ with identifiers and some sanitizations such as removal of double spaces, comma's at the end of document titles and adding missing capital letters. The directory is based on the `it_IT` folder as found in the `inputs` directory.

`VolumesExcelTranslated` contains the English and Dutch _griglie_ with identifiers. It is based on `VolumesExcelSanitized`.

`VolumesExcelFinal` contains the final _griglie_ where identifiers have been replaced with full names, titles and functions. The _griglie_ are stored in all three languages and are based on `VolumesExcelSanitized` (for the Italian version) and `VolumesExcelTranslated`.

`VolumesExcelControl` is an additional directory where the _griglie_ from `VolumesExcelFinal` are combined with the original _griglie_ as received from Rome. This makes checking translations, titles and changes across all languages easier.

## Other outputs

Other outputs besides the _griglie_ include the _.pdf_ of the inventory and updates individuals databases after certain programs have been run on it.
