#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day 3
#
from collections import namedtuple, defaultdict
from itertools import chain
import re
import logging

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logger = logging.getLogger()

INPUTFILE = 'input.txt'

XMAX, YMAX = 1000, 1000

def sample_input():
    lines = split_nonblank_lines("""#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
""")
    expected = 4
    return lines, expected

def sample_input2():
    lines = split_nonblank_lines("""#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
""")
    expected = 3
    return lines, expected

examples2 = [('arg1', 'expected1'),
             ('arg2', 'expected2')]

# Utility functions

def load_input(infile):
    lines = []
    with open(infile, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line:
                lines.append(line)
        return lines

def split_nonblank_lines(text):
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            lines.append(line)
    return lines

# Solution

Claim = namedtuple('Claim', ['id', 'left', 'top',  'width', 'height'])

claim_re = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$")

def parse_claim(line):
    m = claim_re.match(line)
    if m:
        return Claim(*map(int, m.groups()))
    raise ValueError("Cannot parse {}".format(line))

def solve(lines):
    """Solve the problem."""
    claims = list(map(parse_claim, lines))

    sq = []
    for _ in range(YMAX + 1):
        sq.append([0] * (XMAX + 1))

    for c in claims:
        for x in range(c.left, c.left + c.width):
            for y in range(c.top, c.top + c.height):
                sq[y][x] += 1
    # print("\n".join([" ".join(["{:2d}".format(v) for v in row]) for row in sq]))
    return sum([1 for v in chain(*sq) if v > 1])

def solve2(lines):
    """Solve the problem."""
    claims = list(map(parse_claim, lines))

    sq = []
    for _ in range(YMAX + 1):
        sq.append([0] * (XMAX + 1))

    overlap = defaultdict(set)

    for c in claims:
        overlap[c.id].add(c.id)
        for x in range(c.left, c.left + c.width):
            for y in range(c.top, c.top + c.height):
                if not sq[y][x]:
                    sq[y][x] = c.id
                else: 
                    other_id = sq[y][x]
                    overlap[other_id].add(c.id)
                    overlap[c.id].add(other_id)
    # print("\n".join([" ".join(["{:2d}".format(v) for v in row]) for row in sq]))
    for cid, others in overlap.items():
        if len(others) == 1:
            return cid

# PART 1

def example():
    # single example
    lines, expected = sample_input()
    result = solve(lines)
    logger.info("got {} (expected {})".format(result, expected))
    assert result == expected
    logger.info('= ' * 32)

def part1(lines):
    result = solve(lines)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)


# PART 2

def example2():
    lines, expected = sample_input2()
    result = solve2(lines)
    logger.info("got {} (expected {})".format(result, expected))
    assert result == expected
    logger.info('= ' * 32)

def part2(lines):
    result = solve2(lines)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)

if __name__ == '__main__':
    example()
    input = load_input(INPUTFILE)
    part1(input)
    example2()
    part2(input)
