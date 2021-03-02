import lxml.etree as etree


def basic_xml_file():
    root = etree.Element("ead")

    # Eadheader
    eadheader = etree.SubElement(root, "eadheader")
    eaddid = etree.SubElement(eadheader, "eadid")
    comment = etree.Comment('Nationaal Archief')
    eaddid.append(comment)

    # Filedesc
    filedesc = etree.SubElement(eadheader, "filedesc")
    titlestmt = etree.SubElement(filedesc, "titlestmt")
    titleproper = etree.SubElement(titlestmt, "titleproper")
    titleproper.text = "Inventaris van het archieffonds van de Nederlandse Gezantschappen \
                            in Turijn en Rome, 1816 - 1874"
    author = titleproper = etree.SubElement(titlestmt, "author")
    author.text = "D.M. van Noord"
    publicationstmt = etree.SubElement(filedesc, "publicationstmt")
    publisher = etree.SubElement(publicationstmt, "publisher")
    publisher.text = "KNIR"
    date = etree.SubElement(publicationstmt, "date", calendar = "gregorian",\
        era = "ce", normal = "2021")
    date.text = "(c) 2021"
    para = etree.SubElement(publicationstmt, "p", id = "copyright")
    extref = etree.SubElement(para, "extref", linktype = "simple",\
        href = "http://creativecommons.org/publicdomain/zero/1.0/",\
        actuate = "onrequest", show = "new")
    extref.text = "cc0"

    # Profiledesc
    profiledesc = etree.SubElement(eadheader, "profiledesc")
    language = """<langusage>This finding aid is written in
            <language langcode="dut" scriptcode="Latn"> Dutch</language>.
        </langusage>"""
    profiledesc.append(etree.fromstring(language))
    descrules = etree.SubElement(profiledesc, "descrules")

    # Archdesc
    archdesc = etree.SubElement(root, "archdesc", level = "fonds", type = "inventory")
    archdescdid = etree.SubElement(archdesc, "did")
    unittitle = etree.SubElement(archdescdid, "unittitle")

    return root, archdesc
