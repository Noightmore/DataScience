# -*- coding: utf-8 -*-

"""
Úkol 5.
Napište program, který načte soubor large.txt a pro každé dveře vyhodnotí,
zda je možné je otevřít nebo ne. Tedy vyhodnotí, zda lze danou množinu uspořádat
požadovaným způsobem. Výstup z programu uložte do souboru vysledky.txt ve
formátu 1 výsledek =  1 řádek. Na řádek napište vždy počet slov v množině a True
nebo False, podle toho, zda řešení existuje nebo neexistuje.
Podrobnější zadání včetně příkladu je jako obvykle na elearning.tul.cz
"""

from collections import defaultdict
import os


def create_vertex_weights(words) -> dict:
    """
        Function to create a dictionary of letters with their counts at the start and end of the word.
    """
    dictionary = defaultdict(lambda: [0, 0])

    for word in words:
        safe_word = word.strip()

        leading_letter = safe_word[0]
        trailing_letter = safe_word[-1]

        dictionary[leading_letter][0] += 1
        dictionary[trailing_letter][1] += 1

    return dictionary


def is_eulerian_path(dictionary: dict) -> bool:
    """
        Function to check whether a given graph has an Eulerian path or not.
        algorithm source: https://math.stackexchange.com/questions/1871065/euler-path-for-directed-graph
    """

    dominant_out, dominant_in = 0, 0

    for vertex in dictionary:
        in_degree, out_degree = dictionary[vertex]

        if abs(in_degree - out_degree) > 1:
            return False

        if out_degree > in_degree:
            dominant_out += 1

        if in_degree > out_degree:
            dominant_in += 1

    if dominant_out > 1 or dominant_in > 1:
        return False

    return True


def find_solution(input_file_path: str, output_file_path: str) -> bool:
    """
        Function to analyze a text document and the possibility to create a string based
        on the rules of classic word football game.
    """
    if not os.path.isfile(input_file_path):
        return False

    with open(input_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    num_doors = int(lines.pop(0))
    results = []

    for _ in range(num_doors):
        num_words = int(lines.pop(0))
        words = lines[:num_words]
        del lines[:num_words]

        vertex_weights = create_vertex_weights(words)
        is_eulerian = is_eulerian_path(vertex_weights)

        results.append(f'{is_eulerian}')

    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(results))

    return True


def doors():
    find_solution("large.txt", "vysledky.txt")


if __name__ == '__main__':
    doors()

