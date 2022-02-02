# pylint: disable-next=too-few-public-methods
class _ErrorLogger:
    """Class which creates files and attributes to log errors to."""

    def __init__(self) -> None:
        self.log_missing_translations = "outputs/missing_translations"
        """Filename of the log file used to track missing translations."""

        self.log_missing_titles = "outputs/missing_titles"
        """Filename of the log file used to track missing titles."""

        self.log_title_errors = "outputs/title_errors"
        """Filename of the log file used to track errors in document titles."""

        self.log_xml_errors = "outputs/xml_errors"
        """Filename of the log file used to track errors in the xml file."""

        self._create_logging_files()

    def _create_logging_files(self) -> None:
        """Create some files to store messages during the creation process."""
        with open(self.log_missing_translations, "w", encoding="utf-8") as file:
            file.writelines(
                "|no.  |Missing translations |\n" "| ------------- | ------------- |\n"
            )
        with open(self.log_missing_titles, "w", encoding="utf-8") as file:
            file.writelines(
                "|no.  |Missing titles |\n" "| ------------- | ------------- |\n"
            )
        with open(self.log_title_errors, "w", encoding="utf-8") as file:
            file.writelines(
                "|no.  |Errors in titles |\n" "| ------------- | ------------- |\n"
            )
        with open(self.log_xml_errors, "w", encoding="utf-8") as file:
            file.writelines("")
