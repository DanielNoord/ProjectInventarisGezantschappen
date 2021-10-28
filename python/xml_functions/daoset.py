import re

from lxml import etree
from typing_utils.data_classes import FileData


def fix_daoset(root: etree._Element) -> None:
    """Fixes daoset with only one dao entry"""
    for daoset in root.iterdescendants("daoset"):  # type: ignore
        if len(child_nodes := daoset.getchildren()) == 1:
            # Change dao-element to have coverage of whole
            child_nodes[0].attrib["coverage"] = "whole"

            # Append daoset to did-element (parent node of daoset) and remove daoset
            daoset.getparent().append(child_nodes[0])
            daoset.getparent().remove(daoset)


def add_dao(daoset: etree._Element, file_data: FileData) -> None:
    """Adds a dao element to a daoset"""
    
    # If only a verso we only add the verso dao-element
    if re.match(r".+v", file_data.file_name):
        etree.SubElement(
            daoset,
            "dao",
            {
                "coverage": "part",
                "daotype": "derived",
                "id": f"{file_data.file_name}.tif",
            },
        )
    else:
        etree.SubElement(
            daoset,
            "dao",
            {
                "coverage": "part",
                "daotype": "derived",
                "id": f"{file_data.file_name}r.tif",
            },
        )
        etree.SubElement(
            daoset,
            "dao",
            {
                "coverage": "part",
                "daotype": "derived",
                "id": f"{file_data.file_name}v.tif",
            },
        )
