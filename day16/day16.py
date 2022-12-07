#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day 16
#
from typing import Sequence, Union, Optional, Any, List, Dict
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]
        """,
        3
    ),
]

Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

def load_input(infile: str) -> Lines:
    return load_text(Path(infile).read_text())

def sample_case(idx: int = 0) -> tuple[Lines, int]:
    text, expected = SAMPLE_CASES[idx]
    lines = load_text(text)
    return lines, expected

def load_text(text: str) -> Lines:
    return [line.strip() for line in text.strip("\n").split("\n")]

def parse_sections(lines: Lines) -> Sections:
    result = []
    sect = []
    for line in lines:
        line = line.strip()
        if not line:
            if sect:
                result.append(sect)
            sect = []
        else:
            sect.append(line)
    if sect:
        result.append(sect)
    return result


# Solution

Opcode = str

OPCODES: List[Opcode] = [
    "addr",
    "addi",
    "mulr",
    "muli",
    "banr",
    "bani",
    "borr",
    "bori",
    "setr",
    "seti",
    "gtir",
    "gtri",
    "gtrr",
    "eqir",
    "eqri",
    "eqrr",
]

@dataclass
class Instruction():
    """A single instruction for the computing device."""
    op: Opcode
    A: Union[str, int]  # input A
    B: Union[str, int]  # input B
    C: Union[str, int]  # output


class Device():
    """A computing device with four numeric registers and 16 instructions."""
    def __init__(
        self,
        prog: Optional[list[Instruction]] = None,
        reg: Optional[list[int]] = None
    ):
        self.prog = []
        self.reg = [0, 0, 0, 0]
        if prog:
            self.prog = list(prog)
        if reg:
            self.reg = list(reg)
        self.pc = 0

    def load_prog(self, lines: list[str]):
        self.prog = []
        for line in lines:
            line = line.replace(",", " ")
            op, a, b, c, = line.split()
            self.prog.append(Instruction(op, int(a), int(b), int(c)))
        self.pc = 0
        return self

    def run(self):
        while 0<= self.pc < len(self.prog):
            self.step()

    def step(self):
        """Excute a single instruction."""
        ins = self.prog[self.pc]
        if ins.op == "addr":
            self.reg[ins.C] = self.reg[ins.A] + self.reg[ins.B]
        elif ins.op == "addi":
            self.reg[ins.C] = self.reg[ins.A] + ins.B
        elif ins.op == "mulr":
            self.reg[ins.C] = self.reg[ins.A] * self.reg[ins.B]
        elif ins.op == "muli":
            self.reg[ins.C] = self.reg[ins.A] * ins.B
        elif ins.op == "banr":
            self.reg[ins.C] = self.reg[ins.A] & self.reg[ins.B]
        elif ins.op == "bani":
            self.reg[ins.C] = self.reg[ins.A] & ins.B
        elif ins.op == "borr":
            self.reg[ins.C] = self.reg[ins.A] | self.reg[ins.B]
        elif ins.op == "bori":
            self.reg[ins.C] = self.reg[ins.A] | ins.B
        elif ins.op == "setr":
            self.reg[ins.C] = self.reg[ins.A]
        elif ins.op == "seti":
            self.reg[ins.C] = ins.A
        elif ins.op == "gtir":
            self.reg[ins.C] = int(ins.A > self.reg[ins.B])
        elif ins.op == "gtri":
            self.reg[ins.C] = int(self.reg[ins.A] > ins.B)
        elif ins.op == "gtrr":
            self.reg[ins.C] = int(self.reg[ins.A] > self.reg[ins.B])
        elif ins.op == "eqir":
            self.reg[ins.C] = int(ins.A == self.reg[ins.B])
        elif ins.op == "eqri":
            self.reg[ins.C] = int(self.reg[ins.A] == ins.B)
        elif ins.op == "eqrr":
            self.reg[ins.C] = int(self.reg[ins.A] == self.reg[ins.B])
        else:
            raise ValueError(f"Unrecognized opcode '{ins.op}'")
        self.pc += 1


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    return 0


def parse_sample(lines):
    reg, ins, expected = [], [], []

    m = re.match(r"Before: +\[(.*)\]$", lines[0])
    reg = list(map(int, m.group(1).replace(",", " ").split()))

    words = lines[1].split()
    ins = Instruction(
        words[0], int(words[1]), int(words[2]), int(words[3])
    )

    m = re.match(r"After: +\[(.*)\]$", lines[2])
    expected = list(map(int, m.group(1).replace(",", " ").split()))

    return reg, ins, expected


def matching_opcodes(sample) -> List[str]:
    """Find the number of opcodes that match the given sample."""
    reg, ins, expected = parse_sample(sample)
    numcode = int(ins.op)
    matches = []
    for opcode in OPCODES:
        ins.op = opcode
        dev = Device(prog=[ins], reg=reg)
        dev.step()
        if dev.reg == expected:
            matches.append(opcode)
    return numcode, matches


def solve2(parts) -> int:
    """Solve the problem."""
    samples = parts[:-1]
    lines = parts[-1]

    opcode = {}
    for sample in samples:
        numcode, matches = matching_opcodes(sample)
        assert len(matches) > 0
        if numcode not in opcode:
            opcode[numcode] = set(matches)
        else:
            opcode[numcode] &= set(matches)

    # for numcode, matches in opcode.items():
    #     if matches:
    #         print(f"{numcode} -> {list(matches)}")

    strcode = {}
    assignments = True
    while assignments:
        op = None
        assignments = False
        for numcode, matches in opcode.items():
            if len(matches) == 1:
                op = matches.pop()
                strcode[numcode] = op
                # print(f"ASSIGN {numcode} -> {op}")
                assignments = True
                break
        for matches in opcode.values():
            if matches and op in matches:
                matches.remove(op)

    # for numcode, op in sorted(strcode.items()):
    #     print(f"{numcode} -> {op}")

    prog = []
    for line in lines:
        vals = list(map(int, line.replace(",", " ").split()))
        vals[0] = strcode[vals[0]]
        prog.append(Instruction(*vals))

    dev = Device(prog=prog)
    dev.run()

    return dev.reg[0]


def solve(samples) -> int:
    """Solve the problem."""
    result = 0
    for sample in samples:
        _, matches = matching_opcodes(sample)
        if len(matches) >= 3:
          result += 1
    return result


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    text, expected = SAMPLE_CASES[0]
    sample = load_text(text)
    _, matches = matching_opcodes(sample)
    result = len(matches)
    print(f"'{text}' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    parts = parse_sections(lines)
    result = solve(parts[:-1])
    print(f"result is {result}")
    assert result == 651
    print("= " * 32)


# PART 2

def part2(lines: Lines) -> None:
    print("PART 2:")
    parts = parse_sections(lines)
    result = solve2(parts)
    print(f"result is {result}")
    assert result == 706
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    part2(input_lines)
