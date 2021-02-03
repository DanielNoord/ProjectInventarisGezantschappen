import lxml.etree as etree
import re
from datetime import date

def volume(volume):
    pattern = re.compile(r"Volume[\n\r\s]+m[sa]. (.+?)\n(.*?)\n(.*?);\n(.*)\n.*?$", re.DOTALL)
    number, title, volume_date, content = re.match(pattern, volume).groups()
    return number, title, volume_date, content

def split_into_dossiers(volume):
    pattern = re.compile(r"(Dossier.*?(?=Genoemd))", re.DOTALL)
    return re.findall(pattern, volume)

def dossier(dossier):
    pattern = re.compile(r"Dossier (.+) \((.*) bl.\):\n(.*?);\n(.*?);"
                            r"\n*(~.*?;.*?;.*?;)?\n*(In het bijzonder;)?"
                            r"\n*(-.*;)?", re.DOTALL)
    return re.match(pattern, dossier).groups()

def dossier_description(description):
    pattern = re.compile(r"~ bl. (.*?): (.*?); \((.*?); (.*?)\);", re.DOTALL)
    return re.match(pattern, description).groups()

def file(file):
    pattern = re.compile(r"- bl. (.*?): (.*?); \((.*?); (.*?)\);", re.DOTALL)
    return re.match(pattern, file).groups()