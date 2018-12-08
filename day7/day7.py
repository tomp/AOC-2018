#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day 7
#
from collections import namedtuple, defaultdict
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

def parse_line(line):
    """Parse a line of instructions and return a (step, requires) tuple"""
    assert line.startswith("Step ") and line.endswith(" can begin.")
    word = line.split()
    return word[7], word[1]

def parse_tasks(lines):
    """Parse the input decsription and return a dict mapping
    each task to the set of tasks that must be completed first.
    """
    req = defaultdict(set)
    steps = set()
    for line in lines:
        step, after = parse_line(line)
        req[step].add(after)
        steps.add(step)
        steps.add(after)
    for step in steps:
        if step not in req:
            req[step] = set()
    return req

def solve(lines):
    """Solve the problem for Part 1."""
    req = parse_tasks(lines)
    steps = set(req.keys())
    ready = {step for step, reqs in req.items() if not reqs}
    tasks = []
    while ready:
        step = sorted(list(ready))[0]
        tasks.append(step)
        ready.remove(step)
        steps.remove(step)
        for k in steps:
            if all([m not in steps for m in req[k]]):
                ready.add(k)
    return "".join(tasks)

def solve2(lines, helpers=0, basetime=0):
    """Solve the problem for Part 2."""
    req = parse_tasks(lines)
    steps = set(req.keys())
    ready = {step for step, reqs in req.items() if not reqs}
    tasks = dict()
    workers = list(range(1, helpers+2)) # free workers
    elapsed = 0
    while ready or tasks:
        active = list(tasks.keys())
        print(elapsed, active)
        for step in active:
            worker, remaining = tasks[step]
            if remaining == 1:
                del tasks[step]
                steps.remove(step)
                workers.append(worker)
            else:
                tasks[step] = (worker, remaining-1)

        for k in steps:
            if k not in active:
                if all([m not in steps for m in req[k]]):
                    ready.add(k)

        queue = list(sorted(ready))
        while ready and workers:
            step = queue.pop(0)
            worker = workers.pop(0)
            tasks[step] = (worker, basetime + ord(step) - ord('A') + 1)
            ready.remove(step)
            print("@ {:2d}: Start task {} w/ worker {} ({} sec)".format(
                elapsed, step, *tasks[step]))
        if tasks:
            elapsed += 1
    return elapsed


# PART 1

def sample_input():
    """Return the puzzle input and expected result for the part 1
    example problem.
    """
    lines = split_nonblank_lines("""Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""")
    expected = 'CABDFE'
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
    expected = 15
    return lines, expected

def example2():
    lines, expected = sample_input2()
    result = solve2(lines, helpers=1)
    logger.info("got {} (expected {})".format(result, expected))
    assert result == expected
    logger.info('= ' * 32)

def part2(lines):
    result = solve2(lines, 5, 60)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)

if __name__ == '__main__':
    example()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)

