import json
import re

COMMENT_PATTERNS = {
    r"Amadeo Bert was an important contact for travellers.*\.$",
    r"Captain of the ship De Pelicaan.$",
    r"Edgar Ney played an important part in the defense and liberation of Rome during the period of the Roman Republic\.$",  # pylint: disable=line-too-long
    r"Eugenio Giuseppe Allet was also known as colonel M. Allet.$",
    r"François-Xavier Wurth-Paquet held several other \(ministerial\) positions within the Grand Duchy of Luxembourg*\.$",  # pylint: disable=line-too-long
    r"Giambatista Leveroni held the position of vice-president until 1832 or 1833\.$",
    r"Giuseppe Birigazzi and Giuseppe Cavalieri were convicted for inciting a revolt in Bologna.*\.$",  # pylint: disable=line-too-long
    r"His name in Cyrillic script is '.*'\.$",
    r"Ignacio de Valdivieso joined Pope Pius IX in his flight to Gaeta\.$",
    r"Louis du Chastel de la Howarderie had several other functions in the Dutch diplomatic services.*\.$",  # pylint: disable=line-too-long
    r"Luigi Arata was also consul of several other countries, notably Russia\.$",
    r"Paolo Gerolamo Pallavcini was president of the Magistrato since at least 1824\.$",
    r"Sometimes referred to as Verbeke. Several consul.*\.$",
    r"The archive contains documents related to his death, inheritance and a dispute between his heirs\.$",  # pylint: disable=line-too-long
    r"The archive contains documents related to his death and inheritance\.$",
    r"The archive contains documents related to the death and inheritance of her brother, Giovanni Vassen\.$",  # pylint: disable=line-too-long
    r"The archive contains documents related to the death and inheritance of his relative, Giovanni Ronca\.$",  # pylint: disable=line-too-long
    r"The appointment and position of Jacobus Grooff led to some diplomatic correspondence which is documented and discsussed in Santen\.$",  # pylint: disable=line-too-long
    r"The family Meuricoffre was an important banking family in Napels who often functioned as representative of the Dutch in Napels\.$",  # pylint: disable=line-too-long
    r"The family Wilde was originally from Germany and was part of the larger .*\.$",
    r"The Madiai family was involved in an international scandal, discussion of which can be found in the note\.$",  # pylint: disable=line-too-long
    r"\w* \w* held several other \(ministerial\) positions within the Kingdom of.*\.$",
    r"\w* \w* held the position of vice president until 1829 or 1830 and at least since 1824\.$",
    r"\w* \w* is mentioned in the archive in relation to the inheritance of Francesco Cornelio Verbruggen from Genoa\.$",  # pylint: disable=line-too-long
    r"\w* \w* is mentioned in the archive in relation to the inheritance of the Vassen family\.$",
    r"\w* \w* published several works and studies, one of which can be found in the archive. Note has a list of publications\.$",  # pylint: disable=line-too-long
    r"\w* wrote a letter to E. van der Hoeven about the vacant post of Consul General of the Kingdom of the Netherlands in Genoa\.$",  # pylint: disable=line-too-long
    r"\w* \w* was a local Roman lawyer\.$",
    r"\w* \w* was also consul of several other countries\.$",
    r"\w* \w* was convicted of an act of rebellion and insurrection. The notice of his conviction is included in the archive\.$",  # pylint: disable=line-too-long
    r"\w* \w* wrote a letter to E. van der Hoeven about the vacant post of Consul General of the Kingdom of the Netherlands in Genoa\.$",  # pylint: disable=line-too-long
    r"\w* \w* wrote several studies on the government and military of various Italian states.*\.$",
}


def check_all_comments(filename):
    """Checks all comments for given database

    Args:
        filename (str): File name of initial database
    """
    with open(filename) as file:
        persons = json.load(file)
    del persons["$schema"]
    count_todo = 0
    compiled_comment_patterns = [re.compile(i) for i in COMMENT_PATTERNS]

    for identifier, data in persons.items():
        comment = data["comment"]
        if comment == "":
            pass

        elif [True for i in compiled_comment_patterns if i.match(comment)]:
            pass

        else:
            count_todo += 1
            print(count_todo, identifier, data["name"], data["surname"])
            print(f"    {comment}")

    print(f"Finished checking comments in {filename}\n")


if __name__ == "__main__":
    check_all_comments("inputs/Individuals.json")
