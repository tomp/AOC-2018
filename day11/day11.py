#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day 11
#
import re
import json
from datetime import datetime, timedelta
from collections import namedtuple, defaultdict
from itertools import chain
import logging


logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logger = logging.getLogger()

INPUT = 2187

XMIN, XMAX = 1, 300
YMIN, YMAX = 1, 300
XSIZE = XMAX - XMIN + 1
YSIZE = YMAX - YMIN + 1

# Utility functions

def strip(line):
    return line.strip()

def load_input(infile):
    with open(infile, 'r') as fp:
        return list(filter(bool, map(strip, fp)))

def split_nonblank_lines(text):
    return list(filter(bool, map(strip, text.splitlines())))


# Solution

def cell_power(x, y, sn):
    """Return the power level for the fuel cell at (x, y),
    for the given grid serial number (sn).
    """
    rack = x + 10
    val = (rack * y + sn) * rack
    return ((val % 1000) // 100) - 5

def best_square1(sn, size):
    """Return the coords and total power for the size x size square
    with the largest total power.

    This does the least optimized, "brute force", calculation.
    """
    grid = [[cell_power(x,y,sn) for x in range(XMIN, XMAX+1)]
                                for y in range(YMIN, YMAX+1)]

    xr, yr = XMIN, YMIN
    pr = grid[0][0]
    for xc in range(XMAX-XMIN-size+1):
        for yc in range(YMAX-YMIN-size+1):
            values = [grid[yi][xi] for xi in range(xc, xc+size)
                                   for yi in range(yc, yc+size)]
            pc = sum(values)
            if pc > pr:
                xr, yr = xc + XMIN, yc + YMIN
                pr = pc
    return xr, yr, pr

def best_square(sn, size):
    """Return the coords and total power for the size x size square
    with the largest total power.

    This function avoids recalculating many of sums.  It's still not
    as optimized as possible, but it's fast enough for the AoC problem.
    """
    grid = [[cell_power(x,y,sn) for x in range(XMIN, XMAX+1)]
                                for y in range(YMIN, YMAX+1)]

    xsum = [[sum(grid[y][x:x+size]) for x in range(XMAX-XMIN-size+1)]
                                    for y in range(YMAX-YMIN+1)]

    xr, yr = XMIN, YMIN
    pr = grid[0][0]
    for xc in range(XMAX-XMIN-size+1):
        values = [xsum[yi][xc] for yi in range(0, size)]
        pc = sum(values)
        if pc > pr:
            xr, yr = xc + XMIN, YMIN
            pr = pc
        for yc in range(1, YMAX-YMIN-size+1):
            pc += xsum[yc+size-1][xc] - xsum[yc-1][xc] 
            if pc > pr:
                xr, yr = xc + XMIN, yc + YMIN
                pr = pc
    return xr, yr, pr

def solve(arg):
    """Solve the problem for Part 1."""
    sn = int(arg)
    return best_square(sn, 3)

def solve2(arg):
    """Solve the problem for Part 2."""
    sn = int(arg)
    xr, yr, pr, sr = 0, 0, 0, 0
    for size in range(2, 299):
        xs, ys, ps = best_square(sn, size)
        # print("size: {}  --> {}".format(size, (xs,  ys, ps)))
        if ps > pr:
            xr, yr, pr, sr = xs, ys, ps, size
    return xr, yr, sr, pr


# PART 1

def sample_cases():
    """Return the example inputs and expected results for the part 1.
    (Used if there are multiple example cases.)
    """
    return [(18, (33, 45, 29)),
            (42, (21, 61, 30))]

def sample_cases2():
    """Return the example inputs and expected results for the part 1.
    (Used if there are multiple example cases.)
    """
    return [(18, (90, 269, 16, 113)),
            (42, (232, 251, 12, 119))]

def test_cell_power():
    """Test that the cell_power() function returns the right values.
    """
    cases = [((3, 5, 8), 4),
            ((122, 79, 57), -5),
            ((217, 196, 39), 0),
            ((101, 153, 71), 4)]
    for args, expected in cases:
        result = cell_power(*args)
        logger.info("'{}' -> {} (expected {})".format(args, result, expected))
        assert result == expected

def example():
    cases = sample_cases()
    for arg, expected in cases:
        result = solve(arg)
        logger.info("'{}' -> {} (expected {})".format(arg, result, expected))
        assert result == expected

    logger.info('= ' * 32)

def part1(arg):
    result = solve(arg)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)


# PART 2

def example2():
    cases = sample_cases2()
    for arg, expected in cases:
        result = solve2(arg)
        logger.info("'{}' -> {} (expected {})".format(arg, result, expected))
        assert result == expected

    logger.info('= ' * 32)

def part2(arg):
    result = solve2(arg)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)

if __name__ == '__main__':
    test_cell_power()
    example()
    arg = INPUT
    part1(arg)
    example2()
    part2(arg)

