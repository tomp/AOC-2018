#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day N
#
import logging

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logger = logging.getLogger()

INPUTFILE = 'input.txt'

def sample_input():
    return ""

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

def solve(arg):
    """Solve the problem."""
    pass

# PART 1

def example():
    cases = [('arg1', 'expected1'),
             ('arg2', 'expected2')]
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

def example2():
    logger.info('= ' * 32)

def part2(lines):
    logger.info('= ' * 32)

if __name__ == '__main__':
    example()
    # input = load_input(INPUTFILE)
    # part1(input)
    # example2()
    # part2(input)
