#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day 17
#
from typing import Sequence, Union, Optional, Any, List, Dict, Tuple
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
    (
        """
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..17
x=514, y=10..17
x=510, y=12..14
x=512, y=12..14
y=14, x=510..512
y=17, x=498..514
        """,
        158
    ),
]

SAMPLE_CASES2 = [
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
        29
    ),
    (
        """
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..17
x=514, y=10..17
x=510, y=12..14
x=512, y=12..14
y=14, x=510..512
y=17, x=498..514
        """,
        112
    ),
]



Lines = Sequence[str]
Sections = Sequence[Lines]


LINE_RE = re.compile(r"""
    (?P<dim1>[xy])=(?P<range1>(?:\d+|\d+[.][.]\d+)) ,\s
    (?P<dim2>[xy])=(?P<range2>(?:\d+|\d+[.][.]\d+)) $
    """, re.VERBOSE)


# Utility functions

def load_input(infile: str) -> Lines:
    return load_text(Path(infile).read_text())

def sample_case(idx: int = 0) -> Tuple[Lines, int]:
    text, expected = SAMPLE_CASES[idx]
    lines = load_text(text)
    return lines, expected

def load_text(text: str) -> Lines:
    return filter_blank_lines(text.split("\n"))

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]


# Solution

SAND, CLAY, SPRING, FLOW, STILL = ".", "#", "+", "|", "~"
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

    def above(self) -> "Pos":
        return Pos(self.row - 1, self.col)

    def below(self) -> "Pos":
        return Pos(self.row + 1, self.col)

    def right(self) -> "Pos":
        return Pos(self.row, self.col + 1)

    def left(self) -> "Pos":
        return Pos(self.row, self.col - 1)


Cell = str


def list_vals(range_text: str) -> List[int]:
    if DOTDOT in range_text:
        a, b = range_text.split(DOTDOT)
        assert int(a) < int(b)
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

        self.clay_rowmax = max([pos.row for pos, cell in self.grid.items() if cell == CLAY])
        self.clay_rowmin = min([pos.row for pos, cell in self.grid.items() if cell == CLAY])

        self.fresh_flow = []
        for pos, cell in self.grid.items():
            if cell == SPRING:
                self.fresh_flow.append(pos)

    @classmethod
    def from_lines(cls, lines, **kwargs) -> "Board":
        grid = defaultdict(lambda : SAND)
        grid[Pos(0, 500)] = SPRING
        for line in lines:
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
        for r in range(self.rowmin, self.rowmax+1):
            row = []
            for c in range(self.colmin-1, self.colmax+2):
                pos = Pos(r, c)
                val = self.grid[pos][0]
                if overlay and pos in overlay:
                    val = overlay[pos]
                row.append(val)
            print("".join(row))

    def above(self, pos) -> Tuple[Pos, Cell]:
       loc = Pos(pos.row - 1, pos.col)
       return loc, self.grid[loc]

    def below(self, pos) -> Tuple[Pos, Cell]:
        loc = Pos(pos.row + 1, pos.col)
        return loc, self.grid[loc]

    def right(self, pos) -> Tuple[Pos, Cell]:
        loc = Pos(pos.row, pos.col + 1)
        return loc, self.grid[loc]

    def left(self, pos) -> Tuple[Pos, Cell]:
        loc = Pos(pos.row, pos.col - 1)
        return loc, self.grid[loc]

    def count_water(self) -> List[Pos]:
        result = []
        count = 0
        for pos, cell in sorted(self.grid.items()):
            if (cell in (STILL, FLOW) and
                pos.row >= self.clay_rowmin and
                pos.row <= self.clay_rowmax
            ):
                count += 1
                # print(f"WATER:  {count:4d}:  {pos} '{cell}'")
                result.append(pos)
        result.sort()
        return result

    def count_still_water(self) -> List[Pos]:
        result = []
        count = 0
        for pos, cell in sorted(self.grid.items()):
            if (cell == STILL and
                pos.row >= self.clay_rowmin and
                pos.row <= self.clay_rowmax
            ):
                count += 1
                # print(f"WATER:  {count:4d}:  {pos} '{cell}'")
                result.append(pos)
        result.sort()
        return result

    def in_basin(self, pos) -> bool:
        left, right = pos.col, pos.col
        for col in range(pos.col - 1, self.colmin - 1, -1):
            if self.grid[Pos(pos.row+1, col)] == SAND:
                break
            if self.grid[Pos(pos.row, col)] == CLAY:
                left = col
                break

        for col in range(pos.col + 1, self.colmax + 1):
            if self.grid[Pos(pos.row+1, col)] == SAND:
                break
            if self.grid[Pos(pos.row, col)] == CLAY:
                right = col
                break

        basin = (left < pos.col) and (right > pos.col)
        return basin, left+1, right-1

    def step(self) -> bool:
        """Propagate the system for one time step.  Return True if not cells changed."""
        cells = self.fresh_flow
        self.fresh_flow = []
        for pos in cells:
            if pos.row == self.rowmax:
                continue

            cell = self.grid[pos]
            # print(f"--- >> {pos} {cell}")
            if not cell in (SPRING, FLOW):
                continue

            pos_down, cell_down = self.below(pos)
            if cell_down == SAND:
                self.grid[pos_down] = FLOW
                self.fresh_flow.append(pos_down)
            elif cell_down in (CLAY, STILL):
                basin, left, right = self.in_basin(pos)
                if basin:
                    for col in range(left, right+1):
                        self.grid[Pos(pos.row, col)] = STILL
                        if self.grid[Pos(pos.row - 1, col)] == FLOW:
                            self.fresh_flow.append(Pos(pos.row - 1, col))
                else:
                    pos_left, cell_left = self.left(pos)
                    if cell_left == SAND:
                        self.grid[pos_left] = FLOW
                        self.fresh_flow.append(pos_left)
                    pos_right, cell_right = self.right(pos)
                    if cell_right == SAND:
                        self.grid[pos_right] = FLOW
                        self.fresh_flow.append(pos_right)
        return len(self.fresh_flow) == 0

    def run(self, max_steps: int = 0) -> int:
        """Propagate the system until it reaches steady state, or the max_steps have
        been exceeded.  The number of steps taken is returned.
        """
        done = False
        steps = 0
        while not done:
            steps += 1
            if max_steps and steps > max_steps:
                break 
            # print(f"--- step {steps}")
            done = self.step()
            # self.print(title=f"Step {steps}:")
        return steps


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    board = Board.from_lines(lines)
    # board.print(title="initially")
    board.run()
    # board.print(title="final:")
    water = board.count_still_water()
    return len(water)

def solve(lines: Lines) -> int:
    """Solve the problem."""
    board = Board.from_lines(lines)
    # board.print(title="initially")
    board.run()
    # board.print(title="final:")
    water = board.count_water()
    return len(water)


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
    assert result == 27331
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
    assert result == 22245
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
