import itertools

with open("full.txt") as f:
    nums = [int(line.strip()) for line in f.readlines()]
print("part 1: ", sum(nums))
s = 0
mem = set()
nums_it = itertools.cycle(nums)
while s not in mem:
    mem.add(s)
    s += next(nums_it)
print("part 2: ", s)
