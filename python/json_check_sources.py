import json
import re

import requests
from bs4 import BeautifulSoup

SOURCE_PATTERNS = {
    # Biographical dictionaries
    r".*, .*, '.*', in: Allgemeine Deutsche Biographie. Band \d* \(Leipzig, 1\d\d\d\)",
    r".*, .*, '.*', in: Digitaal Vrouwenlexicon van Nederland \(2014\)",
    r"(.*, )?.*, '.*', in: Dizionario Biografico degli Italiani. Volume \d* \(Rome, \d\d\d\d\), found on: https://www.treccani.it/.*Dizionario-Biografico\)",  # pylint: disable=line-too-long
    r".*, .*, '.*', in: Dizionario storico biografico della Tuscia \(2014-\), found on https://www.gentedituscia.it/.*/",  # pylint: disable=line-too-long
    r".*, .*, '.*', in: Historisches Lexikon der Schweiz \(20\d\d\), found on https://hls-dhs-dss.ch/it/articles/\d*/20\d\d-\d\d-\d\d/",  # pylint: disable=line-too-long
    r".*, .*, '.*', in: Jules Mersch, Biographie nationale du pays de Luxembourg depuis ses origines jusqu'à nos jours. Fascicule \d* \(Luxemburg, 19\d\d\)",  # pylint: disable=line-too-long
    r".*, .*, '.*', in: Neue Deutsche Biographie. Band \d* \(Berlin, \d\d\d\d\)",
    r".*, .*, '.*', in: P.J. Blok and K.H. Kossmann, Nieuw Nederlandsch biografisch woordenboek. Deel \d* \(Leiden, 19\d\d\)",  # pylint: disable=line-too-long
    r".*, .*, '.*', in: P.J. Blok and P.C. Molhuysen, Nieuw Nederlandsch biografisch woordenboek. Deel \d* \(Leiden, 19\d\d\)",  # pylint: disable=line-too-long
    r".*, .*, '.*', in: P.J. Blok, P.C. Molhuysen and K.H. Kossmann, Nieuw Nederlandsch biografisch woordenboek. Deel \d* \(Leiden, 19\d\d\)",  # pylint: disable=line-too-long
    r".*, .*, '.*', in: The Catholic Encyclopedia. Volume \d* \(New York, 19\d\d\)",
    r".*, .*, '.*', in: Traugott Bautz \(ed.\), Biographisch-Bibliographisches Kirchenlexikon. Band \d* \(Herzberg, \d\d\d\d\)",  # pylint: disable=line-too-long
    r".*, .*, '.*', in: Repertorium van ambtsdragers en ambtenaren 1428-1861, found on: http://resources.huygens.knaw.nl/repertoriumambtsdragersambtenaren1428-1861",  # pylint: disable=line-too-long
    r".*, .*, '.*', in: Società di Studi Valdesi, Il Dizionario Biografico on-line dei Protestanti in Italia \(2021\)",  # pylint: disable=line-too-long
    r"'.*', in: A.J. van der AA, Biographisch woordenboek der Nederlanden. .* \(Haarlem, 18\d\d\)",
    r"'.*', in: Charles Mullié, Biographie des célébrités militaires des armées de terre et de mer de 1789 à 1850 \(Paris, 1852\)",  # pylint: disable=line-too-long
    r"'.*', in: Constantin von Wurzbach, Biographisches Lexikon des Kaiserthums Oesterreich. \d*. Teil \(Vienna, 18\d\d\)",  # pylint: disable=line-too-long
    r"'.*', in: Database of the Office of the Historian, found on https://history.state.gov/departmenthistory/people/.*",  # pylint: disable=line-too-long
    r"'.*', in: Hessische Biografie, found on https://www.lagis-hessen.de/pnd/.*",
    r"'.*', in: Index Catalogue of the Library of the Surgeon-general's Office United States Army, volume 15 \(Washington, 1894\)",  # pylint: disable=line-too-long
    r"'.*', in: Leopold von Zedlitz-Neukirch, Neues Preussisches Adels-Lexicon. Dritter Band I-O \(Leipzig, 18\d\d\), \d*",  # pylint: disable=line-too-long
    r"'.*', in: Österreichisches Biographisches Lexikon 1815–1950. Band \d* \(Vienna, 1957\)",
    r"'.*', in: Pierre Larousse, Grand dictionnaire universel du XIXe siècle. \d* \(Paris, 18\d\d\)",  # pylint: disable=line-too-long
    r"'.*', in: Wikisource Database \(2\d\d\d-\d\d-\d\d\), found on: https://it.wikisource.org/wiki/.*",  # pylint: disable=line-too-long
    r"Dutch Institute for Art History \(RKD\), '.*', found on: https://rkd.nl/explore/artists/\d*",
    r"Fait, Riccardo \(red.\), Biografie dei consiglieri comunali di Roma \(Rome, 1873\), \d*(-\d*)?",  # pylint: disable=line-too-long
    r"Mersch, Jules, Biographie nationale du pays de Luxembourg depuis ses origines jusqu'à nos jours. Fascicule \d\d \(Luxemburg, 19\d\d\),( \d*,)* \d*?( and \d*)?",  # pylint: disable=line-too-long
    r"Moroni, G., Dizionario di erudizione storico-ecclesiastica da S. Pietro sino ai nostri giorni. Volume \d* \(Rome, 1840\), \d*( and \d*)?",  # pylint: disable=line-too-long
    r"Redactie parlement.com, '.*', found on: https://www.parlement.com/.*",  # pylint: disable=line-too-long
    # State almanac/calendar
    r"Almanacco imperiale reale per le provincie del Regno Lombardo-Veneto soggette al governo di Milano per l'anno bisestile 18\d\d \(Milan, 18\d\d\), \d*",  # pylint: disable=line-too-long
    r"Almanacco reale del Regno delle Due Sicilie per l'anno 18\d\d \(Naples, 18\d\d\), \d*",
    r"Almanacco Romano pel 18\d\d. Raccolta dei primari dignitari e funzionari della citta' di Roma, Anno \d* \(Rome, 18\d\d\), \d*",  # pylint: disable=line-too-long
    r"Annuario del Ministero delle finanze del Regno d'Italia, Anno \d* \(Turin, 18\d\d\), \d*",
    r"Belinfante, J., 's Gravenhaagsche Stads- en Residentie-almanak voor het jaar 18\d\d \('s Gravenhage, 18\d\d\), \d*",  # pylint: disable=line-too-long
    r"Calendario generale della città, diocesi, e provincia di Ancona per l'anno 18\d\d \(Ancona, 18\d\d\), \d*",  # pylint: disable=line-too-long
    r"Casalis, Goffredo, Dizionario geografico-storico-statistico-commerciale degli stati di S.M. il Re di Sardegna, volume .* \(Turin, 18\d\d\), \d*",  # pylint: disable=line-too-long
    r"Eene Vereniging van Letterkundigen, Onze tijd: merkwaardige gebeurtenissen onzer dagen. Serie \d*. Deel \d* \(Amsterdam, 18\d\d\), \d*",  # pylint: disable=line-too-long
    r"Fontana, Allesandro, Il Palmaverde: calendario storico-statistico-amministrativo, \(Turin, 18\d\d\), \d*",  # pylint: disable=line-too-long
    r"Governo di Malta, Repertorio di proclami, ordinanze, notificazioni ecc. dall ottobre 1813 a giugno 1842, Volume 1 A-M \(Malta, 18\d\d\), \d*",  # pylint: disable=line-too-long
    r"Handbuch über den Königlich Preußischen Hof und Staat für das Jahr 18\d\d \(Berlin, 18\d\d\), \d*",  # pylint: disable=line-too-long
    r"Manuale del regno lombardo-veneto per l'anno 18\d\d, \(Milan, 18\d\d\), \d*",
    r"Ministero dell'interno, Calendario generale del Regno di Sardegna, \(Turin, 18\d\d\), \d*",
    r"Ministero dell'interno, Calendario generale del Regno d'Italia, \(Turin, 18\d\d\), \d*",
    r"Ministero dell'interno, Calendario generale pe' regii stati, \(Turin, 18\d\d\), \d*",
    r"Palmaverde almanacco piemontese per l'anno 18\d\d \(Turin, 18\d\d\), \d*",  # pylint: disable=line-too-long
    r"Perthes, Justus, Almanach de Gotha. Annuaire diplomatique et statistique pour l'année 18\d\d \(Gotha, 18\d\d\), \d*",  # pylint: disable=line-too-long
    r"Perthes, Justus, Gothaischer Genealogisches Taschenbuch der deutschen gräflichen Häuser auf das Jahr 18\d\d \(Gotha, 18\d\d\), \d*",  # pylint: disable=line-too-long
    r"Società di Agricoltura Jesina. Annali ed Atti, volume \d* \(Rome, 18\d\d\), \d*",
    r"Staats-almanak voor den jare 18\d\d \(The Hague, 18\d\d\), \d*",
    r"Staats- und Adress-Handbuch des Herzogthums Nassau für das Jahr 18\d\d \(Wiesbaden, 18\d\d\), \d*",  # pylint: disable=line-too-long
    r"Stamperia Chracas, Notizie per l'anno 18\d\d \(Roma, 18\d\d\), \d*",
    r"Stamperia Davico e Picco, Raccolta di regi editti, proclami, manifesti ed altri provvedimenti de' magistrati ed uffizi. Volume \d\d \(Turin, 18\d\d\), \d*",  # pylint: disable=line-too-long
    r"Tipografia Giusti, Almanacco di Corte per l'anno 18\d\d \(Lucca, 18\d\d\), \d*",
    r"Tipografia della Rev. Cam. Apostolica, Notizie per l'anno 18\d\d \(Roma, 18\d\d\), \d*",
    r"Wegwyzer der stad Gent en provinciale almanach van Oost-Vlaenderen voor het jaer des zaligmakers 18\d\d, volume \d* \(Gent, 18\d\d\), \d*",  # pylint: disable=line-too-long
    # Journals
    r".*, .*, '.*', in: Annales valaisannes: bulletin trimestriel de la Société d'histoire du Valais romand, \d* \(19\d\d\), \d*-\d*",  # pylint: disable=line-too-long
    r".*, .*, '.*', in: Historisch Voorburg, \d*, \d* \(\d\d\d\d\)(, \d*)?",
    r".*, .*, '.*', in: Jaarboek van de Maatschappij der Nederlandse Letterkunde, 18\d\d \(Amsterdam, 18\d\d\), \d*-\d*",  # pylint: disable=line-too-long
    r"Allgemeiner Polizei-Anzeiger, Jahr .*, \d* \(Gotha, 18\d\d-\d\d-\d\d\), \d*",
    r"Bureaux de l'agence générale pour la défense de la liberté religieuse, Premier bulletin de l'agence générale pour la défense de la liberté religieuse \(Paris, 18\d\d-\d\d-\d\d\), \d*",  # pylint: disable=line-too-long
    r"De Nederlandsche Leeuw, \d*, \d* \(1\d\d\d-\d\d\), \d*",
    r"Gaceta de Madrid, N. \d* \(Madrid, 18\d\d-\d\d-\d\d\)",
    r"Gazzetta di Genova, Anno .*, \d* \(Genoa, 18\d\d-\d\d-\d\d\), \d*",
    r"Gazzetta Piemontese, Anno .*, \d* \(Turin, 18\d\d-\d\d-\d\d\), \d*",
    r"Gazzetta Ufficiale del Regno d'Italia, Anno 18\d\d, \d* \(Florence, 18\d\d-\d\d-\d\d\)",
    r"Gazzetta Ufficiale di Roma, Anno .*, \d* \(Rome, 18\d\d-\d\d-\d\d\), \d*",
    r"La Civiltà Cattolica, Anno \d*, .* \(Rome, 18\d\d\), \d*",
    r"Il Fanfulla, Anno \d*, .* \(Rome, 18\d\d\), \d*",
    r"Lohrli, Anne, ‘The Madiai: A Forgotten Chapter of Church History’, Victorian Studies 33 \(1989\), 29–50",  # pylint: disable=line-too-long
    r"Middelburgsche courant, \d* \(Middelburg, \d\d\d\d-\d\d-\d\d\), \d*",
    r"Nederlandsche Staatscourant 18\d\d, \d* \(The Hague, 18\d\d-\d\d-\d\d\)",
    r"'Notizie raccolte dagli amici della verità e della giustizia ed autenticate dalla generale cognizione dei romani, a confutazione dell'articolo inserito a modo di bando per corrispondenza di Roma nel diario L'Unità Cattolica del 15 giugno 1869.*",  # pylint: disable=line-too-long
    r"Osservatore del Trasimeno, Anno .*, \d* \(Perugia, 18\d\d-\d\d-\d\d\), \d*",
    r"Pavone, Claudio, Alcuni aspetti dei primi mesi di governo italiano a Roma e nel Lazio \(Continuazione e fine\), Archivio Storico Italiano 116 \(1958\), 346–380, 349",  # pylint: disable=line-too-long
    r"Pilaar, J.C. and J.M. Obreen, Tijdschrift toegewijd aan het zeewezen. Tweede reeks. Derde deel \(Medemblik, 18\d\d\), \d*",  # pylint: disable=line-too-long
    # Books
    r"Archivum Historiae Pontificiae, volume \d* \(Rome, 19\d\d\), \d*",
    r"Assereto, Giovanni, «Per la comune salvezza dal morbo contagioso». I controlli di sanità nella Repubblica di Genova \(Genoa, 2007\), 176",  # pylint: disable=line-too-long
    r"Avetta, M. and Società per la storia del Risorgimento italiano, Dall'archivio di un diplomatico: Il barone Marco Antonio Alessandro Jocteau \(Casale, 1924\)",  # pylint: disable=line-too-long
    r"Barclay, David E., ‘Hof und Hofgesellschaft in Preußen in der Zeit Friedrich Wilhelms IV. \(1840 bis 1857\). Überlegungen und Fragen’, in: Karl Möckl ed., Hof und Hofgesellschaft in den deutschen Staaten im 19. und beginnenden 20. Jahrhundert \(Berlin, Boston, 1990\), \d*",  # pylint: disable=line-too-long
    r"Beth, J.C., De archieven van het Departement van Buitenlandsche Zaken \(Den Haag, 1918\), \d*",  # pylint: disable=line-too-long
    r"Bountry, Philippe, Souverain et pontife: Recherches prosopographiques sur la Curie Romaine à l’âge de la Restauration \(1814-1846\) \(Rome, 2002\), \d*",  # pylint: disable=line-too-long
    r"Croce, Giuseppe Maria, Vincenzo Tizzani. Effemeridi Romane. Volume 1 \(Rome, 2015\), \d*",  # pylint: disable=line-too-long
    r"De Boni, Filippo, La Congiura di Roma e Pio IX. Ricordi di Filippo de Boni \(Losanna, 1848\), \d*",  # pylint: disable=line-too-long
    r"Bringmann, Tobias C., Handbuch der Diplomatie 1815-1963 \(Berlin, 2012\), \d*",
    r"Capitelli, G. and S. Cracolici, Roma en Mexico – Mexico en Roma. Las academias de arte entre Europa y el Nuevo Mundo, 1843-1867 \(Rome, 2018\)",  # pylint: disable=line-too-long
    r"du Chastel de la Howarderie, Paul-Armand, Les Toparques héréditaires des deux Howardries, ou crayon généalogique de la maison comtale du Chastel de la Howardries \(Péruwelz, 1840\), \d*",  # pylint: disable=line-too-long
    r"Cormier, Hyacinthe Marie, La vita del reverendissimo padre fr. Alessandro Vincenzo Jandel, LXXIII maestro generale dei Frati Predicatori \(Rome, 1896\)",  # pylint: disable=line-too-long
    r"Cozzo, Paolo, Andrea Merlotti and Andrea Nicolotti, The Shroud at Court: History, Usages, Places and Images of a Dynastic Relic \(Leiden, 2019\), \d*",  # pylint: disable=line-too-long
    r"Crisafulli, Vincenzo, Studi sull'apostolica sicola legazia, volume 1 \(Palermo, 1850\)",
    r"van Dommelen, G.F., Geschiedenis der militaire geneeskundige dienst in Nederland, met inbegrip van die zijner zeemagt en overzeesche bezittingen, van af den vroegsten tijd tot op heden \(Zutphen, 1857\), .*",  # pylint: disable=line-too-long
    r"Douma, Klaasje, De adel in Noord-Brabant, 1814-1918: groepsvorming, adellijke levensstijl en regionale identiteit \(Tilburg, 2015\)",  # pylint: disable=line-too-long
    r"Foreign Office, British and Foreign State Papers. 1833-1834, volume 22 \(London, 1847\), \d*",
    r"Frezza, Filippo, Dei camerieri segreti e d’onore del Sommo Pontefice: memorie storiche \(Rome, 1884\), 56",  # pylint: disable=line-too-long
    r"Iacobini, Franco, Terrae Cinthiani, Storia di Genzano e della nobile Famiglia Iacobini \(Rome, 2003\)",  # pylint: disable=line-too-long
    r"Kallenberg, Lodewijk, Pieter Otto van der Chijs \(1802-1867\), zandgraf 242, vak F, \(Leiden, 2020\), found on https://www.begraafplaatsgroenesteeg.nl/N_B_personen/Artikel%20Van%20der%20Chijs.pdf",  # pylint: disable=line-too-long
    r"Lencisa, G.F., Ragionamento sulla rinnovazione del trattato di commercio e di navigazione conchiuso tra il Piemonte e la Francia nell'anno 1843, e della Convenzione speciale sulla proprietà letteraria annessa a quel trattato medesimo \(Turin, 1851\)",  # pylint: disable=line-too-long
    r"Martina, G., Pio IX \(1846-1850\) \(Rome, 1974\), \d*",
    r"van der Meulen, M.E., Mijne Reis door Zwitserland naar de Waldenzen in Piemont’s Valleijen \(London, 1852\)",  # pylint: disable=line-too-long
    r"Mori, Renato, Le scritture della legazione e del consolato del Granducato di Toscana in Roma dal 1737 al 1859 \(Rome, 1959\)",  # pylint: disable=line-too-long
    r"Moscati, Ruggero, Le scritture della segreteria di Stato degli Affari Esteri del Regno di Sardegna \(Rome, 1947\), \d*",  # pylint: disable=line-too-long
    r"Nuyens, A., Gedenkboek der pauselijke Zouaven. 1867-1892 \(Roermond, 1892\)",
    r"Pirri S.J., P. Pietro, Pio IX e Vittorio Emanuele II dal loro carteggio privato \(Rome, 1980\), \d*( and \d*)?",  # pylint: disable=line-too-long
    r"Pohle, Frank, Alfred von Reumont \(1808–1887\) – Ein Diplomat als kultureller Mittler \(Berlin, 2015\)",  # pylint: disable=line-too-long
    r"de Régnon, M., Relation des événements qui ont précédé et suivi l'expulsion de 78 Anglais dits trappistes de Meilleraye \(Nantes, 1831\)",  # pylint: disable=line-too-long
    r"Ricci, Angelo Maria, Epistola Poetica a sua eccellenza reverendissima monsignor Achille Maria Ricci \(Rome, 1847\)",  # pylint: disable=line-too-long
    r"Sánchez, Elena Vázquez, Un historiador del derecho, Pedro José Pidal \(Madrid, 1998\)",
    r"van Santen, Cornelis Willem, Het internationale recht in Nederlands buitenlands beleid: een onderzoek in het archief van het Ministerie van Buitenlandse Zaken \(Den Haag, 1955\), \d*",  # pylint: disable=line-too-long
    r"Santoni, Pedro, and Will Fowler, Mexico, 1848-1853: Los Años Olvidados \(London, 2018\), \d*",
    r"Savini, Luigi, Al battaglione isolato della emerita guardia civica di cingoli ed appodiati \(Loreto, 1848\)",  # pylint: disable=line-too-long
    r"Schijf, Huibert, Netwerken van een financieel-economische elite \(Amsterdam, 1993\), \d*",
    r"Schutte, O., Repertorium der Nederlandse vertegenwoordigers residerende in het buitenland 1584-1810 \(The Hague, 1976\), \d*",  # pylint: disable=line-too-long
    r"Schmidt-Brentano, Antonio, Die k. k. bzw. k. u. k. Generalität 1816-1918 \(Vienna 2007\), \d*",  # pylint: disable=line-too-long
    r"De Sivo, Giacinto, Storia delle Due Sicilie, volume 2 \(Brindisi, 2013\)",
    r"Smith, Robert and Brenda Packman, Memoirs of Giambattista Scala: Consul of his Italian Majesty in Lagos in Guinea \(1862\) \(Oxford, 2000\)",  # pylint: disable=line-too-long
    r"Solaro della Margarita, Clemente, Memorandum storico politico del conte Clemente Solaro della Margarita \(Turin, 1852\)",  # pylint: disable=line-too-long
    r"Sträter, F., Herinneringen aan de Eerwaarde Paters Leo, Clemens en Wilhelm Wilde, priesters der Sociëteit van Jezus \(Nijmegen, 1911\)",  # pylint: disable=line-too-long
    r"Sunti delle Dissertazioni lette nell'Accademia Liturgica, volume 1 \(Rome, 1843\), \d*",
    r"Thewes, Guy, Les gouvernements du Grand-Duché de Luxembourg depuis 1848 \(Luxembourg, 2011\), \d*",  # pylint: disable=line-too-long
    r"van der Vijver, C., Geschiedkundige beschrijving der stad Amsterdam sedert hare wording tot op den tegenwoordige tijd, deel 3 \(Amsterdam, 1846\), \d*",  # pylint: disable=line-too-long
    r"Wels, Cornelis Boudewijn, Bescheiden betreffende de buitenlandse politiek van Nederland, 1848-1919. Volume 1 \(Den Haag, 1972\), \d*",  # pylint: disable=line-too-long
    # Archives
    r"KADOC, Leuven, Archief van de Nederlandse jezuïeten",
    r"Koninklijke Verzamelingen, The Hague, Archive: Thesaurie, inventory number E08-II-\d\d",
    r"Nationaal Archief, The Hague, Collectie Van Aerssen van Voshol, 1.10.01",
    r"Nationaal Archief, The Hague, Gezantschap Italië, 2.05.26",
    r"Stadsarchief Amsterdam, Amsterdam, inventory number: \d*",
    r"Stadsarchief Rotterdam, Rotterdam, inventory number: \d*, documents: \d*-\d*",
    r"Stadsarchief Utrecht, Utrecht, inventory number: \d*, documents: \d*.\d*.\d*",
}


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
    author = author.split(" ")
    author = f"{author[-1]}, {' '.join(author[0:-1])}"
    final_source = (
        f"{author}, '{title}', in: Dizionario Biografico degli Italiani "
        f"vol. {volume} (Rome, {year})"
        f", found on: {source}"
    )

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

    return final_source


