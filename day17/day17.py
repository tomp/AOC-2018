#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day 17
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
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
        """,
        57
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
    return filter_blank_lines(text.split("\n"))

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]


# Solution

Cell = str

SAND, CLAY, FLOW, STILL = ".", "#", "|", "~"
DOTDOT = ".."
XDIM, YDIM = "x", "y"

@dataclass(order=True, frozen=True)
class Pos():
    row: int
    col: int

    def __str__(self) -> str:
        return f"({self.row},{self.col})"

    def neighbors(self) -> "List[Pos]":
        return [
            Pos(self.row, self.col + 1),
            Pos(self.row + 1, self.col),
            Pos(self.row, self.col - 1),
            Pos(self.row - 1, self.col),
        ]

LINE_RE = re.compile(r"""
    (?P<dim1>[xy])=(?P<range1>(?:\d+|\d+[.][.]\d+)) ,\s
    (?P<dim2>[xy])=(?P<range2>(?:\d+|\d+[.][.]\d+)) $
    """, re.VERBOSE)

def list_vals(range_text: str) -> List[int]:
    if DOTDOT in range_text:
        a, b = range_text.split(DOTDOT)
        return list(range(int(a), int(b)+1))
    return [int(range_text)]


class Board():
    grid: dict[Pos, Cell]

    def __init__(self, cells):
        self.grid = cells
        self.rowmax = max([v.row for v in self.grid.keys()])
        self.rowmin = min([v.row for v in self.grid.keys()])
        self.colmax = max([v.col for v in self.grid.keys()])
        self.colmin = min([v.col for v in self.grid.keys()])

    @classmethod
    def from_lines(cls, lines, **kwargs) -> "Board":
        grid = defaultdict(lambda : SAND)
        grid[Pos(0, 500)] = FLOW
        for line in lines:
            print(f">>> {line}")
            m = LINE_RE.match(line)
            if not m:
                raise ValueError("unparseable line: '{line}'")
            dim1, range1, dim2, range2 = m.groups()

            vals1 = list_vals(range1)
            vals2 = list_vals(range2)
            if dim1 == XDIM:
                xvals, yvals = vals1, vals2
            else:
                xvals, yvals = vals2, vals1

            for x in xvals:
                for y in yvals:
                    grid[Pos(y, x)] = CLAY

        return cls(grid, **kwargs)

    def print(self, title="", overlay=None):
        if title:
            print(title)
        for r in range(self.rowmin, self.rowmax+2):
            row = []
            for c in range(self.colmin-1, self.colmax+2):
                pos = Pos(r, c)
                val = self.grid[pos][0]
                if overlay and pos in overlay:
                    val = overlay[pos]
                row.append(val)
            print("".join(row))


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    return 0

def solve(lines: Lines) -> int:
    """Solve the problem."""
    board = Board.from_lines(lines)
    board.print(title="Initially")
    return 0


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, expected in SAMPLE_CASES:
        lines = load_text(text)
        result = solve(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    for text, expected in SAMPLE_CASES2:
        lines = load_text(text)
        result = solve2(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines)
    print(f"result is {result}")
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    # example2()
    # part2(input_lines)
