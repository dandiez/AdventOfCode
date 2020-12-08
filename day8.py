import re
import networkx as nx
from parse import *
import copy

with open("input8.txt") as f:
    lines =[line.strip() for line in f.readlines() if line.strip()]

operations = {n:parse("{} {:d}", lines[n]).fixed for n in range(len(lines))}

class InfiniteLoop(Exception):
    pass

def calculate(operations):
    s=set()
    n=0
    tot=0
    while n not in s:
        if n>= len(operations.keys()):
            print("reached the end...")
            return tot
        s.add(n)
        ins, amount = operations[n]
        if ins=="nop":
            n+=1
        elif ins=="acc":
            tot+=amount
            n+=1
        elif ins=="jmp":
            n+=amount
    raise InfiniteLoop(f"Infinite recursion detected at value {tot}")

# part 1
# print(calculate(operations))

# part 2
def fix_attempts(operations):
    orig_operations = copy.deepcopy(operations)
    for n, (ins, amount) in orig_operations.items():
        operations = copy.deepcopy(orig_operations)
        if ins=="nop":
            operations[n]=("jmp", amount)
            yield operations
        elif ins=="jmp":
            operations[n]=("nop", amount)
            yield operations
        

def fix_program_and_output_result(operations):
    for attempt in fix_attempts(operations):
        try:
            tot = calculate(attempt)
        except InfiniteLoop:
            continue
        else:
            return tot
print(fix_program_and_output_result(operations))
