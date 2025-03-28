"""
Třída pro reprezentaci hracích karet
"""

class Card:
    """
    Třída pro reprezentaci hracích karet
    """

    def __init__(self, rank, suit):
        """
        :type rank: int
        :param rank:
        :param suit:
        """
        if not isinstance(rank, int) or rank < 2 or rank > 14:
            raise TypeError("Invalid rank value. Rank must be an integer between 2 and 14.")
        if not isinstance(suit, str) or suit not in ['s', 'k', 'p', 't']:
            raise TypeError("Invalid suit value. Suit must be one of the characters: 's', 'k', 'p', 't'.")

        self.rank = rank
        self.suit = suit

    def black_jack_rank(self):
        """"
        :return:
        """
        if 2 <= self.rank <= 10:
            return self.rank
        elif 11 <= self.rank <= 13:
            return 10
        elif self.rank == 14:
            return 11

    def compare_cards(self, other_card):
        """
        :type other_card: Card
        :param other_card:
        :return:
        """
        if not isinstance(other_card, Card):
            raise TypeError("Invalid argument. Must provide a Card object.")

        return self.black_jack_rank() - other_card.black_jack_rank()

    def __eq__(self, other):
        """
        :type other: Card
        :param other:
        :return:
        """
        if isinstance(other, Card):
            return self.compare_cards(other) == 0
        return False

    def __lt__(self, other):
        """"
        :type other: Card
        :param other:
        :return:
        """
        if isinstance(other, Card):
            return self.compare_cards(other) < 0
        return False

    def __gt__(self, other):
        """
        :type other: Card
        :param other:
        :return:
        """
        if isinstance(other, Card):
            return self.compare_cards(other) > 0
        return False

    def __le__(self, other):
        """
        :type other: Card
        :param other:
        :return:
        """
        if isinstance(other, Card):
            return self.compare_cards(other) <= 0
        return False

    def __ge__(self, other):
        """
        :type other: Card
        :param other:
        :return:
        """
        if isinstance(other, Card):
            return self.compare_cards(other) >= 0
        return False

    def __ne__(self, other):
        """
        :type other: Card
        :param other:
        :return:
        """
        if isinstance(other, Card):
            return self.compare_cards(other) != 0
        return False

    def rank(self, value: int):
        """
            rank setter
        """

        if value < 2 or value > 14:
            raise TypeError()

        self.rank = value

    def suit(self, value: str):
        """
            suit setter
        """

        allowed_values = ["s", "k", "p", "t"]

        if value not in allowed_values:
            raise TypeError()

        self.suit = value

    def __str__(self):

        """
        ssssss
        :return:
        """
        num_str = [
            "dvojka",
            "trojka",
            "čtyřka",
            "pětka",
            "šestka",
            "sedmička",
            "osmička",
            "devítka",
            "desítka"
        ]

        suit_str = {
            "s": {
                "m": "srdcový",
                "f": "srdcová",
                "n": "srdcové"
            },
            "k": {
                "m": "kárový",
                "f": "kárová",
                "n": "kárové"
            },
            "p": {
                "m": "pikový",
                "f": "piková",
                "n": "pikové"
            },
            "t": {
                "m": "trefový",
                "f": "trefová",
                "n": "trefové",
            }
        }

        if self.rank <= 10:
            return f'{suit_str[self.suit]["f"]} {num_str[self.rank - 2]}'

        more_than_ten = [
            ("m", "spodek"),
            ("f", "královna"),
            ("m", "král"),
            ("n", "eso")
        ]

        rod, rank_name = more_than_ten[self.rank - 11]

        return f'{suit_str[self.suit][rod]} {rank_name}'


if __name__ == '__main__':
    pass

