#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day 5
#
from string import ascii_uppercase, ascii_lowercase
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

REACTS = dict([(cha, chb) for cha, chb in
               zip(ascii_uppercase + ascii_lowercase,
                   ascii_lowercase + ascii_uppercase)])

def react(poly):
    """Carry out all reactions on the input polymer.
    The remaining polymer is returned.
    """
    result = []
    idx = 0
    stop = len(poly) - 1
    while idx < stop:
        if poly[idx+1] == REACTS[poly[idx]]:
            idx += 2
        else:
            result.append(poly[idx])
            idx += 1
    if idx == stop:
        result.append(poly[idx])
    return "".join(result)

def fully_react(arg):
    """Carry out all possible reactions on the input polymer.
    The remaining polymer is returned.
    """
    poly = arg
    new_poly = react(poly)
    while new_poly != poly:
        poly = new_poly
        new_poly = react(poly)
    return poly

def solve(arg):
    """Solve the problem for Part 1."""
    new_poly = fully_react(arg)
    return len(new_poly)

def solve2(arg):
    """Solve the problem for Part 2."""
    best = ""
    for ch in ascii_uppercase:
        poly = arg.replace(ch, "").replace(REACTS[ch], "")
        new_poly = fully_react(poly)
        if len(new_poly) < len(best) or not best:
            best = new_poly
    return len(best)

# PART 1

def sample_cases():
    """Return the example inputs and expected results for the part 1.
    (Used if there are multiple example cases.)
    """
    return [('aA', 0),
            ('a', 1),
            ('aAB', 1),
            ('baA', 1),
            ('abBA', 0),
            ('abcdefgGFEDCBA', 0),
            ('abAB', 4),
            ('aabAAB', 6),
            ('dabAcCaCBAcCcaDA', 10)]

def example():
    cases = sample_cases()
    for arg, expected in cases:
        result = solve(arg)
        logger.info("'{}' -> '{}' (expected '{}')".format(arg, result, expected))
        assert result == expected
    logger.info('= ' * 32)

def part1(lines):
    result = solve(lines[0])
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)


# PART 2

def sample_input2():
    """Return the puzzle input and expected result for the part 2
    example problem.
    """
    text = 'dabAcCaCBAcCcaDA'
    expected = 4
    return text, expected

def example2():
    text, expected = sample_input2()
    result = solve2(text)
    logger.info("'{}' -> '{}' (expected '{}')".format(text, result, expected))
    logger.info('= ' * 32)

def part2(lines):
    result = solve2(lines[0])
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)

if __name__ == '__main__':
    example()
    input = load_input(INPUTFILE)
    part1(input)
    example2()
    part2(input)

