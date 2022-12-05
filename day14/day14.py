#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day 14
#
from typing import Sequence, Union, Optional, Any
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    ["9", "5158916779"],
    ["5", "0124515891"],
    ["18", "9251071085"],
    ["2018", "5941429882"],
]

SAMPLE_CASES2 = [
    ["51589", 9],
    ["01245", 5],
    ["92510", 18],
    ["59414", 2018],
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

## Use these if blank lines should be discarded.

def load_text(text: str) -> Lines:
    return filter_blank_lines(text.split("\n"))

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]


# Solution

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    target = lines[0].strip()
    print(f"target: {target}")
    scores = [3, 7]
    elf1, elf2 = 0, 1
    while True:
        tail = ''.join(list(map(str, scores[-10:])))
        # print(f"{elf1}:{scores[elf1]}, {elf2}:{scores[elf2]} :: {tail}")
        if target in tail:
            break
        elf1, elf2 = propagate(scores, elf1, elf2)
    position = len(scores) - 10 + tail.index(target)
    return position

def propagate(scores, elf1, elf2):
    """ """
    sum12 = scores[elf1] + scores[elf2]
    if sum12 < 10:
        scores.append(sum12)
    else:
        scores.append(sum12 // 10)
        scores.append(sum12 % 10)
    elf1 = (elf1 + scores[elf1] + 1) % len(scores)
    elf2 = (elf2 + scores[elf2] + 1) % len(scores)
    return elf1, elf2


def solve(lines: Lines) -> int:
    """Solve the problem."""
    target = int(lines[0])
    print(f"target: {target}")
    scores = [3, 7]
    elf1, elf2 = 0, 1
    while len(scores) < target + 10:
        # print(f"{elf1}:{scores[elf1]}, {elf2}:{scores[elf2]} :: {' '.join(list(map(str, scores)))}")
        elf1, elf2 = propagate(scores, elf1, elf2)
    return "".join(list(map(str, scores[target:target+10])))


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
    assert result == "2107929416"
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
    assert result == 20307394
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
