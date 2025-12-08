#!/usr/bin/env python3

import json
import re

import requests
from bs4 import BeautifulSoup
from write_files import write_single_json_file


def update_trecanni(source: str) -> str:
    """Downloads the correct author and title date from the Dizionario Biografico.

    Args:
        source: The source to be updated

    Returns:
        str: Updated source
    """
    page = requests.get(source, timeout=10)
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find_all("h1", {"class": "title-search title-leaf"})[0].contents[0].split(", ")
    title[0] = title[0].title()
    title = ", ".join(title)
    author_string = (
        soup.find_all("div", {"class": "module-briciole_di_pane"})[0].contents[1].contents[0]
    )
    author_string = author_string.replace("\t", "").replace("\n", "")
    if mat := re.match(
        r"di (.*?) - Dizionario Biografico degli Italiani - Volume (.*?) \((.*)\)$",
        author_string,
    ):
        author, volume, year = mat.groups()
    else:
        raise ValueError(f"Can't parse Trecanni author string of {source}")
    author = author.split(" ")
    author = f"{author[-1]}, {' '.join(author[0:-1])}"
    final_source = (
        f"{author}, '{title}', in: Dizionario Biografico degli Italiani. "
        f"Volume {volume} (Rome, {year})"
        f", found on: {source}"
    )

    return final_source


def update_parlement(source: str) -> str:
    """Downloads the correct birth date/place and death date/place from parlement.com.

    Args:
        source: The source of the person to be update

    Returns:
        str: Updated source
    """
    page = requests.get(source, timeout=10)
    soup = BeautifulSoup(page.content, "html.parser")
    name = soup.find_all("div", {"class": "partext_c"})[0].contents[1].contents[0]
    final_source = f"Redactie parlement.com, '{name}', found on: {source}"

    return final_source


def check_sources_entry(
    sources: list[str],
    compiled_source_patterns: list[re.Pattern[str]],
    used_patterns: set[re.Pattern[str]],
    identifier: str,
    count_todo: int,
    probably_wrong: list[str],
    update: bool = False,
) -> tuple[list[str], set[re.Pattern[str]], int, list[str]]:
    """Check the individuals sources of an entry."""
    for index, source in enumerate(sources):
        # Empty
        if source == "":
            pass

        # Websites
        elif update and re.match(r"https://www.treccani.it/.*Dizionario-Biografico\)", source):
            sources[index] = update_trecanni(source)
        elif update and re.match(r"https://www\.parlement.com/.*", source):
            sources[index] = update_parlement(source)

        # Authors
        elif mat := re.match(r"\$Beth, (.*)", source):
            sources[index] = (
                f"Beth, J.C., De archieven van het Departement van Buitenlandsche Zaken (The Hague, 1918), {mat.groups()[0]}"  # noqa: E501
            )
        elif re.match(r"\$Lohrli", source):
            sources[index] = (
                "Lohrli, Anne, 'The Madiai: A Forgotten Chapter of Church History', Victorian Studies 33 (1989), 29–50"  # noqa: E501
            )
        elif mat := re.match(r"\$Moroni, (\d*), (.*)", source):
            sources[index] = (
                f"Moroni, G., Dizionario di erudizione storico-ecclesiastica da S. Pietro sino ai nostri giorni. Volume {mat.groups()[0]} (Rome, 1840), {mat.groups()[1]}"  # noqa: E501
            )
        elif mat := re.match(r"\$Moscati, (.*)", source):
            sources[index] = (
                f"Moscati, Ruggero, Le scritture della segreteria di Stato degli Affari Esteri del Regno di Sardegna (Rome, 1947), {mat.groups()[0]}"  # noqa: E501
            )
        elif mat := re.match(r"\$Santen, (.*)", source):
            sources[index] = (
                f"van Santen, Cornelis Willem, Het internationale recht in Nederlands buitenlands beleid: een onderzoek in het archief van het Ministerie van Buitenlandse Zaken (The Hague, 1955), {mat.groups()[0]}"  # noqa: E501
            )
        elif mat := re.match(r"\$Schmidt-Brentano, (.*)", source):
            sources[index] = (
                f"Schmidt-Brentano, Antonio, Die k. k. bzw. k. u. k. Generalität 1816-1918 (Vienna 2007), {mat.groups()[0]}"  # noqa: E501
            )
        elif re.match(r"\$Sträter", source):
            sources[index] = (
                "Sträter, F., Herinneringen aan de Eerwaarde Paters Leo, Clemens en Wilhelm Wilde, priesters der Sociëteit van Jezus (Nijmegen, 1911)"  # noqa: E501
            )
        elif mat := re.match(r"\$Wels, (.*)", source):
            sources[index] = (
                f"Wels, Cornelis Boudewijn, Bescheiden betreffende de buitenlandse politiek van Nederland, 1848-1919. Volume 1 (The Hague, 1972), {mat.groups()[0]}"  # noqa: E501
            )

        elif match := [i for i in compiled_source_patterns if i.match(source)]:
            used_patterns.add(match[0])

        # TODO: Sources to discuss
        elif source.startswith("https://notes9.senato.it/"):
            pass
        elif source.startswith("https://storia.camera.it/presidenti/"):
            pass
        elif source.startswith("https://storia.camera.it/deputato/"):
            pass
        elif source.startswith("https://www.britannica.com/biography/"):
            pass

        # TODO: Sources to look up
        elif source.startswith("Dizionario bibliografico dell'Armata Sarda seimila biografie"):
            pass

        # If not known/missing
        else:
            count_todo += 1
            if not source.startswith("http"):
                probably_wrong.append(source)
            print(count_todo, identifier)
            print("", source)

    return sources, used_patterns, count_todo, probably_wrong


def check_all_sources(
    filename: str,
) -> None:
    """Check and update all sources for given database.

    Args:
        filename: File name of initial database
    """
    with open(filename, encoding="utf-8") as file:
        persons = json.load(file)
    del persons["$schema"]

    source_patterns = []
    with open("inputs/SourcePatterns.json", encoding="utf-8") as file:
        source_types = json.load(file)
        for sources in source_types.values():
            source_patterns += sources

    count_todo = 0
    probably_wrong: list[str] = []
    compiled_source_patterns = [re.compile(f"{i}$") for i in source_patterns]
    used_patterns: set[re.Pattern[str]] = set()

    for identifier, data in persons.items():
        (
            data["sources"],
            used_patterns,
            count_todo,
            probably_wrong,
        ) = check_sources_entry(
            data["sources"],
            compiled_source_patterns,
            used_patterns,
            identifier,
            count_todo,
            probably_wrong,
        )

    persons["$schema"] = "../static/JSON/Individuals.json"

    # Write new file if this file itself is run
    if __name__ == "__main__":
        write_single_json_file(persons, "outputs", "Individuals.json")
    if probably_wrong:
        print("\nThese sources might be wrong")
        print("They have not been added to the list in python/json_check_sources.py")
        print(r"However, that list is awful anyway and is in dire need of updating :')")
        for i in probably_wrong:
            print("", i)
    if unused_patterns := [i for i in compiled_source_patterns if i not in used_patterns]:
        print(f"Found the following unused source patterns:\n {unused_patterns}")
    print(f"Finished checking sources in {filename}!\n")


if __name__ == "__main__":
    check_all_sources("inputs/Individuals.json")
