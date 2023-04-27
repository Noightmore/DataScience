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


def output_json(result_list):
    """
    Uloží list slovníků do souboru output.json tak jak je požadováno 
    v zadání.
    """
    with open('output.json', 'w') as output:
        output.write(json.dumps(result_list, indent=4, sort_keys=True))



if __name__ == '__main__':
    pass