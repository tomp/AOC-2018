#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day 6
#
import re
from datetime import datetime, timedelta
from collections import namedtuple, defaultdict
from itertools import chain, islice, islice, islice
import logging


logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logger = logging.getLogger()

INPUTFILE = 'input.txt'


# Utility functions

def strip(line):
    return line.strip()

def load_input(infile):
    with open(infile, 'r') as fp:
        return list(filter(bool, map(strip, fp)))

def split_nonblank_lines(text):
    return list(filter(bool, map(strip, text.splitlines())))


# Solution

def parse_points(lines):
    """Return a list of the (x, y) tuples parsed from the
    given text input.
    """
    return [tuple(map(int, line.split(", "))) for line in lines]

def dist(p1, p2):
    """Return Manhattan distance between the given points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def solve(lines):
    """Solve the problem for Part 1."""
    points = parse_points(lines)
    xmin = min([p[0] for p in points])
    xmax = max([p[0] for p in points])
    ymin = min([p[1] for p in points])
    ymax = max([p[1] for p in points])
    region = defaultdict(int)
    for x in range(xmin, xmax+1):
        for y in range(ymin, ymax+1):
            neighbors = [(dist((x, y), p), i) for i, p in enumerate(points)]
            neighbors.sort()
            d1, d2 = neighbors[:2]
            if d1[0] < d2[0]:
                region[d1[1]] += 1
    sizes = sorted(region.values(), reverse=True)
    return sizes[0]
            
def solve2(lines, max_total):
    """Solve the problem for Part 2."""
    points = parse_points(lines)
    xmin = min([p[0] for p in points])
    xmax = max([p[0] for p in points])
    ymin = min([p[1] for p in points])
    ymax = max([p[1] for p in points])
    size = 0
    for x in range(xmin, xmax+1):
        for y in range(ymin, ymax+1):
            total = sum([dist((x, y), p) for p in points])
            if total < max_total:
                size += 1
    return size

# PART 1

def sample_input():
    """Return the puzzle input and expected result for the part 1
    example problem.
    """
    lines = split_nonblank_lines("""1, 1
1, 6
8, 3
3, 4
5, 5
8, 9""")
    expected = 17
    return lines, expected

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

def sample_input2():
    """Return the puzzle input and expected result for the part 2
    example problem.
    """
    lines, _ = sample_input()
    expected = 16
    return lines, expected

def example2():
    lines, expected = sample_input2()
    result = solve2(lines, 32)
    logger.info("got {} (expected {})".format(result, expected))
    assert result == expected
    logger.info('= ' * 32)

def part2(lines):
    result = solve2(lines, 10000)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)

if __name__ == '__main__':
    example()
    input = load_input(INPUTFILE)
    part1(input)
    example2()
    part2(input)

