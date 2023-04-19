# -*- coding: utf-8 -*-

"""
Úkol 6.
Vaším dnešním úkolem je vytvořit program, který o zadaném textu zjistí některé
údaje a vypíše je na standardní výstup. Hlavním smyslem cvičení je procvičit
si práci s regulárními výrazy, takže pro plný bodový zisk je nutné použít k
řešení právě tento nástroj.

Program musí pracovat s obecným textem, který bude zadaný v souboru. Jméno
souboru bude zadáno jako vstupní parametr funkce main, která by měla být
vstupním bodem programu. Samozřejmě, že funkce main by neměla řešit problém
kompletně a měli byste si vytvořit další pomocné funkce. Můžete předpokládat,
že soubor bude mít vždy kódování utf-8 a že bude psaný anglicky, tedy jen
pomocí ASCII písmen, bez české (či jiné) diakritiky.

Konkrétně musí program zjistit a vypsat:

1. Počet slov, která obsahují nejméně dvě samohlásky (aeiou) za sebou. Například
slovo bear.

2. Počet slov, která obsahují alespoň tři samohlásky - například slovo atomic.

3. Počet slov, která mají šest a více znaků - například slovo terrible.

4. Počet řádků, které obsahují nějaké slovo dvakrát.

Podrobnější zadání včetně příkladu je jako obvykle na elearning.tul.cz
"""


import os
import re
from typing import Match, Any

two_vowels = r'[aeiyou]{2}'
TWO_VOWELS = re.compile(two_vowels, re.IGNORECASE)
three_vowels = r'[aeiyou]'
THREE_VOWELS = re.compile(three_vowels, re.IGNORECASE)
six_chars = r'.'
SIX_CHARACTERS = re.compile(six_chars, re.IGNORECASE)
duplicate_words = r'\b(\w+)\b(.*)\b\1\b'
DUPLICATE_WORDS = re.compile(duplicate_words, re.IGNORECASE)


def get_matches_counts(word: str, counter: dict) -> object:
    """
    Finds specific patterns in a word.
    """

    if not word.strip():
        return

    two_vowels_result = TWO_VOWELS.search(word)
    if two_vowels_result:
        counter["two_vowels"] += 1

    three_vowels_result = THREE_VOWELS.findall(word)
    if len(three_vowels_result) >= 3:
        counter["three_vowels"] += 1

    six_characters_result = SIX_CHARACTERS.findall(word)
    if len(six_characters_result) >= 6:
        counter["six_characters"] += 1


def main(file_name: str):
    """
    processes the file and checks for specific patterns.
    Prints the results.
    """

    if not os.path.isfile(file_name):
        return

    match_counter = dict(two_vowels=0, three_vowels=0, six_characters=0, duplicates_in_line=0)

    with open(file_name, "r", encoding="utf-8") as file:
        rows: list[str] = file.readlines()

        rows = list(map(lambda row: row.strip(), rows))

        for line in rows:
            has_duplicates: Match[str] | None = DUPLICATE_WORDS.search(line)

            if has_duplicates is None:
                continue

            match_counter["duplicates_in_line"] += 1

        rows = list(map(lambda x: x.split(" "), rows))

        words: list[Any] = list(set({word.lower() for words in rows for word in words}))

        for word in words:
            get_matches_counts(word, match_counter)

    for key in match_counter:
        print(match_counter[key])


if __name__ == '__main__':
    main('cv06_test.txt')
