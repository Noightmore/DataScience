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


def solve_puzzle(words):
    for perm in itertools.permutations(words):
        chain = [perm[0]]
        for i in range(1, len(perm)):
            if chain[-1][-1] == perm[i][0]:
                chain.append(perm[i])
            else:
                break
        else:
            return True  # executed if the loop completes without encountering a "break"
    return False


def doors():
    with open("large.txt", encoding='utf-8-sig') as f:
        num_cases = int(f.readline().strip())

        for _ in range(num_cases):
            num_words = int(f.readline().strip())
            words = []

            for _ in range(num_words):
                words.append(f.readline().strip())

            result = solve_puzzle(words)

            print(result)


if __name__ == '__main__':
    import itertools
    doors()

