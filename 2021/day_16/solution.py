import dataclasses
import operator
from functools import reduce
from operator import mul
from typing import Optional
from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines[0]


def as_bin(hex_string):
    num_bits = 4 * len(hex_string)
    return bin(int(hex_string, 16))[2:].zfill(num_bits)


@dataclasses.dataclass
class Packet:
    version: int
    type_id: int
    literal: Optional[int] = None
    length_type_id: Optional[int] = None
    subpacket_lengths: Optional[int] = None
    subpackets: list["Packet"] = None


def parse(rest: str, n_max=None) -> tuple[list[Packet], str]:
    packets = []
    n = n_max or 9e999
    while rest:
        try:
            if n == 0:
                break
            packet, rest = parse_next(rest)
            packets.append(packet)
            n -= 1
        except (KeyError, ValueError):
            print(f"finish parse. Rest is '{rest}'")
            rest = ""
            break
    return packets, rest


def parse_next(rest):
    version_str, rest = pop_n(3, rest)
    version = int(version_str, 2)
    type_id_str, rest = pop_n(3, rest)
    type_id = int(type_id_str, 2)
    if type_id == 4:
        # literal
        packet, rest = parse_literal_type_4(rest, type_id, version)
    else:
        # operator
        packet, rest = parse_operator(rest, type_id, version)
    return packet, rest


def parse_operator(rest, type_id, version):
    length_type_id_str, rest = pop_n(1, rest)
    length_type_id = int(length_type_id_str, 2)
    if length_type_id == 0:
        total_length_in_bits_str, rest = pop_n(15, rest)
        total_length_in_bits = int(total_length_in_bits_str, 2)
        subpacket_bits, rest = pop_n(total_length_in_bits, rest)
        subpackets, _ = parse(subpacket_bits)
        packet = Packet(
            version=version,
            type_id=type_id,
            length_type_id=length_type_id,
            subpackets=subpackets,
        )
    elif length_type_id == 1:
        number_of_subpackages_str, rest = pop_n(11, rest)
        number_of_subpackages = int(number_of_subpackages_str, 2)
        subpackets, rest = parse(rest, number_of_subpackages)
        packet = Packet(
            version=version,
            type_id=type_id,
            length_type_id=length_type_id,
            subpackets=subpackets,
        )
    else:
        raise RuntimeError("bad length type id")
    return packet, rest


def pop_n(n, rest):
    return rest[:n], rest[n:]


def parse_literal_type_4(rest, type_id, version):
    fivers = []
    next_fiver, rest = pop_n(5, rest)
    fivers.append(next_fiver)
    while next_fiver[0] == "1":
        next_fiver, rest = pop_n(5, rest)
        fivers.append(next_fiver)
    bin_literal = ""
    for fiver in fivers:
        fours = fiver[1:]
        bin_literal = bin_literal + fours
    literal = int(bin_literal, 2)
    packet = Packet(version=version, type_id=type_id, literal=literal, subpackets=[])

    return packet, rest


def part_1(inp):
    p, rest = parse(as_bin(inp))
    return sum_versions(p)


def sum_versions(package_list):
    s = 0
    for p in package_list:
        s += p.version
        s += sum_versions(p.subpackets)
    return s


def part_2(inp):
    p, rest = parse(as_bin(inp))
    return calculate(p[0])


def calculate(p: Packet):
    if p.type_id == 4:
        return p.literal
    elif p.type_id == 0:
        # sum
        return sum(calculate(sub_p) for sub_p in p.subpackets)
    elif p.type_id == 1:
        # product
        prod = 1
        for sub_p in p.subpackets:
            prod *= calculate(sub_p)
        return prod
    elif p.type_id == 2:
        # minimum
        return min(calculate(sub_p) for sub_p in p.subpackets)
    elif p.type_id == 3:
        return max(calculate(sub_p) for sub_p in p.subpackets)
    elif p.type_id == 5:
        return calculate(p.subpackets[0]) > calculate(p.subpackets[1])
    elif p.type_id == 6:
        return calculate(p.subpackets[0]) < calculate(p.subpackets[1])
    elif p.type_id == 7:
        return calculate(p.subpackets[0]) == calculate(p.subpackets[1])
    else:
        raise RuntimeError(p.type_id)


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    inp = read_input(input_file)
    p1 = part_1(inp)
    print(f"Solution to part 1: {p1}")

    # part 2
    inp = read_input(input_file)
    p2 = part_2(inp)
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_sample_1(self):
    # literal example
    packets, rest = parse(as_bin("D2FE28"))
    self.assertEqual(2021, packets[0].literal)

    # operator type 0 example
    packets, rest = parse(as_bin("38006F45291200"))
    self.assertEqual(2, len(packets[0].subpackets))

    # operator type 1 example
    packets, rest = parse(as_bin("EE00D40C823060"))
    self.assertEqual(3, len(packets[0].subpackets))

    self.assertEqual(16, part_1("8A004A801A8002F478"))
    self.assertEqual(12, part_1("620080001611562C8802118E34"))
    self.assertEqual(23, part_1("C0015000016115A2E0802F182340"))
    self.assertEqual(31, part_1("A0016C880162017C3686B18A3D4780"))

    pass


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
