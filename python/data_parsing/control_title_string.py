from lxml import etree


def control_title(title: str, parent_element: etree._Element) -> None:
    """Control titles for common errors"""
    # pylint: disable=line-too-long
    with open("outputs/title_errors", "a", encoding="utf-8") as file:
        if title.count('"') % 2:
            vol = parent_element.getparent().getparent().getchildren()[0].getchildren()[0].text  # type: ignore
            print(f"|{vol}|Uneven amount of quotes for {title}", file=file)
        if title.count("_") % 2:
            vol = parent_element.getparent().getparent().getchildren()[0].getchildren()[0].text  # type: ignore
            print(f"|{vol}|Uneven amount of italics indications for {title}", file=file)
        if title.count("(") != title.count(")"):
            vol = parent_element.getparent().getparent().getchildren()[0].getchildren()[0].text  # type: ignore
            print(f"|{vol}|Uneven amount of braces '(' and ')' for {title}", file=file)
