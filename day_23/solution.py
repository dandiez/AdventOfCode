from unittest import TestCase


def get_destination(current, pick_up, min_cup, max_cup):
    c = current.value
    pu = set(c.value for c in pick_up)
    d = c - 1
    if d < min_cup:
        d = max_cup
    while d in pu:
        d -= 1
        if d < min_cup:
            d = max_cup
    return d


class Element():
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class LinkedList():
    def __init__(self, input):
        self.elements = dict()
        start = Element(-1)  # dummy
        last = start
        for n in input:
            e = Element(n)
            self.link_elements(last, e)
            last = e
            self.elements[n] = e
        self.min_val = min(v.value for v in self.elements.values())
        self.max_val = max(v.value for v in self.elements.values())
        self.num_elements = len(self.elements.keys())

        # redefine start
        start = start.next

        # make it circular
        self.link_elements(last, start)
        self.start = start
        self.current = None

        print(f"Linked list has been initialised with {self.num_elements} elements"
              f" with values in range {self.min_val} to {self.max_val}.")

    @staticmethod
    def link_elements(e, next_e):
        e.next = next_e
        next_e.prev = e

    def extract_pick_up(self):
        old_cur = self.current
        pick_up = [next(self) for _ in range(3)]
        new_next_to_current = next(self)
        self.link_elements(old_cur, new_next_to_current)
        self.link_elements(pick_up[-1], pick_up[0])
        self.current = new_next_to_current.prev
        return pick_up

    def insert_pick_up(self, pick_up, destination):
        destination_cup = self.elements[destination]
        next_to_destination = destination_cup.next
        self.link_elements(destination_cup, pick_up[0])
        self.link_elements(pick_up[-1], next_to_destination)

    def print_from_current(self):
        c = self.current
        print(f"({c.value}) ", end=", ")
        e = self.current.next
        while e is not c:
            print(e.value, end=", ")
            e = e.next

    def __next__(self):
        if self.current is None:
            self.current = self.start
        else:
            self.current = self.current.next
        return self.current

    def p1_solution(self):
        e = self.elements[1].next
        p1 = ""
        for _ in range(self.num_elements - 1):
            p1 += str(e.value)
            e = e.next
        return p1

    def p2_solution(self):
        e = self.elements[1].next
        return e.value * e.next.value


def main(input_file, moves, part_2=False):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    inp = input_file
    cups = [int(c) for c in list(inp)]
    if part_2:
        cups.extend(list(range(max(cups) + 1, 1000000 + 1)))
        assert max(cups) == 1000000
        assert len(cups) == 1000000
        print("starting part 2...")

    cup_list = LinkedList(cups)

    for m in range(1, moves + 1):
        # print(f"--- move {m} ---")
        current_cup = next(cup_list)
        # print(f"current cup is ({current_cup.value})")
        # print(f"cups are {cup_list.print_from_current()}")
        pick_up = cup_list.extract_pick_up()
        # print(f"pick up: {[c.value for c in pick_up]}")
        # print(f"cups are {cup_list.print_from_current()}")
        destination = get_destination(current_cup, pick_up, min_cup=cup_list.min_val,
                                      max_cup=cup_list.max_val)
        # print(f"destination cup is {destination}")
        cup_list.insert_pick_up(pick_up, destination)
        # print(f"cups are {cup_list.print_from_current()}")
    final = cup_list
    # print(f"final are {cups}")
    if part_2:
        p1 = None
        p2 = final.p2_solution()
    else:
        p1 = final.p1_solution()
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
    p1, p2 = main(input_file, 10000000, part_2=True)
    self.assertEqual(149245887792, p2)
    print("***Tests passed so far***")


if __name__ == "__main__":
    test_samples(TestCase())
    main("562893147", 100)
    main("562893147", 10000000, part_2=True)
