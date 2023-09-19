"""

Program for parsing html and json data and comparing them
according to the requirements specified in the assignment.

"""

import json
import re
from typing import Dict, List, TypedDict, Union
from bs4 import BeautifulSoup


class SportsmanData(TypedDict):
    """
        Sportsman data type for JSON file
    """
    id: int
    firstname: str
    lastname: str
    nationality: str
    gender: bool  # male = True, female = False


def parse_json_and_transfer() -> Dict[str, List[SportsmanData]]:
    """
    Load sportsmen from a JSON file.
    """
    with open('competitors.json', 'r', encoding='utf-8') as json_file:
        sportsmen_data: List[SportsmanData] = json.load(json_file)

    record: Dict[str, List[SportsmanData]] = {}
    for sportsman in sportsmen_data:
        lastname = sportsman.get('lastname')

        if lastname not in record:
            record[lastname] = []
        record[lastname].append(sportsman)

    return record


def parse_html() -> List[SportsmanData]:
    """
    Parse an HTML file to extract sportsmen data.
    """

    with open('result.html', 'r', encoding='utf-8') as html_file:
        content = html_file.read()

    soup = BeautifulSoup(content, 'html.parser')
    relay_cat = soup.find('p', text=re.compile('Relay', flags=re.IGNORECASE))
    relay_line_info = relay_cat.fetchNextSiblings(limit=4)

    gender = None
    sportsmen = []

    for line in relay_line_info:
        text = line.text.strip()

        if text == "Men":
            gender = True
            continue

        if text == "Women":
            gender = False
            continue

        participants = [x.strip() for x in text.split("),")]
        participants = [transfer_sportsmen(x, gender) for x in participants]
        participants = [item for sublist in participants for item in sublist]

        sportsmen.extend(participants)

    return sportsmen


def transfer_sportsmen(string: str, gender: bool) -> List[Dict[str, Union[str, bool]]]:
    """
    Parse a relay results row from an HTML file
    Args:
        string: The string containing the relay results row.
        gender: The gender of the racers in the relay.

    Returns:
        A list of dictionaries containing the parsed data for each racer.
    """
    record = []
    rank_delimiter = string.find(")")
    rank = string[:rank_delimiter]
    text = string[rank_delimiter + 1:].strip()

    country = re.compile("^(.*?)(?=[0-9])", re.IGNORECASE).search(text).group(0).strip()
    text = text[len(country):].strip()

    time = re.compile("[0-9]+:[[0-9]+:[0-9]+").search(text).group(0)
    text = text[len(time):].strip()

    text = text.replace("(", "").replace(")", "").replace(".", "")
    names = [x.strip() for x in text.split(",")]

    for sportsman_name in names:
        firstname, *lastname = re.compile(r"\s+").split(sportsman_name)
        record.append({
            "firstname": firstname,
            "lastname": " ".join(lastname),
            "result": rank,
            "id": False,
            "nationality": country,
            "time": time,
            "gender": gender,
        })

    return record


def output_json(result_list):
    """
    Uloží list slovníků do souboru output.json tak jak je požadováno
    v zadání.
    """

    with open('output.json', 'w', encoding='utf-8') as output:
        output.write(json.dumps(result_list, indent=4, sort_keys=True))


def main() -> None:
    """
    Main program function
    """
    # Load data
    json_data = parse_json_and_transfer()
    html_data = parse_html()

    # Compare data and generate results
    result = []
    for sportsman in html_data:
        lastname = sportsman["lastname"]
        firstname = sportsman["firstname"]
        candidates = json_data.get(lastname, [])
        db_sportsman = next(
            (c for c in candidates if c.get("firstname") == firstname), None
        )

        if db_sportsman:
            result.append(
                {
                    "id": db_sportsman.get("id"),
                    "result": sportsman.get("result"),
                    "time": sportsman.get("time"),
                }
            )

        result.append(
            {
                "id": False,
                "result": sportsman.get("result"),
                "time": sportsman.get("time"),
                "no_match": f"{firstname} {lastname}",
            }
        )

    # Output results to file
    output_json(result)
    with open('compare.txt', 'w', encoding='utf-8') as compare, open(
            'errors.txt', 'w', encoding='utf-8'
    ) as errors:
        sorted_results = sorted(result, key=lambda x: x["id"])
        for sportsman in sorted_results:
            if sportsman.get("id") is False:
                name = sportsman.get("no_match")
                errors.write(f"{name}\n")
                continue

            s_id = sportsman["id"]
            s_res = sportsman["result"]
            compare.write(f"{s_id} {s_res}\n")


if __name__ == '__main__':
    main()
