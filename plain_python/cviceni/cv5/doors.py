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
    def build_chain(chain, remaining_words):
        if not remaining_words:
            return True
        last_word = chain[-1]
        for i, word in enumerate(remaining_words):
            if last_word[-1] == word[0]:
                result = build_chain(chain + [word], remaining_words[:i] + remaining_words[i+1:])
                if result:
                    return True
        return False

    for i, word in enumerate(words):
        if build_chain([word], words[:i] + words[i+1:]):
            return True
    return False


def doors():
    with open("small.txt", encoding='utf-8-sig') as f:
        num_cases = int(f.readline().strip())

        for _ in range(num_cases):
            num_words = int(f.readline().strip())
            words = []

            for _ in range(num_words):
                words.append(f.readline().strip())

            result = solve_puzzle(words)

            print(result)


if __name__ == '__main__':
    doors()

