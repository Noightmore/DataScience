"""
Implementujte program dle zadání úlohy 9. na elearning.tul.cz

Vytvořte program, který prohledá zadaný textový
soubor a nejde v něm řádky, na kterých se vyskytuje hledaný vzor. Případně více
vzorů. Tyto řádky pak vypíše na obrazovku a přidat k ním jejich čísla v původním
souboru.

Tak trochu se toto chování podobá unixovému příkazu grep, přesněji
řečeno grep -n.  Ten můžete případně použít pro kontrolu. Nicméně váš program
toho bude umět v mnoha ohledech méně a v jednom více (vyhledávání více vzorů
najednou). Nejde tedy o to vytvářet 100% kopii příkazu grep.

Program musí jít  ovládat z příkazové řádky. Základním parametrem zadávaným
vždy, je jméno souboru. Pokud jméno souboru není zadané program nemůže pracovat
a měl by v takovém případě zobrazit nápovědu.

Druhý parametr  parametr -s --search bude volitelný. Může být následován
libovolným počtem n slov. Samozřejmě, pokud je tam parametr -s musí tam být to
slovo alespoň jedno (tedy n >= 1).  Pokud není zadané hledané slovo, musí
program opět vypsat chybu nebo nápovědu.
 """

import argparse
import os
import sys
from pathlib import Path

parser = argparse.ArgumentParser(
    prog='Hledac',
    description='Hledá řádky v souboru, které obsahují zadané výrazy, stejně jako příkaz grep -n',
    exit_on_error=False
)
parser.add_argument("-f", "--filename", help="Jméno souboru k analýze")
parser.add_argument("-s", "--search", action="extend",
                    nargs="+", help="Hledané výrazy")


def read_file(filepath: Path) -> list[str]:
    """
        function for reading file
    """

    if not os.path.isfile(filepath):
        return []

    with open(filepath, encoding="utf-8") as filehandle:
        lines = filehandle.readlines()
        return lines


def number_them_lines(lines: list[str]) -> list[str]:
    """
        line numbering function
    """
    return [f"{i + 1}:{x}" for i, x in enumerate(lines)]


def filter_lines(lines: list[str], expressions: list[str]) -> list[str]:
    """
        line filtering function
    """

    return list(filter(lambda line: all(expr in line for expr in expressions), lines))


def main(cli_args=None) -> int:
    """
    Main Program method
    """

    if cli_args is None:
        cli_args = []

    try:
        args = parser.parse_args(cli_args)

        if args.filename is None:
            raise ValueError()

        path_to_file = Path(args.filename)
        contents = read_file(path_to_file)
        numbered = number_them_lines(contents)

        if args.search is not None:
            filtered_lines = filter_lines(numbered, args.search)
            output_lines(filtered_lines)
        else:
            output_lines(numbered)

        return 0

    except (ValueError, argparse.ArgumentError):
        parser.print_help()
        return -1


def output_lines(lines):
    """
    Outputs the lines to the console
    """
    print("".join(lines))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

