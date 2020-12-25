from unittest import TestCase

BIG = 20201227


def loop_it_once(sn, num):
    val = num * sn
    return val % BIG


MAX_IT = 1000000000


def get_loop_size(pk, sn=7, num=1):
    for loop_size in range(1, MAX_IT + 1):
        num = loop_it_once(sn, num)
        if num == pk:
            print(f"found pk {pk} for loop size {loop_size}")
            return loop_size
        else:
            pass
            # print(f"pk {pk} does not match {num} for loop size {loop_size}")
    raise Exception("loop size not found")


def transform(sn, ls, num=1):
    for n in range(ls):
        num = loop_it_once(sn, num=num)
    return num


def main(input):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    cpk, dpk = input

    cls = get_loop_size(cpk)
    dls = get_loop_size(dpk)
    enc_k_1 = transform(dpk, cls)
    enc_k_2 = transform(cpk, dls)
    assert enc_k_1 == enc_k_2

    p1 = enc_k_1
    p2 = None
    print(f"Solution to part 1: {p1}")
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_samples(self):
    input = (5764801, 17807724)  # card, door pk
    p1, p2 = main(input)
    self.assertEqual(14897079, p1)
    # self.assertEqual( , p2)
    print("***Tests passed so far***")


if __name__ == "__main__":
    test_samples(TestCase())
    input = (14788856, 19316454)
    p1, p2 = main(input)
    assert p1 == 545789
