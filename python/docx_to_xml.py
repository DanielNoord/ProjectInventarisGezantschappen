import locale
import lxml.etree as etree

import create_xml
import parse_docx
import read_docx

def write_xml_file(localization, filename):
    print("Starting to create XML file!")
    locale.setlocale(locale.LC_ALL, localization)
    volumes_in_file = read_docx.extract_volumes(filename)
    root, archdesc = create_xml.basic_xml_file()

    # Parse and create volume entries
    for volume in volumes_in_file:
        v_number, v_title, v_date = parse_docx.volume(volume)

        # These volumes are incorrect
        if v_number in ["301", "302", "303", "306"]:
            continue

        # c01 is the c01-level entry for the volume
        c01 = create_xml.volume_entry(v_number, v_title, v_date, archdesc, localization)


        dossiers_in_volume = parse_docx.split_into_dossiers(volume)
        for dossier in dossiers_in_volume:
            # Create dossier entry
            d_number, d_pages, d_title, d_date,\
                d_serie_desc, files = parse_docx.dossier(dossier)
            c02 = create_xml.dossier_entry(v_number, d_number, d_pages,\
                d_title, d_date, c01, localization)

            # For debug purposes
            print(v_number, d_number, d_title)

            # Handle sub-series in dossiers
            if d_serie_desc:
                all_sub_series = parse_docx.sub_series(d_serie_desc)
                for sub_serie in all_sub_series:
                    d_d_pages, d_d_title, d_d_place, d_d_date =\
                        parse_docx.sub_dossier_description(sub_serie[0])
                    c03 = create_xml.dossier_with_desc(d_d_pages, d_d_title, d_d_place,\
                        d_d_date, c02, localization)
                    if sub_serie[1]:
                        for file in sub_serie[2].split("\n"):
                            f_pages, f_title, f_place, f_date = parse_docx.file(file)
                            create_xml.dossier_specific_file(f_pages, f_title, f_place,\
                                f_date, c03, localization)

            # If there are only files and no sub-series
            elif files:
                for file in files.split("\n"):
                    f_pages, f_title, f_place, f_date = parse_docx.file(file)
                    # Creates c04 level, might want to change
                    create_xml.dossier_specific_file(f_pages, f_title,\
                        f_place, f_date, c02, localization)
            
            # Handle "Insteeksels"
            elif "." in d_number:
                pass
            else:
                raise Exception()

    tree = etree.ElementTree(root)
    tree.write(f"EADFiles/Inventaris_{localization}.xml", pretty_print=True,\
        xml_declaration = True, encoding = 'UTF-8',\
        doctype='''<!DOCTYPE ead SYSTEM "http://www.nationaalarchief.nl/collectie/ead/ead.dtd">''')
    print("Writing XML complete!")

if __name__ == "__main__":
    write_xml_file("nl_NL", "Fonds Nederlandse Gezantschappen.docx")