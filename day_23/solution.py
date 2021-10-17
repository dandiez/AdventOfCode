import asyncio
import dataclasses
from typing import Dict
from unittest import TestCase

from day_09.solution import IntcodeComputer
import logging

logger = logging.getLogger("day_23")

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


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [int(val) for val in lines[0].split(",")]  # parse here...
    return inp


@dataclasses.dataclass
class Package:
    destination: int
    x: int
    y: int


class Network:
    def __init__(self, inp, num_computers = 50):
        self.computers: Dict[int, IntcodeComputer] = {
            n: IntcodeComputer(inp) for n in range(num_computers)
        }
        self.computer_tasks = {}
        self.build_packages_helper_tasks = {}
        self.package_sender_task = None
        self.full_packages_queue: asyncio.Queue[Package] = asyncio.Queue()
        self.part_1_answer = asyncio.Queue()

    def configure(self):
        for n, computer in self.computers.items():
            computer.input_queue.put_nowait(n)
            self.build_packages_helper_tasks[n] = asyncio.create_task(
                self.build_packages_helper(
                    computer.output_queue, self.full_packages_queue, n
                )
            )
        self.package_sender_task = asyncio.create_task(self.package_sender())

    async def package_sender(self):
        print("Started package sender")
        while True:
            # need small sleep or otherwise it deadlocks
            await asyncio.sleep(0.001)
            await self.forward_ready_packages_to_destination()
            await self.feed_computers_with_empty_input_queues()

    async def forward_ready_packages_to_destination(self):
        while not self.full_packages_queue.empty():
            package: Package = await self.full_packages_queue.get()
            print(f"Received package {package}")
            if package.destination == 255:
                await self.part_1_answer.put(package.y)
            try:
                await self.computers[package.destination].input_queue.put(package.x)
                await self.computers[package.destination].input_queue.put(package.y)
            except KeyError:
                logger.error(f"Unknown destination {package.destination}")

    async def feed_computers_with_empty_input_queues(self):
        for n, computer in self.computers.items():
            if computer.input_queue.empty():
                await computer.input_queue.put(-1)

    async def start_network_loop(self):
        self.configure()
        self.computer_tasks = {
            n: asyncio.create_task(computer.execute())
            for n, computer in self.computers.items()
        }
        return await self.part_1_answer.get()

    async def build_packages_helper(
        self,
        queue_partial_packages: asyncio.Queue[int],
        queue_full_packages: asyncio.Queue[Package],
        computer_id
    ):
        print(f"Starting package helper for computer {computer_id}")
        while True:
            destination_id = await queue_partial_packages.get()
            x = await queue_partial_packages.get()
            y = await queue_partial_packages.get()
            package = Package(x=x, y=y, destination=destination_id)
            await queue_full_packages.put(package)

async def main_loop(inp):
    network = Network(inp)
    return await network.start_network_loop()

def part_1(inp):
    return asyncio.run(main_loop(inp))


def part_2(inp):
    pass


def test_sample_1(self):
    pass


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
