def control_title(title: str, file_name: str) -> None:
    """Control document titles for common errors"""
    with open("outputs/title_errors", "a", encoding="utf-8") as file:
        if title.count('"') % 2:
            print(f"|{file_name}|Uneven amount of quotes for {title}", file=file)
        if title.count("_") % 2:
            print(
                f"|{file_name}|Uneven amount of italics indications for {title}",
                file=file,
            )
        if title.count("(") != title.count(")"):
            print(
                f"|{file_name}|Uneven amount of braces '(' and ')' for {title}",
                file=file,
            )
        assert not title.count("$"), f"Incorrect title: {title}"
        assert not title.count('"'), f"Incorrect title: {title}"
        assert not title.count("‘"), f"Incorrect title: {title}"
        assert not title.count("’"), f"Incorrect title: {title}"
