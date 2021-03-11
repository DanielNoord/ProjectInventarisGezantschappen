import json
import re
import requests
from bs4 import BeautifulSoup


def update_trecanni(filename):
    """Downloads the correct author and title date from the Dizionario Biografico

    Args:
        filename (str): File name of the original database

    Returns:
        dict: Updated individuals dictionary
    """
    with open(filename) as file:
        persons = json.load(file)
    del persons["$schema"]

    for _, data in persons.items():
        for index, source in enumerate(data["sources"]):
            if re.match(r"https://www.treccani.it/.*Dizionario-Biografico\)", source):
                page = requests.get(source)
                soup = BeautifulSoup(page.content, "html.parser")
                title = (
                    soup.find_all("h1", {"class": "title-search title-leaf"})[0]
                    .contents[0]
                    .title()
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

                data["sources"][index] = final_source
                print(f"New source:\n   {final_source}")
    return persons


if __name__ == "__main__":
    update_trecanni("inputs/Individuals.json")
