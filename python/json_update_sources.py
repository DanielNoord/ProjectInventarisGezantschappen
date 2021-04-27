import json
import re

import requests
from bs4 import BeautifulSoup

SOURCE_PATTERNS = {}


def update_trecanni(source):
    """Downloads the correct author and title date from the Dizionario Biografico

    Args:
        source (str): The source to be updated

    Returns:
        str: Updated source
    """
    page = requests.get(source)
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find_all("h1", {"class": "title-search title-leaf"})[0].contents[0].split(", ")
    title[0] = title[0].title()
    title = ", ".join(title)
    author_string = (
        soup.find_all("div", {"class": "module-briciole_di_pane"})[0].contents[1].contents[0]
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
    # print(f"New source:\n   {final_source}")
    return final_source


def update_parlement(source):
    """Downloads the correct birth date/place and death date/place from parlement.com

    Args:
        source (str): The source of the person to be update

    Returns:
        str: Updated source
    """
    page = requests.get(source)
    soup = BeautifulSoup(page.content, "html.parser")
    name = soup.find_all("div", {"class": "partext_c"})[0].contents[1].contents[0]
    final_source = f"Redactie parlement.com, '{name}', found on: {source}"
    # print(f"New source:\n   {final_source}")
    return final_source


def update_all_sources(filename):
    """Updates all sources for given database

    Args:
        filename (str): File name of initial database
    """
    with open(filename) as file:
        persons = json.load(file)
    del persons["$schema"]
    count_todo = 0

    for identifier, data in persons.items():
        for index, source in enumerate(data["sources"]):
            # Websites
            if re.match(r"https://www.treccani.it/.*Dizionario-Biografico\)", source):
                persons[identifier]["sources"][index] = update_trecanni(source)
            elif re.match(r"https://www.parlement.com/.*", source):
                persons[identifier]["sources"][index] = update_parlement(source)

            # Biographical dictionaries
            elif re.match(
                r"(.*?, .*?, )?'.*', in: P.J. Blok and P.C. Molhuysen, Nieuw Nederlandsch biografisch woordenboek. Deel \d*? \(Leiden, 19\d\d\)",  # pylint: disable=line-too-long
                source,
            ):
                pass
            elif re.match(
                r"'.*', in: A.J. van der AA, Biographisch woordenboek der Nederlanden. \d*? \(Haarlem, 18\d\d\)",  # pylint: disable=line-too-long
                source,
            ):
                pass
            elif re.match(
                r"Mersch, Jules, Biographie nationale du pays de Luxembourg depuis ses origines jusqu'à nos jours. Fascicule \d\d \(Luxemburg, 19\d\d\),( \d*,)* \d*? (and \d*)?",  # pylint: disable=line-too-long
                source,
            ):
                pass
            elif re.match(
                r"'.*' in: Mullié, Charles, Biographie des célébrités militaires des armées de terre et de mer de 1789 à 1850 \(Parijs, 1852\)",  # pylint: disable=line-too-long
                source,
            ):
                pass
            elif re.match(
                r"Dutch Institute for Art History \(RKD\), '.*', found on: https://rkd.nl/explore/artists/\d*",  # pylint: disable=line-too-long
                source,
            ):
                pass
            elif re.match(
                r"'.*' in: von Zedlitz-Neukirch, Leopold, Neues Preussisches Adels-Lexicon. Dritter Band I-O \(Leipzig, 18\d\d\), \d*",  # pylint: disable=line-too-long
                source,
            ):
                pass

            # State almanac/calendar
            elif re.match(
                r"Ministero dell'interno, Calendario generale del Regno di Sardegna, \(Turin, 18\d\d\), \d*",  # pylint: disable=line-too-long
                source,
            ):
                pass
            elif re.match(
                r"Ministero dell'interno, Calendario generale del Regno d'Italia, \(Turin, 18\d\d\), \d*",  # pylint: disable=line-too-long
                source,
            ):
                pass
            elif re.match(
                r"Ministero dell'interno, Calendario generale pe' regii stati, \(Turin, 18\d\d\), \d*",  # pylint: disable=line-too-long
                source,
            ):
                pass
            elif re.match(
                r"Tipografia Giusti, Almanacco di Corte per l'anno 18\d\d \(Lucca, 18\d\d\), \d*",  # pylint: disable=line-too-long
                source,
            ):
                pass
            elif re.match(
                r"Tipografia della Rev. Cam. Apostolica, Notizie per l'anno 18\d\d \(Roma, 18\d\d\), \d*",  # pylint: disable=line-too-long
                source,
            ):
                pass
            elif re.match(
                r"Stamperia Chracas, Notizie per l'anno 18\d\d \(Roma, 18\d\d\), \d*",
                source,
            ):
                pass
            elif re.match(
                r"Belinfante, J., 's Gravenhaagsche Stads- en Residentie-almanak voor het jaar 18\d\d \('s Gravenhage, 18\d\d\), \d*",  # pylint: disable=line-too-long
                source,
            ):
                pass
            elif re.match(
                r"Stamperia Davico e Picco, Raccolta di regi editti, proclami, manifesti ed altri provvedimenti de' magistrati ed uffizi. Volume \d\d \(Turin, 18\d\d\), \d*",  # pylint: disable=line-too-long
                source,
            ):
                pass
            elif re.match(
                r"Staats-almanak voor den jare 18\d\d \(The Hague, 18\d\d\), 'd*",
                source,
            ):
                pass
            elif re.match(
                r"Staats- und Adress-Handbuch des Herzogthums Nassau für das Jahr 18\d\d \(Wiesbaden, 18\d\d\), \d*",  # pylint: disable=line-too-long
                source,
            ):
                pass
            elif re.match(
                r"Perthes, Justus, Almanach de Gotha. Annuaire diplomatique et statistique pour l'année 18\d\d \(Gotha, 18\d\d\), \d*",  # pylint: disable=line-too-long
                source,
            ):
                pass
            elif re.match(
                r"Handbuch über den Königlich Preußischen Hof und Staat für das Jahr 18\d\d \(Berlin, 18\d\d\), \d*",  # pylint: disable=line-too-long
                source,
            ):
                pass
            elif re.match(
                r"Casalis, Goffredo, Dizionario geografico-storico-statistico-commerciale degli stati di S.M. il Re di Sardegna, volume .* \(Turin, 18\d\d\), \d*",  # pylint: disable=line-too-long
                source,
            ):
                pass

            # Journals
            elif re.match(
                r"Osservatore del Trasimeno, Anno .*?, \d* \(Perugia, 18\d\d-\d\d-\d\d\), \d*",
                source,
            ):
                pass
            elif re.match(
                r"Gazzetta di Genova, Anno .*?, \d* \(Genoa, 18\d\d-\d\d-\d\d\), \d*",
                source,
            ):
                pass
            elif re.match(
                r"Gazzetta Piemontese, Anno .*?, \d* \(Turin, 18\d\d-\d\d-\d\d\), \d*",
                source,
            ):
                pass
            elif re.match(
                r"Nederlandsche Staatscourant 18\d\d, \d* \(The Hague, 18\d\d-\d\d-\d\d\)",
                source,
            ):
                pass
            elif re.match(
                r"Pilaar, J.C. and J.M. Obreen, Tijdschrift toegewijd aan het zeewezen. Tweede reeks. Derde deel \(Medemblik, 18\d\d\), \d*",  # pylint: disable=line-too-long
                source,
            ):
                pass
            elif re.match(
                r"Allgemeiner Polizei-Anzeiger, Jahr .*?, \d* \(Gotha, 18\d\d-\d\d-\d\d\), \d*",
                source,
            ):
                pass

            # Books
            elif re.match(
                r"Crisafulli, Vincenzo, Studi sull'apostolica sicola legazia, volume 1 \(Palermo, 1850\)",  # pylint: disable=line-too-long
                source,
            ):
                pass
            elif re.match(
                r"Cormier, Hyacinthe Marie, La vita del reverendissimo padre fr. Alessandro Vincenzo Jandel, LXXIII maestro generale dei Frati Predicatori \(Rome, 1896\)",  # pylint: disable=line-too-long
                source,
            ):
                pass

            # Authors
            elif mat := re.match(r"\$Moscati, (.*)", source):
                persons[identifier]["sources"][
                    index
                ] = f"Moscati, Ruggero, Le scritture della segreteria di Stato degli Affari Esteri del Regno di Sardegna (Rome, 1947), {mat.groups()[0]}"  # pylint: disable=line-too-long
            elif mat := re.match(r"\$Beth, (.*)", source):
                persons[identifier]["sources"][
                    index
                ] = f"Beth, J.C., De archieven van het Departement van Buitenlandsche Zaken (Den Haag, 1918), {mat.groups()[0]}"  # pylint: disable=line-too-long
            elif mat := re.match(r"\$Wels, (.*)", source):
                persons[identifier]["sources"][
                    index
                ] = f"Wels, Cornelis Boudewijn, Bescheiden betreffende de buitenlandse politiek van Nederland, 1848-1919 vol. 1 (Den Haag, 1972), {mat.groups()[0]}"  # pylint: disable=line-too-long
            elif mat := re.match(r"\$Santen, (.*)", source):
                persons[identifier]["sources"][
                    index
                ] = f"van Santen, Cornelis Willem, Het internationale recht in Nederlands buitenlands beleid: (een onderzoek in het Archief van het Ministerie van Buitenlandse Zaken) (Den Haag, 1955), {mat.groups()[0]}"  # pylint: disable=line-too-long
            elif mat := re.match(r"\$Lohrli", source):
                persons[identifier]["sources"][
                    index
                ] = "Lohrli, Anne, ‘The Madiai: A Forgotten Chapter of Church History’, Victorian Studies 33 (1989), 29–50"  # pylint: disable=line-too-long
            elif source.startswith("Bountry, Philippe, Souverain et pontife: Recherches"):
                pass

            # Empty
            elif source == "":
                pass

            # If not known/missing
            else:
                count_todo += 1
                print(count_todo, filename, source)
                pass

    persons["$schema"] = "../static/JSON/Individuals.json"

    with open("outputs/Individuals.json", "w", encoding="utf-8") as file:
        json.dump(persons, file, ensure_ascii=False, indent=4)
    print("Wrote file to outputs/Individuals.json")


if __name__ == "__main__":
    update_all_sources("inputs/Individuals.json")
