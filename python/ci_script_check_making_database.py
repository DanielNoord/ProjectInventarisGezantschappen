import os

from dotenv import load_dotenv

from onedrive.onedrive import OneDrive  # type: ignore[import]
from xml_make_ead import EADMaker

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Download from OneDrive
    folder = OneDrive(os.getenv("ONEDRIVE_LINK"), path="./inputs")
    folder.download()

    # Run database creation
    eadmaker = EADMaker(
        "inputs/VolumesExcel/it_IT",
        True,
    )
    eadmaker.create_ead()
