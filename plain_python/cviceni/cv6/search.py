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

import re
from typing import Any, TextIO


def process_text(text: str) -> None:
    """
    Method that process the text and finds the number of words that match the patterns
    which are specified above. And prints the results.
    :param text: text loaded from the file preferably.
    :return: void
    """
    # Define regex patterns for the different word types
    duplicate_words_pattern: str = r'\b(\w+)\b(.*)\b\1\b'
    double_vowels_pattern: str = r'\b\w*[aeyiou]{2}\w*\b'
    triple_vowels_pattern: str = r'\b\w*[aeyiou]\w*[aeyiou]\w*[aeyiou]\w*\b'
    long_words_pattern: str = r'.{6,}'

    # Count the number of words that match the patterns
    text = text.lower()
    # Convert all words to lowercase
    words: list[Any] = re.findall(r'\b\w+\b', text)

    # Count the number of lines containing duplicate words
    num_duplicates: int = len(re.findall(duplicate_words_pattern, text))

    # Remove duplicates from the list of words
    unique_words: list[Any] = list(set(words))

    # Convert the list of unique words to a string
    unique_words_string: str = ' '.join(unique_words)

    # Count the number of words containing double vowels
    num_double_vowels: int = len(re.findall(double_vowels_pattern, unique_words_string))

    # Count the number of words containing triple vowels
    num_triple_vowels: int = len(re.findall(triple_vowels_pattern, unique_words_string))

    # Count the number of words with 6 or more characters
    long_word_count: int = 0
    for word in unique_words:
        if re.match(long_words_pattern, word):
            long_word_count += 1

    # Print the results
    print(f"{num_double_vowels}")
    print(f"{num_triple_vowels}")
    print(f"{long_word_count}")
    print(f"{num_duplicates}")


def main(file_name: str):

    # Read the text file
    file: TextIO
    with open(file_name, 'r') as file:
        text: str = file.read()

    process_text(text)


if __name__ == '__main__':
    main('cv06_test.txt')
