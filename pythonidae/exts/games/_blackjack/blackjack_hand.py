# -*- coding: utf-8 -*-


from itertools import islice

from exts.games._cards import Card


class BlackjackHand:
    """class for storing cards and calculating the the hands values"""

    card_values = {
        Card.Rank.ACE: 1,
        Card.Rank.TWO: 2,
        Card.Rank.THREE: 3,
        Card.Rank.FOUR: 4,
        Card.Rank.FIVE: 5,
        Card.Rank.SIX: 6,
        Card.Rank.SEVEN: 7,
        Card.Rank.EIGHT: 8,
        Card.Rank.NINE: 9,
        Card.Rank.TEN: 10,
        Card.Rank.JACK: 10,
        Card.Rank.QUEEN: 10,
        Card.Rank.KING: 10,
    }

    def __init__(self, cards: Card = None):
        self.cards = []

        if cards:
            for card in cards:

                if not isinstance(card, Card):
                    raise TypeError('can only add Card type to hand')

                self.cards.append(card)

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def append(self, card):
        return self.cards.append(card)

    def extend(self, cards):
        return self.cards.extend(cards)

    def pop(self, i):
        return self.cards.pop(i)

    def clear(self):
        self.card_hidden = None
        self.cards.clear()

    def __repr__(self):
        cards = ', '.join(card.format_short() for card in self.cards)
        return f'Hand(cards=[{cards}])'

    def __str__(self):
        return self.__repr__()

    @property
    def value_hard(self):
        val = 0
        for card in self.cards:
            val += self.card_values[card.rank]

        return val

    @property
    def blackjack(self):
        return len(self.cards) == 2 and self.value == 21

    @property
    def value(self):
        ace = False
        val = 0
        for card in self.cards:
            if card.rank == Card.Rank.ACE:
                ace = True
            val += self.card_values[card.rank]
        if ace and val < 12:
            val += 10

        return val


class BlackjackDealerHand(BlackjackHand):
    """dealer specific BlackjackHand subclass"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __iter__(self):
        return islice(self.cards, 1, len(self.cards))

    def iter_all(self):
        return iter(self.cards)

    @property
    def hidden(self):
        if self.cards:
            return self.cards[0]
        else:
            return None

    @property
    def value_hidden_hard(self):
        val = 0
        for card in self:
            val += self.card_values[card.rank]

        return val

    @property
    def value_hidden(self):
        ace = False
        val = 0
        for card in self:
            if card.rank == Card.Rank.ACE:
                ace = True
            val += self.card_values[card.rank]
        if ace and val < 12:
            val += 10

        return val


def main():

    cards = [Card(Card.Rank.KING, Card.Suit.SPADES), Card(Card.Rank.ACE, Card.Suit.SPADES)]
    hand = BlackjackHand(cards)

    print(hand)
    print(f'{hand.blackjack=}')
    print(f'{hand.value=}')
    print(f'{hand.value_hard=}')
    print(f'{hand.value_soft=}')

    print()


    cards = [Card(Card.Rank.KING, Card.Suit.SPADES), Card(Card.Rank.TEN, Card.Suit.SPADES), Card(Card.Rank.ACE, Card.Suit.SPADES)]
    hand = BlackjackDealerHand(cards)

    print(hand)
    print(f'{hand.blackjack=}')
    print(f'{hand.value=}')
    print(f'{hand.value_hard=}')
    print(f'{hand.value_soft=}')

    for card in hand:
        print(f'    {card.format_short()}')


if __name__ == '__main__':
    main()
