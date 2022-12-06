#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day 15
#
from typing import Sequence, Union, Optional, Any
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
import math
import re

INPUTFILE = "input.txt"

SAMPLE1 = """
#######
#E..G.#
#...#.#
#.G.#G#
#######
"""

SAMPLE2 = """
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########
"""

SAMPLE_CASES = [
    (
        """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#   
#######   
        """,
        27730
    ),
    (
        """
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
        """,
        36334
    ),
    (
        """
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
        """,
        39514
    ),
    (
        """
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
        """,
        27755
    ),
    (
        """
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
        """,
        28944
    ),
    (
        """
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
        """,
        18740
    ),
]

SAMPLE_CASES2 = [
    (
        """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#   
#######   
        """,
        4988
    ),
    (
        """
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
        """,
        31284
    ),
    (
        """
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
        """,
        3478
    ),
    (
        """
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
        """,
        6474
    ),
    (
        """
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
        """,
        1140
    ),
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

def load_text(text: str) -> Lines:
    return filter_blank_lines(text.split("\n"))

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]


# Solution

Cell = str

EMPTY, ROCK, ELF, GOBLIN = ".", "#", "E", "G"
FOE = {ELF: GOBLIN, GOBLIN: ELF}

DEFAULT_HIT_POINTS = 200
DEFAULT_ATTACK_POWER = 3


@dataclass(order=True, frozen=True)
class Pos():
    row: int
    col: int

    def __str__(self) -> str:
        return f"({self.row},{self.col})"

    def neighbors(self) -> "List[Pos]":
        return [
            Pos(self.row, self.col + 1),
            Pos(self.row + 1, self.col),
            Pos(self.row, self.col - 1),
            Pos(self.row - 1, self.col),
        ]

class Board():
    grid: dict[Pos, Cell]

    def __init__(self, cells, elf_power=DEFAULT_ATTACK_POWER):
        self.grid = cells
        self.rowmax = max([v.row for v in self.grid.keys()])
        self.rowmin = min([v.row for v in self.grid.keys()])
        self.colmax = max([v.col for v in self.grid.keys()])
        self.colmin = min([v.col for v in self.grid.keys()])
        self.hit_points = defaultdict(lambda: DEFAULT_HIT_POINTS)

        self.power = {}
        for elf in self.locate(ELF):
            name = self.grid[elf]
            self.power[name] = elf_power
        for gob in self.locate(GOBLIN):
            name = self.grid[gob]
            self.power[name] = DEFAULT_ATTACK_POWER


    @classmethod
    def from_lines(cls, lines, **kwargs) -> "Board":
        grid = defaultdict(lambda : ROCK)
        goblins = 0
        elves = 0
        for r, line in enumerate(lines):
            for c, val in enumerate(line):
                if val == ELF:
                    elves += 1
                    val = f"{ELF}{elves}"
                elif val == GOBLIN:
                    goblins += 1
                    val = f"{GOBLIN}{goblins}"
                grid[Pos(r, c)] = val
        return cls(grid, **kwargs)

    def print(self, title="", overlay=None):
        if title:
            print(title)
        for r in range(self.rowmin, self.rowmax+1):
            row = []
            for c in range(self.colmin, self.colmax+1):
                pos = Pos(r, c)
                val = self.grid[pos][0]
                if overlay and pos in overlay:
                    val = overlay[pos]
                row.append(val)
            print("".join(row))

    def move(self, pos, dest):
        # print(f"Move {self.grid[pos]} from {pos} to {dest}")
        assert self.grid[pos][0] in (ELF, GOBLIN)
        assert self.grid[dest] == EMPTY
        assert dest in pos.neighbors()
        self.grid[dest] = self.grid[pos]
        self.grid[pos] = EMPTY

    def attack(self, pos: Pos, target: Pos) -> bool:
        """Character at position 'pos' attacks character at position 'target'.
        Return True if target is killed, else False.
        """
        attacker = self.grid[pos]
        defender = self.grid[target]
        before = self.hit_points[defender]
        assert attacker[0] in (ELF, GOBLIN)
        assert defender[0] in (ELF, GOBLIN)
        self.hit_points[defender] -= self.power[attacker]
        # print(f"{attacker} attacks {defender} [{before} -> {self.hit_points[defender]}HP]")
        if self.hit_points[defender] < 1:
            # print(f"{attacker} kills {defender} ")
            self.grid[target] = EMPTY
            return True
        return False
        

    def locate(self, target):
        result = []
        for pos, val in self.grid.items():
            if val[0] == target:
                result.append(pos)
        return result

    def inrange(self, target):
        """Return positions of all locations in range of the
        given target type (ELF or GOBLIN).
        """
        positions = set()
        for pos in self.locate(target):
            for nayb in pos.neighbors():
                if self.grid[nayb] == EMPTY:
                    positions.add(nayb)
        result = list(positions)
        result.sort()
        return result

    def distances(self, pos):
        """Return dict mapping positions of all reachable locations to
        the shortest distance to thatlocation.
        """
        result = defaultdict(lambda: -1)
        positions = [(pos, 0)]
        visited = set()
        while positions:
            loc, dist = positions.pop(0)
            if loc in visited:
                continue
            result[loc] = dist
            visited.add(loc)
            for nayb in loc.neighbors():
                if self.grid[nayb] == EMPTY and nayb not in visited:
                    positions.append((nayb, dist+1))
        return result

    def targets(self, pos):
        """Return sorted list of foes that can be attacked by the elf or
        goblin at the given location.
        """
        result = []
        assert self.grid[pos][0] in (ELF, GOBLIN)
        foe = FOE[self.grid[pos][0]]
        for nayb in pos.neighbors():
            if self.grid[nayb][0] == foe:
                result.append((self.hit_points[self.grid[nayb]], nayb))
        result.sort()
        return result


