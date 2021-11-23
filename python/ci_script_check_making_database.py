import os

from dotenv import load_dotenv

from onedrive.onedrive import OneDrive  # type: ignore[import]
from xlsx_make import create_sanitized_xlsx
from xml_make_ead import create_output_files, create_xml_file

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Download from OneDrive
    folder = OneDrive(os.getenv("ONEDRIVE_LINK"), path="./inputs")
    folder.download()

    # Run database creation
    create_output_files()
    create_sanitized_xlsx("inputs/VolumesExcel/it_IT")
    create_xml_file("outputs/VolumesExcelSanitized/it_IT")
