#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day N
#
import logging

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logger = logging.getLogger()

INPUTFILE = 'input.txt'
MAX_ITER = 10000000


# Utility functions

def load_input(infile):
    lines = []
    with open(infile, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line:
                lines.append(line)
        return lines


# Solution

def solve(arg):
    """Solve the problem."""
    return sum([int(line) for line in arg])


def solve2(arg):
    """Solve the problem."""
    vals = [int(line) for line in arg]
    freq = 0
    freqs = set([freq])
    while True:
        if len(freqs) > MAX_ITER:
            raise RuntimeError("found {} freqs without a repeat!".format(len(freqs)))
        for v in vals:
            freq += v
            if freq in freqs:
                return freq
            freqs.add(freq)

# PART 1

def example():
    lines = "+1, -2, +3, +1".split(", ")
    result = solve(lines)
    expected = 3
    logger.info("got {} (expected {})".format(result, expected))
    assert result == expected
    logger.info('= ' * 32)

def part1(lines):
    result = solve(lines)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)


# PART 2

def example2():
    expected = 3
    cases = [('+1, -1', 0),
             ('+3, +3, +4, -2, -4', 10),
             ('-6, +3, +8, +5, -6', 5),
             ('+7, +7, -2, -7, -4', 14)]
    for arg, expected in cases:
        result = solve2(arg.split(", "))
        logger.info("'{}' -> {} (expected {})".format(arg, result, expected))
        assert result == expected
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
