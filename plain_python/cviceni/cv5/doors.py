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

from collections import deque


def solve_puzzle(start, target, _list):

    if start == target:
        return False
    # If the target is not
    # present in the dictionary
    if target not in _list:
        return False

    # To store the current chain length
    # and the length of the words
    #level = 0
    wordlength = len(start)

    # Push the starting word into the queue
    Q = deque()
    Q.append(start)

    # While the queue is non-empty
    while (len(Q) > 0):

        # Increment the chain length
        #level += 1

        # Current size of the queue
        sizeofQ = len(Q)

        # Since the queue is being updated while
        # it is being traversed so only the
        # elements which were already present
        # in the queue before the start of this
        # loop will be traversed for now
        for i in range(sizeofQ):

            # Remove the first word from the queue
            word = [j for j in Q.popleft()]
            #Q.pop()

            # For every character of the word
            for pos in range(wordlength):

                # Retain the original character
                # at the current position
                orig_char = word[pos]

                # Replace the current character with
                # every possible lowercase alphabet
                for c in range(ord('a'), ord('z')+1):
                    word[pos] = chr(c)

                    # If the new word is equal
                    # to the target word
                    if "".join(word) == target:
                        return True #level + 1

                    # Remove the word from the set
                    # if it is found in it
                    if "".join(word) not in _list:
                        continue

                    # And push the newly generated word
                    # which will be a part of the chain
                    Q.append(_list.index("".join(word)))

                    del _list[_list.index("".join(word))]

                # Restore the original character
                # at the current position
                word[pos] = orig_char

    return 0


def doors():
    start, target = "", ""
    output = ""
    file = open("large.txt", "r", encoding='utf-8-sig')

    num_cases = int(file.readline().strip())

    for _ in range(num_cases):
        num_words = int(file.readline().strip())
        words = []

        # loads words
        for _a in range(num_words):
            word = file.readline().strip()
            if _a == 0:
                start = word
            elif _a == num_words -1:
                target = word
            words.append(word)

        result = solve_puzzle(start, target, words)
        #print(result)
        output += str(result) + "\n"

    file.close()

    f = open("vysledky.txt", "w")
    print(output)
    f.write(output)
    f.close()


if __name__ == '__main__':
    doors()
