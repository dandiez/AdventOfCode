import lark
from lark import Transformer

grammar = r"""
    start: ticket_fields _NEWLINE _NEWLINE your_ticket _NEWLINE _NEWLINE nearby_tickets
    ticket_fields: ticket_field (_NEWLINE ticket_field)*
    ticket_field: name ": " ranges
    ranges: range (" or " range)*
    name: WORD_SP 
    range: number "-" number
    number: SIGNED_NUMBER
    your_ticket: "your ticket:\n" number ("," number)*
    nearby_tickets: "nearby tickets:\n" ticket (_NEWLINE ticket)*
    ticket: number ("," number)*
    WORD_SP: WORD (" " WORD)*
    _NEWLINE: "\n"
    %import common.WORD
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS
    
"""


class ReadTickets(Transformer):
    def start(self, items):
        ret = {
            "ticket_fields": items[0],
            "your_ticket": items[1],
            "nearby_tickets": items[2],
        }
        return ret

    name = lambda self, items: str(items[0])
    number = lambda self, items: int(items[0])
    ticket_fields = dict
    ticket_field = list
    range = tuple
    ranges = list
    ticket = list
    nearby_tickets = list
    your_ticket = list


with open("sample_1_for_parser.txt") as f:
    text = f.read()

parser = lark.Lark(grammar)
p = parser.parse(text)
print(p.pretty())
tickets = ReadTickets().transform(p)
print(tickets)

assert tickets == {
    "ticket_fields": {
        "class": [(1, 3), (5, 7)],
        "departure location": [(25, 568), (594, 957)],
        "row": [(6, 11), (33, 44)],
        "seat": [(13, 40), (45, 50)],
    },
    "your_ticket": [7, 1, 14],
    "nearby_tickets": [[7, 3, 47], [40, 4, 50], [55, 2, 20], [38, 6, 12]],
}
