#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day 2
#
import logging
from collections import defaultdict

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logger = logging.getLogger()

INPUTFILE = 'input.txt'

def sample_input():
    lines= ['abcdef',
            'bababc',
            'abbcde',
            'abcccd',
            'aabcdd',
            'abcdee',
            'ababab']
    expected = 12
    return lines, expected

def sample_input2():
    lines = ['abcde',
             'fghij',
             'klmno',
             'pqrst',
             'fguij',
             'axcye',
             'wvxyz']
    expected = 'fgij'
    return lines, expected


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

def count_letters(text):
    count = defaultdict(int)
    for ch in text:
        count[ch] += 1
    return count

def solve(lines):
    """Solve the problem."""
    two, three = 0, 0
    for line in lines:
        count = count_letters(line)
        if any([v == 2 for v in count.values()]):
            two += 1
        if any([v == 3 for v in count.values()]):
            three += 1
    return two * three

def solve2(lines):
    """Solve the problem."""
    nlines = len(lines)
    nch = len(lines[0])
    result = []
    for ich in range(nch):
        ids = [line[:ich]+line[ich+1:] for line in lines] 
        if len(set(ids)) < nlines:
            ids.sort()
            for v1, v2 in zip(ids[:-1], ids[1:]):
                if v1 == v2:
                    return v1
    return ''

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
