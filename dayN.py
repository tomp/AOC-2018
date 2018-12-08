#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day N
#
import re
import json
from datetime import datetime, timedelta
from collections import namedtuple, defaultdict
from itertools import chain
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

def solve(lines):
    """Solve the problem for Part 1."""
    pass

def solve2(lines):
    """Solve the problem for Part 2."""
    pass

# PART 1

def sample_input():
    """Return the puzzle input and expected result for the part 1
    example problem.
    """
    lines = []
    expected = 'value'
    return lines, expected

def sample_cases():
    """Return the example inputs and expected results for the part 1.
    (Used if there are multiple example cases.)
    """
    return [('arg1', 'value1'),
            ('arg2', 'value2')]

def example():
    # single example
    lines, expected = sample_input()
    result = solve(lines)
    logger.info("got {} (expected {})".format(result, expected))
    assert result == expected

    # multiple examples
    cases = sample_cases()
    for arg, expected in cases:
        result = solve(arg)
        logger.info("'{}' -> {} (expected {})".format(arg, result, expected))
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
    expected = "value2"
    return lines, expected

def example2():
    logger.info('= ' * 32)

def part2(lines):
    logger.info('= ' * 32)

if __name__ == '__main__':
    example()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)

