#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day 13
#
from typing import Sequence, Union, Optional, Any
from pathlib import Path
from operator import attrgetter
import time

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        r"""
/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
        """,
        (7, 3)
    ),
]

SAMPLE_CASES2 = [
    (
        r"""
/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
        """,
        (6, 4)
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
    return [line for line in lines if line.strip()]

# Solution

# bearing (0, 1, 2, 3) -> (dRow, dCol)
MOVE = {
    0: (0, 1),
    1: (1, 0),
    2: (0, -1),
    3: (-1, 0),
}


class Cart():
    def __init__(self, loc, bearing):
        self.loc = loc
        self.bearing = bearing
        self._next_turn = -1

    def __str__(self):
        return f"@{self.loc}/{self.bearing}"

    @property
    def xy(self):
        return (self.loc[1], self.loc[0])

    def advance_turn(self):
        if self._next_turn == -1:
            self._next_turn = 0
        elif self._next_turn == 0:
            self._next_turn = 1
        elif self._next_turn == 1:
            self._next_turn = -1
        else:
            raise ValueError(f"cart @{self.loc} has next_turn '{self._next_turn}'")

    def move(self, track):
        """Move, based on our current bearing, and adjust our bearing, based on
        what kind of cell we end up in.
        """
        move = MOVE[self.bearing]
        self.loc = (self.loc[0] + move[0], self.loc[1] + move[1])
        cell = track[self.loc]
        if cell == "+":
            self.bearing = (self.bearing + self._next_turn) % 4
            self.advance_turn()
        elif cell == "-":
            assert self.bearing in (0, 2)
        elif cell == "|":
            assert self.bearing in (1, 3)
        elif cell == "/":
            if self.bearing in (0, 2):
                self.bearing = (self.bearing - 1 ) % 4
            else:
                self.bearing = (self.bearing + 1 ) % 4
        elif cell == "\\":
            if self.bearing in (0, 2):
                self.bearing = (self.bearing + 1 ) % 4
            else:
                self.bearing = (self.bearing - 1 ) % 4
        else:
            raise RuntimeError(f"bad cell @{self.loc} '{cell}'")


def parse_lines(lines):
    nrow, ncol = len(lines), max([len(line) for line in lines])
    track = {}
    carts = []
    for row, line in enumerate(lines):
        for col, symbol in enumerate(line):
            loc = (row, col)
            if symbol == " ":
                continue
            elif symbol in ("-", "|", "+", "\\", "/"):
                track[loc] = symbol
            elif symbol == ">":
                track[loc] = "-"
                carts.append(Cart(loc, 0))
            elif symbol == "<":
                track[loc] = "-"
                carts.append(Cart(loc, 2))
            elif symbol == "^":
                track[loc] = "|"
                carts.append(Cart(loc, 3))
            elif symbol == "v":
                track[loc] = "|"
                carts.append(Cart(loc, 1))
            else:
                raise ValueError(f"unrecognized symbol @({row}, {col}): {symbol}")
    return track, carts

CART_SYMBOL = {
    0: ">",
    1: "v",
    2: "<",
    3: "^",
}

def track_size(track):
    ncol, nrow = -1, -1
    for (r, c) in track.keys():
        ncol = max(ncol, c)
        nrow = max(nrow, r)
    return nrow, ncol

def print_carts(carts):
    print(", ".join(map(str, carts)))

def print_track(track, carts):
    nrow, ncol = track_size(track)
    cart = {v.loc: v.bearing for v in carts}
    for r in range(nrow + 1):
        row = []
        for c in range(ncol + 1):
            pos = (r, c)
            cell = track.get(pos, " ")
            if pos in cart:
                cell = CART_SYMBOL[cart[pos]]
            row.append(cell)
        print("".join(row))
        if r > 50:
            break


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    track, carts = parse_lines(lines)
    ncarts = len(carts)
    nrow, ncol = track_size(track)
    print(f"{ncarts} carts on a {nrow} by {ncol} track")
    final_ticks = 0
    while True:
        # print_carts(carts)
        # print_track(track, carts)
        carts.sort(key=attrgetter('loc'))
        crash = []
        for i in range(ncarts):
            if i in crash:
                continue
            carts[i].move(track)
            for j in range(ncarts):
                if i == j or j in crash:
                    continue
                if carts[i].loc  == carts[j].loc:
                    crash.extend([i, j])
                    break
            if crash:
                continue
        if crash:
            carts = [carts[i] for i in range(ncarts) if i not in crash]
            ncarts = len(carts)
        if ncarts == 1:
            break
        # time.sleep(0.5)
    # print_track(track, carts)
    return carts[0].xy


def solve(lines: Lines) -> int:
    """Solve the problem."""
    track, carts = parse_lines(lines)
    ncarts = len(carts)
    nrow, ncol = track_size(track)
    print(f"{ncarts} carts on a {nrow} by {ncol} track")
    crashed_cart = None
    while not crashed_cart:
        # print('\v')
        # print_carts(carts)
        # print_track(track, carts)
        carts.sort(key=attrgetter('loc'))
        for i in range(ncarts):
            carts[i].move(track)
            if carts[i].loc in [carts[j].loc for j in range(ncarts) if i != j]:
                crashed_cart = carts[i]
                break
        # time.sleep(0.5)
    # print('\v')
    # print_track(track, carts)
    return crashed_cart.xy


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
    assert result == (43, 111)
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
    assert result == (44, 56)
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
