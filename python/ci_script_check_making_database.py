from xml_check_document_numbers import traverse_c01_elements
from xml_make_ead import EADMaker

if __name__ == "__main__":
    # Run database creation
    eadmaker = EADMaker(
        "inputs/VolumesExcel/it_IT",
        True,
    )
    eadmaker.create_ead()
    with open("outputs/Legation_Archive.xml", encoding="utf-8") as file:
        traverse_c01_elements(
            file,
            "/Volumes/Seagate Basic Media/VolumesLegazione",
            True,
        )
