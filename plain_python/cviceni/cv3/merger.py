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


def merge_tuples(line_a, line_b, line_c) -> dict:
    """
    Funkce, která převede tři sekvence na slovník
    """
    _dict = {}

    for tuples in [line_a, line_b, line_c]:
        for _tuple in tuples:
            index, value = _tuple

            if index not in _dict:
                _dict[index] = [0, 0, 0]

            if tuples is line_a:
                _dict[index][0] += value
            elif tuples is line_b:
                _dict[index][1] += value
            else:
                _dict[index][2] += value
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