# -*- coding: utf-8 -*-

"""
Cvičení 7. - práce s daty

Vaším dnešním úkolem je spojit dohromady data, uložená ve dvou různých
souborech. První soubor obsahuje výsledky závodu - jména a časy závodníků. Druhý
pak obsahuje databázi závodníků uloženou jako JSON - mimo jiné jejich id. Cílem
je vytvořit  program, který tyto data propojí, tedy ke každému závodníkovi ve
štafetě najde jeho id. Případně také nenajde, data nejsou ideální. I tuto
situaci ale musí program korektně ošetřit.  Výsledky programu bude potřeba
zapsat do dvou souborů.

Kompletní zadání je jako vždy na https://elearning.tul.cz/

"""
from typing import Dict, List, TypedDict
import json
from bs4 import BeautifulSoup
import re


class RacerData(TypedDict):
    """
        class for storing json data for each racer
    """
    id: int
    firstname: str
    lastname: str
    nationality: str
    birth: str
    gender: str


def load_data_from_html() -> (List[Dict], List[Dict]):

    """
    Function for loading data from HTML file
    """

    men = []
    women = []

    # Read the HTML file
    with open('result.html') as file:
        html = file.read()

    # Parse the HTML using Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Find the paragraph that contains the word "Relay" in a <strong> tag
    strong_tag = soup.find('strong', text='Relay')
    parent_paragraph = strong_tag.find_parent('p')

    # Find the next four paragraphs
    next_paragraphs = parent_paragraph.find_next_siblings('p', limit=4)

    women_flag = False
    men_flag = False

    # Print the text content of the four paragraphs
    for p in next_paragraphs:
        #print(p.text)

        if p.text == "Women":
            women_flag = True
        elif p.text == "Men":
            men_flag = True

        if men_flag:
            men = store_parsed_data(p.text)
        elif women_flag:
            women = store_parsed_data(p.text)

    return men, women


def store_parsed_data(text: str) -> List[Dict]:
    """
        Function for parsing text into a list of dictionaries of racers
    """

    pattern = r'\d+\)\s+(\w+)\s+(\d+:\d+:\d+)\s+\((.*?)\)'
    matches = re.findall(pattern, text)

    structs = []
    for match in matches:
        country = match[0]
        time = match[1]
        names = [n.strip() for n in match[2].split(',')]
        structs.append({'country': country, 'time': time, 'names': names})

    return structs


def parse_json():
    """
        Funkce pro preprocessing JSON souboru se závodníky
    """
    record: Dict[str, List[RacerData]] = {}

    with open('competitors.json', 'r', encoding="utf-8") as json_file:
        data: List[RacerData] = json.load(json_file)

        for racer in data:
            if racer.get("lastname") not in record:
                record[racer.get("lastname")] = []

            record[racer.get("lastname")].append(racer)

    return record


def output_json(result_list):
    """
    Uloží list slovníků do souboru output.json tak jak je požadováno 
    v zadání.
    """
    with open('output.json', 'w') as output:
        output.write(json.dumps(result_list, indent=4, sort_keys=True))


def main():
    men, women = load_data_from_html()
    sportsmen = parse_json()
    result = []

    # print the results
    print("MEN")
    for _ in men:
        print(_)

    print("WOMEN")
    for _ in women:
        print(_)

    #for _ in sportsmen:
    #   print(_)

    for sportsman in men + women:
        if sportsman["lastname"] in sportsmen:
            candidates = sportsmen.get(sportsman["lastname"])
            is_in_list = False
            racer_from_db = None

            for candidate in candidates:
                if candidate.get("firstname") == sportsman.get("firstname"):
                    is_in_list = True
                    racer_from_db = candidate
                    break

            if is_in_list:
                result.append({
                    "id": racer_from_db.get("id"),
                    "result": sportsman.get("result"),
                    "time": sportsman.get("time")
                })
                return

            result.append({
                "id": False,
                "result": sportsman.get("result"),
                "time": sportsman.get("time"),
                "no_match": " ".join([sportsman.get("firstname"), sportsman.get("lastname")])
            })


if __name__ == '__main__':
    main()
