import json
import re
import requests
from bs4 import BeautifulSoup


def update_trecanni(source):
    """Downloads the correct author and title date from the Dizionario Biografico

    Args:
        persons (str): The source to be updated

    Returns:
        str: Updated source
    """
    page = requests.get(source)
    soup = BeautifulSoup(page.content, "html.parser")
    title = (
        soup.find_all("h1", {"class": "title-search title-leaf"})[0].contents[0].title()
    )
    author_string = (
        soup.find_all("div", {"class": "module-briciole_di_pane"})[0]
        .contents[1]
        .contents[0]
    )
    author_string = author_string.replace("\t", "").replace("\n", "")
    author, volume, year = re.match(
        r"di (.*?) - Dizionario Biografico degli Italiani - Volume (.*?) \((.*)\)$",
        author_string,
    ).groups()
    final_source = (
        f"{author}, '{title}', in: Dizionario Biografico degli Italiani "
        f"vol. {volume} (Rome, Trecanni, {year})"
    )
    print(f"New source:\n   {final_source}")
    return final_source


def update_parlement(source):
    """Downloads the correct birth date/place and death date/place from parlement.com

    Args:
        persons (str): The source of the person to be update

    Returns:
        str: Data related to birth
        str: Data related to death
    """
    page = requests.get(source)
    soup = BeautifulSoup(page.content, "html.parser")
    personalia = soup.find_all("div", {"class": "partext_c"})[2].text.split("\n")
    data1 = personalia[personalia.index("geboorteplaats en -datum") + 1]
    data2 = personalia[personalia.index("overlijdensplaats en -datum") + 1]
    print(f"Found birth data {data1}, found death data {data2}.")
    return data1, data2


def update_all_sources(filename):
    """Updates all sources for given database

    Args:
        filename (str): File name of initial database
    """
    with open(filename) as file:
        persons = json.load(file)
    del persons["$schema"]

    for identifier, data in persons.items():
        for index, source in enumerate(data["sources"]):
            if re.match(r"https://www.treccani.it/.*Dizionario-Biografico\)", source):
                persons[identifier]["sources"][index] = update_trecanni(source)
            if re.match(r"https://www.parlement.com/.*", source):
                pass
                # (persons[identifier]["date_of_birth"],
                # #persons[identifier]["date_of_death"]) = update_parlement(source)
    persons["$schema"] = "../static/JSON/Individuals.json"

    with open("outputs/Individuals.json", "w", encoding="utf-8") as file:
        json.dump(persons, file, ensure_ascii=False, indent=4)
    print("Wrote file to outputs/Individuals.json")


if __name__ == "__main__":
    update_all_sources("inputs/Individuals.json")
