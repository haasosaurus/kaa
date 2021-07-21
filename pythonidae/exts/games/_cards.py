# -*- coding: utf-8 -*-


import enum
import random
from typing import Union


class Card:
    """
    represents a single playing card
    """

    class Suit(enum.Enum):
        SPADES = ('Spades', 'S', '♠️')
        DIAMONDS = ('Diamonds', 'D', '♣️')
        CLUBS = ('Clubs', 'C', '♥️')
        HEARTS = ('Hearts', 'H', '♦️')

        def __repr__(self):
            return f'Card.Suit.{self.name}'

        def __str__(self):
            return self.__repr__()

        def format_long(self):
            return self.value[0]

        def format_short(self):
            return self.value[1]

        def format_emoji(self):
            return self.value[2]

    class Rank(enum.Enum):
        ACE = (0, 'Ace', 'A')
        TWO = (1, 'Two', '2')
        THREE = (2, 'Three', '3')
        FOUR = (3, 'Four', '4')
        FIVE = (4, 'Five', '5')
        SIX = (5, 'Six', '6')
        SEVEN = (6, 'Seven', '7')
        EIGHT = (7, 'Eight', '8')
        NINE = (8, 'Nine', '9')
        TEN = (9, 'Ten', '10')
        JACK = (10, 'Jack', 'J')
        QUEEN = (11, 'Queen', 'Q')
        KING = (12, 'King', 'K')

        def __repr__(self):
            return f'Card.Rank.{self.name}'

        def __str__(self):
            return self.__repr__()

        def __int__(self):
            return self.value[0]

        def format_long(self):
            return self.value[1]

        def format_short(self):
            return self.value[2]


    def __init__(self, rank: Rank, suit: Suit, value: int = None):
        self.rank = rank
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f'Card({self.rank.__repr__()}, {self.suit.__repr__()})'

    def __str__(self):
        return self.__repr__()

    def format_long(self):
        return f'{self.rank.format_long()} of {self.suit.format_long()}'

    def format_short(self):
        return f'{self.rank.format_short()}{self.suit.format_short()}'

    def format_short_emoji(self):
        return f'{self.rank.format_short()}{self.suit.format_emoji()}'


class Deck:
    """
    playing card deck class
    """

    class Icons:
        """
        icon container for Card/Deck
        """

        card_back = '🂠'
        joker_red = '🂿'
        joker_white = '🃏'
        joker_black = '🃟'
        clubs = '🃑🃒🃓🃔🃕🃖🃗🃘🃙🃚🃛🃝🃞'
        clubs_extra = '🃜'
        diamonds = '🃁🃂🃃🃄🃅🃆🃇🃈🃉🃊🃋🃍🃎'
        diamonds_extra = '🃌'
        hearts = '🂱🂲🂳🂴🂵🂶🂷🂸🂹🂺🂻🂽🂾'
        hearts_extra = '🂼'
        spades = '🂡🂢🂣🂤🂥🂦🂧🂨🂩🂪🂫🂭🂮'
        spades_extra = '🂬'


    def __init__(
            self,
            cards = None,
            *,
            jokers: bool = False,
            shuffled: bool = False,
    ):
        if cards is not None:
            self._cards = cards
        else:
            self._cards = [Card(rank, suit) for suit in [Card.Suit.SPADES, Card.Suit.DIAMONDS] for rank in Card.Rank]
            self._cards.extend(Card(rank, suit) for suit in [Card.Suit.CLUBS, Card.Suit.HEARTS] for rank in reversed(Card.Rank))

        if jokers:
            raise NotImplementedError('please implement this parameter')

        if shuffled:
            self.shuffle()

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, s: Union[int, slice]):
        return self._cards[s]

    def shuffle(self):
        random.shuffle(self._cards)

    def deal(self):
        return self._cards.pop()





def tests():

    def print_header(title, line_length=30):
        line_length = 30
        print('-' * line_length)
        indent = line_length // 2 - len(title) // 2
        print(f"{' ' * indent}{title}\n{'-' * line_length}")

    # debug options
    debugging_card = True
    # debugging_card = False

    debugging_suit = True
    debugging_suit = False

    debugging_rank = True
    debugging_rank = False

    debugging_deck = True
    debugging_deck = False


    # tests - card
    if debugging_card:
        print_header('Card')
        card = Card(Card.Rank.ACE, Card.Suit.SPADES)
        print(f'{card.__repr__()}')
        print(f'{str(card)=}')
        print(f'{card.format_short()=}')
        print()


    # tests - deck
    if debugging_deck:
        print_header('Deck')

        # print debug info
        deck = Deck(shuffled=False)
        for card in deck:
            print(f'    {card.format_long()}')
        print()

        print(f'{len(deck)=}')
        # print(deck.Icons.joker_white)
        # print(deck.Icons.clubs[0])

        print()


    # tests - suit
    if debugging_suit:
        print_header('Suit')

        # print debug info
        card = Card(Card.Rank.ACE, Card.Suit.SPADES)
        print(f'{str(card.suit)=}')

        # for name, member in Card.Suit.__members__.items():
        #     print(f'name: {name}, member: {member}')

        print()


    # tests - rank
    if debugging_rank:
        print_header('Rank')

        # print debug info
        card = Card(Card.Rank.ACE, Card.Suit.SPADES)
        print(f'{int(card.rank)=}')
        print(f'{str(card.rank)=}')

        print()


if __name__ == '__main__':
    tests()
