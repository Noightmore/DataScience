"""
Na vstupu jsou dány 3 sekvence. Každá z nich obsahuje několik uspořádaných
dvojic uložených jako tuple (id, count).
Sekvence může tedy vypadat například takto: ((1, 3), (3, 4), (10, 2)).
První prvek sekvence je tedy tuple s hodnotami  id = 1 je count = 3 a tak dále.
Vaším úkolem je spojit tyto tři sekvence do jednoho slovníku. Ten bude výstupem z programu.

Položky slovníku budou v následujícím tvaru {id: [A, B, C]},
kde A, B a C jsou hodnoty pro příslušné ID v první, druhé a třetí sekvenci.

Ovšem pozor - neplatí, že každé id je obsaženo ve všech sekvencích.
Může být ve všech, ve dvou, nebo pouze v jedné.

Tady máte konkrétní příklad. Zadané sekvence mají následující podobu:

line_a = ((1, 3), (3, 4), (10, 2))
line_b = ((1, 2), (2, 4), (5, 2))
line_c = ((1, 5), (3, 2), (7, 3))

Transformací musí vzniknout následující slovník:

{1: [3, 2, 5],
 2: [0, 4, 0],
 3: [4, 0, 2],
 5: [0, 2, 0],
 7: [0, 0, 3],
10: [2, 0, 0]}
"""


def merge_tuples(line_a, line_b, line_c):
    """
    Funkce, která převede tři sekvence na slovník
    """

    # kdyby byl promenny pocet jednotlivych radku na vstupu list hodnot ve slovniku by byl ,
    # tak by zde na zacatku se promenna line a seznam jejich delek vytvarely dynamicky
    _dict = {}
    line = line_a + line_b + line_c
    lens = [len(line_a), len(line_b), len(line_c)]

    line_size = lens[0]
    dict_list_index = 0

    for i, _tuple in enumerate(line):
        # check if key exists at _tuple[0]

        if _tuple[0] not in _dict:
            _dict[_tuple[0]] = []
            # initialize list
            for _ in range(dict_list_index):
                _dict[_tuple[0]].append(0)

        _dict[_tuple[0]].append(_tuple[1])

        if i - line_size + 1 == 0:
            for key in _dict:
                if len(_dict[key]) <= dict_list_index:
                    _dict[key].append(0)

        if i - line_size == 0:
            line_size += lens[dict_list_index + 1]
            dict_list_index += 1

    _dict = dict(sorted(_dict.items()))
    return _dict


def simple_visual_test():
    """
    Print výsledku je sice primitivní metoda, ale jako základní test
    slouží programátorům odjakživa...
    """

    #line_a = ((1, 3), (3, 4), (10, 2))
    #line_b = ((1, 2), (2, 4), (5, 2))
    #line_c = ((1, 5), (3, 2), (7, 3))

    line_a = ((1, 3), (3, 4), (10, 2))
    line_b = ((1, 2), (2, 4), (5, 2), (12, 3), (6, 3))
    line_c = ((1, 5), (3, 2), (7, 3))

    my_dict = merge_tuples(line_a, line_b, line_c)
    print(line_a + line_b + line_c)
    print(my_dict)


if __name__ == "__main__":
    simple_visual_test()

"""
************* Module merger
cv3/merger.py:55:12: C0206: Consider iterating with .items() (consider-using-dict-items)

Poznamky k pylintu, opet nesmyslne pripomenuti, na radku 57 vylozene potrebuji pristupovat k prvku na klici slovniku
iterace pouze pres hodnoty klicu neni mozna.

"""