def check_all_sources(filename):
    """Check and update all sources for given database

    Args:
        filename (str): File name of initial database
    """
    with open(filename) as file:
        persons = json.load(file)
    del persons["$schema"]
    count_todo = 0
    probably_wrong = []
    compiled_source_patterns = [re.compile(i) for i in SOURCE_PATTERNS]
    used_patterns = set()

    for identifier, data in persons.items():
        for index, source in enumerate(data["sources"]):
            # Empty
            if source == "":
                pass

            # Websites
            elif re.match(r"https://www.treccani.it/.*Dizionario-Biografico\)", source):
                persons[identifier]["sources"][index] = update_trecanni(source)
            elif re.match(r"https://www.parlement.com/.*", source):
                persons[identifier]["sources"][index] = update_parlement(source)

            # Authors
            elif mat := re.match(r"\$Beth, (.*)", source):
                persons[identifier]["sources"][
                    index
                ] = f"Beth, J.C., De archieven van het Departement van Buitenlandsche Zaken (Den Haag, 1918), {mat.groups()[0]}"  # pylint: disable=line-too-long
            elif re.match(r"\$Lohrli", source):
                persons[identifier]["sources"][
                    index
                ] = "Lohrli, Anne, ‘The Madiai: A Forgotten Chapter of Church History’, Victorian Studies 33 (1989), 29–50"  # pylint: disable=line-too-long
            elif mat := re.match(r"\$Moroni, (\d*), (.*)", source):
                persons[identifier]["sources"][
                    index
                ] = f"Moroni, G., Dizionario di erudizione storico-ecclesiastica da S. Pietro sino ai nostri giorni. Volume {mat.groups()[0]} (Rome, 1840), {mat.groups()[1]}"  # pylint: disable=line-too-long
            elif mat := re.match(r"\$Moscati, (.*)", source):
                persons[identifier]["sources"][
                    index
                ] = f"Moscati, Ruggero, Le scritture della segreteria di Stato degli Affari Esteri del Regno di Sardegna (Rome, 1947), {mat.groups()[0]}"  # pylint: disable=line-too-long
            elif mat := re.match(r"\$Santen, (.*)", source):
                persons[identifier]["sources"][
                    index
                ] = f"van Santen, Cornelis Willem, Het internationale recht in Nederlands buitenlands beleid: een onderzoek in het archief van het Ministerie van Buitenlandse Zaken (Den Haag, 1955), {mat.groups()[0]}"  # pylint: disable=line-too-long
            elif mat := re.match(r"\$Schmidt-Brentano, (.*)", source):
                persons[identifier]["sources"][
                    index
                ] = f"Schmidt-Brentano, Antonio, Die k. k. bzw. k. u. k. Generalität 1816-1918 (Vienna 2007), {mat.groups()[0]}"  # pylint: disable=line-too-long
            elif re.match(r"\$Sträter", source):
                persons[identifier]["sources"][
                    index
                ] = "Sträter, F., Herinneringen aan de Eerwaarde Paters Leo, Clemens en Wilhelm Wilde, priesters der Sociëteit van Jezus (Nijmegen, 1911)"  # pylint: disable=line-too-long
            elif mat := re.match(r"\$Wels, (.*)", source):
                persons[identifier]["sources"][
                    index
                ] = f"Wels, Cornelis Boudewijn, Bescheiden betreffende de buitenlandse politiek van Nederland, 1848-1919. Volume 1 (Den Haag, 1972), {mat.groups()[0]}"  # pylint: disable=line-too-long

            elif mat := [i for i in compiled_source_patterns if i.match(source)]:
                used_patterns.add(mat[0])

            # Sources to discuss
            # TODO: What to do with these two sites? Links are not persistent (I think)
            elif source.startswith("https://notes9.senato.it/"):
                pass
            elif source.startswith("https://storia.camera.it/presidenti/"):
                pass
            elif source.startswith("https://storia.camera.it/deputato/"):
                pass
            # TODO: Similar to problem avoce
            elif source.startswith("https://www.britannica.com/biography/"):
                pass

            # Sources to look up
            elif source.startswith("Dizionario bibliografico dell’Armata Sarda seimila biografie"):
                pass

            # If not known/missing
            else:
                count_todo += 1
                if not source.startswith("http"):
                    probably_wrong.append(source)
                print(count_todo, data["name"], data["surname"])
                print("", source)

    persons["$schema"] = "../static/JSON/Individuals.json"

    # Write new file if this file itself is run
    if __name__ == "__main__":
        with open("outputs/Individuals.json", "w", encoding="utf-8") as file:
            json.dump(persons, file, ensure_ascii=False, indent=4)
        print("Wrote file to outputs/Individuals.json")
    if probably_wrong:
        print("\nThese sources might be wrong")
        for i in probably_wrong:
            print("", i)
    unused_patterns = [i for i in compiled_source_patterns if not i in used_patterns]
    if unused_patterns:
        print(f"Found the following unused source patterns:\n {unused_patterns}")
    print(f"Finished checking sources in {filename}!\n")


if __name__ == "__main__":
    check_all_sources("inputs/Individuals.json")