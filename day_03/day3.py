with open("input3.txt") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]


def num_trees(_r, _d, lines):
    s = 0
    n = 0
    m = 0
    w = len(lines[0])
    for line in lines:
        n += _d
        m += _r
        m = m % w
        if n >= (len(lines)):
            continue
        if lines[n][m] == "#":
            s += 1
    print("Trees found", s)
    return s


mult = 1
for _r, _d in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    mult *= num_trees(_r, _d, lines)
    print(mult)
