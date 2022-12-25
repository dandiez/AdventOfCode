import dataclasses
from functools import lru_cache
from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines


@dataclasses.dataclass
class SnafuLimits:
    """min and max numbers that can be stored with n digits."""

    n: int
    min_limit: int
    max_limit: int
    pow_factor: int

    def contains(self, numb: int):
        return self.min_limit <= numb <= self.max_limit


@lru_cache(None)
def limits(n: int) -> SnafuLimits:
    if n < 0:
        return SnafuLimits(n=n, pow_factor=0, min_limit=0, max_limit=0)
    if n == 0:
        return SnafuLimits(n=n, pow_factor=5**n, min_limit=-2, max_limit=2)
    else:
        return SnafuLimits(
            n=n,
            pow_factor=5**n,
            min_limit=-2 * 5**n + limits(n - 1).min_limit,
            max_limit=2 * 5**n + limits(n - 1).max_limit,
        )


@dataclasses.dataclass
class SNAFU:
    char_to_dec: dict[str, int] = None
    dec_to_char: dict[int, str] = None

    def __post_init__(self):
        self.char_to_dec = {
            "2": 2,
            "1": 1,
            "0": 0,
            "-": -1,
            "=": -2,
        }
        self.dec_to_char = {d: c for c, d in self.char_to_dec.items()}

    def to_decimal(self, snafu: str):
        return sum(
            self.char_to_dec[c] * 5**n for c, n in zip(snafu[::-1], range(len(snafu)))
        )

    def to_snafu(self, dec: int) -> str:
        n = self.get_number_of_digits_needed(dec)
        factors = []
        number = dec
        for n in range(n, -1, -1):
            for digit in self.char_to_dec.values():
                reminder = number - digit * limits(n).pow_factor
                if limits(n - 1).contains(reminder):
                    factors.append(digit)
                    number = reminder
                    break
        s = [self.dec_to_char[f] for f in factors]
        return "".join(s)

    def get_number_of_digits_needed(self, dec) -> int:
        N = 10000
        for n in range(N):
            lims = limits(n)
            if lims.contains(dec):
                break
        else:
            raise ValueError(
                f"Number cannot be represented with {N} digits or less. Increase N."
            )
        return n


def part_1(inp):
    in_dec = sum(SNAFU().to_decimal(s) for s in inp)
    return SNAFU().to_snafu(in_dec)


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    inp = read_input(input_file)
    p1 = part_1(inp)
    print(f"Solution to part 1: {p1}")
    return p1


def test_sample_1(self):
    inp = read_input("sample_1")
    self.assertEqual(4890, sum(SNAFU().to_decimal(s) for s in inp))
    self.assertEqual("2=-1=0", SNAFU().to_snafu(4890))


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    print("*** solving main ***")
    main("input")
