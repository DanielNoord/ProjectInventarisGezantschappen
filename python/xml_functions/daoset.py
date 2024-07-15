from lxml import etree
from typing_utils.data_classes import FileData, SeriesData


def fix_daoset(root: etree._Element) -> None:
    """Fixes daoset with only one dao entry."""
    for daoset in root.iterdescendants("daoset"):
        if len(child_nodes := daoset.getchildren()) == 1:  # type: ignore[attr-defined]
            # Change dao-element to have coverage of whole
            child_nodes[0].attrib["coverage"] = "whole"

            if (parent := daoset.getparent()) is None:
                raise ValueError(f"{daoset} is missing a parent element!")

            # Append daoset to did-element (parent node of daoset) and remove daoset
            parent.append(child_nodes[0])
            parent.remove(daoset)


def add_dao(daoset: etree._Element, file_data: FileData, individual_verso: bool) -> None:
    """Adds a dao element to a daoset."""
    filename = f"VolumesLegazione/{file_data.file_name.split('_')[0]}/{file_data.file_name}"
    # If only a verso we only add the verso dao-element
    if individual_verso:
        etree.SubElement(
            daoset,
            "dao",
            {
                "coverage": "part",
                "daotype": "derived",
                "id": f"{file_data.file_name}.tif",
                "href": f"{filename}.tif",
            },
        )
    elif file_data.only_recto:
        etree.SubElement(
            daoset,
            "dao",
            {
                "coverage": "part",
                "daotype": "derived",
                "id": f"{file_data.file_name}r.tif",
                "href": f"{filename}r.tif",
            },
        )
    elif file_data.only_verso:
        etree.SubElement(
            daoset,
            "dao",
            {
                "coverage": "part",
                "daotype": "derived",
                "id": f"{file_data.file_name}v.tif",
                "href": f"{filename}v.tif",
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
                "href": f"{filename}r.tif",
            },
        )
        etree.SubElement(
            daoset,
            "dao",
            {
                "coverage": "part",
                "daotype": "derived",
                "id": f"{file_data.file_name}v.tif",
                "href": f"{filename}v.tif",
            },
        )


def add_volume_dao(daoset: etree._Element, vol_data: SeriesData) -> None:
    """Adds a dao element to a daoset for a volume (ms...)."""
    filename = f"VolumesLegazione/MS{vol_data.num}/MS{vol_data.num}"
    etree.SubElement(
        daoset,
        "dao",
        {
            "coverage": "part",
            "daotype": "derived",
            "id": f"MS{vol_data.num}_d.tif",
            "href": f"{filename}_d.tif",
        },
    )
    etree.SubElement(
        daoset,
        "dao",
        {
            "coverage": "part",
            "daotype": "derived",
            "id": f"MS{vol_data.num}_p.tif",
            "href": f"{filename}_p.tif",
        },
    )