def first_step(start, goal, dists):
    """Return list of the shortest paths from the start position to the goal.
    The distance map for the start position must be provided.
    """
    result = []
    dist = dists[goal]
    frontier = [goal]
    # print(f"dist: {dist}  frontier: {', '.join([str(v) for v in frontier])}")
    while dist > 1:
        dist -= 1
        next_step = []
        for pos in frontier:
            for nayb in pos.neighbors():
                if dists.get(nayb, -1) == dist:
                    # print(f"... pos: {pos}  nayb: {nayb}")
                    next_step.append(nayb)
        frontier = next_step
        # print(f"dist: {dist}  frontier: {', '.join([str(v) for v in frontier])}")
    frontier.sort()
    return frontier[0]

def propagate(board, attack: bool = True) -> int:
    """Play the game.  Return when one side has won, or no further
    progress can be made.  The board is updated in place.
    """
    rounds = 0
    initial_elves = board.locate(ELF)

    # board.print(title=f"Initially:")
    while True:
        rounds += 1
        elves = board.locate(ELF)
        goblins = board.locate(GOBLIN)
        # print(f"\nRound {rounds} :: Elves: {len(elves)}  Goblins: {len(goblins)}")

        action = 0
        incomplete_loop = False

        units = elves + goblins
        units.sort()

        for pos in units:
            name = board.grid[pos]
            if name == EMPTY:
                continue
            other = FOE[board.grid[pos][0]]
            if not board.locate(other):
                incomplete_loop = True
                break
            foes = board.targets(pos)
            if not foes:
                # Move
                inrange = board.inrange(other)
                dists = board.distances(pos)
                reachable = {pos: dist for pos, dist in dists.items() if pos in inrange}
                if reachable:
                    mindist = min(reachable.values())
                    nearest = [pos for pos, dist in reachable.items() if dist == mindist]
                    nearest.sort()
                    goal = nearest[0]
                    step = first_step(pos, goal, dists)
                    board.move(pos, step)
                    pos = step
                    action += 1
                foes = board.targets(pos)
            if foes:
                if attack:
                    # Attack!
                    _, foe = foes[0]
                    board.attack(pos, foe)
                    action += 1

        # board.print(title=f"After {rounds} rounds:")
        if incomplete_loop or not action:
            rounds -= 1
            break

    elves = board.locate(ELF)
    goblins = board.locate(GOBLIN)
    casualties  = len(initial_elves) - len(elves)
    # for pos in elves + goblins:
    #     character = board.grid[pos]
    #     print(f"{character} has {board.hit_points[character]} HP")
    if elves:
        total_hit_points = sum([board.hit_points[board.grid[elf]] for elf in elves])
        victory = True
    elif goblins:
        total_hit_points = sum([board.hit_points[board.grid[gob]] for gob in goblins])
        victory = False
    score = rounds * total_hit_points
    print(f"Final score: {score} <-- {rounds} rounds, {total_hit_points} HP remaining") 
    return score, victory, casualties


def check2(lines):
    """Test the various operations we need to run the game.
    """
    board = Board.from_lines(lines)

    elves = board.locate(ELF)
    goblins = board.locate(GOBLIN)
    print(f"Elves: {len(elves)}  Goblins: {len(goblins)}")
    propagate(board, attack=False)


def check(lines):
    """Test the various operations we need to run the game.
    """
    board = Board.from_lines(lines)

    elves = board.locate(ELF)
    goblins = board.locate(GOBLIN)
    print(f"Elves: {len(elves)}  Goblins: {len(goblins)}")
    board.print(title="Targets:")

    inrange = board.inrange(GOBLIN)
    symbols = {pos: "?" for pos in inrange}
    board.print(title="In range:", overlay=symbols)

    elf1 = elves[0]
    dists = board.distances(elf1)
    reachable = {pos: dist for pos, dist in dists.items() if pos in inrange}
    symbols = {pos: "@" for pos in reachable}
    board.print(title="Reachable:", overlay=symbols)

    mindist = min(reachable.values())
    print(f"nearest reachble locations @ {mindist}")
    nearest = {pos: dist for pos, dist in reachable.items() if dist == mindist}
    symbols = {pos: "!" for pos in nearest.keys()}
    board.print(title="Nearest:", overlay=symbols)

    locs = list(nearest.keys())
    locs.sort()
    goal = locs[0]
    symbols = {goal: "+"}
    board.print(title="Chosen:", overlay=symbols)

    step = first_step(elf1, goal, dists)
    board.move(elf1, step)
    board.print(title="Step:")


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    victory = False
    casualties = -1
    power = DEFAULT_ATTACK_POWER + 1
    while not victory or casualties != 0:
        board = Board.from_lines(lines, elf_power=power)
        score, victory, casualties = propagate(board)
        if victory:
            if not casualties:
                print(f"ELVES WIN!  power={power}, score={score}")
            else:
                print(f"elves win.  power={power}, score={score}, casualties={casualties}")
        else:
            print(f"goblins win.  power={power}, score={score}")
        power += 1
    return score

def solve(lines: Lines) -> int:
    """Solve the problem."""
    board = Board.from_lines(lines)
    score, _, _ = propagate(board)
    return score


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")

    print("- "*32)
    lines = load_text(SAMPLE1)
    check(lines)

    print("- "*32)
    lines = load_text(SAMPLE2)
    check2(lines)

    for text, expected in SAMPLE_CASES:
        print("- "*32)
        lines = load_text(text)
        result = solve(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 198531
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
    assert result == 90420
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
