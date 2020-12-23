import itertools
from unittest import TestCase


def get_destination(cups, current, pick_up):
    d = current - 1
    remaining = list(set(cups).difference(set(pick_up)))
    min_label = min(cups)
    max_label = max(cups)
    while d not in remaining:
        d -= 1
        if d < min_label:
            d = max_label
    return d


def main(input_file, moves):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    inp = input_file
    cups = [int(c) for c in list(inp)]
    id = 0
    for m in range(1, moves + 1):
        print(f"move {m}")
        print(f"cups: {cups}")
        current_cup = cups[id]
        print(f"current cup with id {id} is ({current_cup})")
        pick_up = cups[1:4]
        print(f"pick up: {pick_up}")
        destination = get_destination(cups, current_cup, pick_up)
        print(f"destination cup is {destination}")
        remaining_cups = cups[4:]
        print(f"remaining cups are {remaining_cups}")
        destination_position = remaining_cups.index(destination)
        remaining_cups=remaining_cups[:destination_position+1] + pick_up + remaining_cups[destination_position+1:]
        print(f"remaining cups with picked up inserted {remaining_cups}")
        remaining_cups.append(current_cup)
        cups = remaining_cups
    final = cups
    print(f"final are {cups}")

    p1 = "".join([str(n) for n in itertools.islice(itertools.cycle(cups), cups.index(1)+1, cups.index(1)+len(cups))])
    p2 = None
    print(f"Solution to part 1: {p1}")
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_samples(self):
    input_file = "389125467"
    p1, p2 = main(input_file, 10)
    self.assertEqual("92658374", p1)
    p1, p2 = main(input_file, 100)
    self.assertEqual("67384529", p1)
    print("***Tests passed so far***")


if __name__ == "__main__":
    test_samples(TestCase())
    main("562893147", 100)
