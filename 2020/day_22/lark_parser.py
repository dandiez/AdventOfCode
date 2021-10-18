import lark
from lark import Transformer

grammar = r"""
    start: deck _NEWLINE _NEWLINE (deck)*
    deck: "Player " id ":" _NEWLINE cards
    _NEWLINE: "\n"
    id: number -> player_id
    cards: number ("\n" number)*
    number: SIGNED_NUMBER
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS
"""


class ReadDecks(Transformer):
    def start(self, items):
        print("Start items are", items)
        print("will return ", dict(items))
        return dict(items)

    def deck(self, items):
        print("Deck items are ", items)
        print("will return ", tuple(items))
        return tuple(items)

    def cards(self, items):
        print("Card items are ", items)
        print("will return ", list(items))
        return list(items)

    def player_id(self, id):
        print("Player id is ", id)
        print("will return ", int(id[0]))
        (id,) = id
        return int(id)

    def number(self, n):
        print("Number is ", n)
        (n,) = n
        print("will return ", n)
        return int(n)


with open("sample_1.txt") as f:
    text = f.read()

parser = lark.Lark(grammar)
p = parser.parse(text)
print(p.pretty())
decks = ReadDecks().transform(p)
print(decks)
assert decks == {1: [9, 2, 6, 3, 1], 2: [5, 8, 4, 7, 10]}
