# https://lark-parser.readthedocs.io/en/latest/examples/calc.html#sphx-glr-examples-calc-py
from lark import Lark, Transformer, v_args



calc_grammar = """
    ?start: sum
          | NAME "=" sum    -> assign_var

    ?sum: product
        | sum "+" product   -> add
        | sum "*" product   -> mul

    ?product: atom
        | product "/" atom  -> div

    ?atom: NUMBER           -> number
         | "-" atom         -> neg
         | NAME             -> var
         | "(" sum ")"

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE

    %ignore WS_INLINE
"""


@v_args(inline=True)    # Affects the signatures of the methods
class CalculateTree(Transformer):
    from operator import add, sub, mul, truediv as div, neg
    number = float

    def __init__(self):
        self.vars = {}

    def assign_var(self, name, value):
        self.vars[name] = value
        return value

    def var(self, name):
        try:
            return self.vars[name]
        except KeyError:
            raise Exception("Variable not found: %s" % name)


calc_parser = Lark(calc_grammar, parser='lalr', transformer=CalculateTree())
calc = calc_parser.parse


def main():

    with open("full.txt", "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    print(lines)
    p1 = sum(calc(line) for line in lines)
    print(p1)


def test():
    assert calc("1 + 2 * 3 + 4 * 5 + 6") == 71

if __name__ == '__main__':
    test()
    main()