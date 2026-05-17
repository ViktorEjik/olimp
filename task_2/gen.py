#!/usr/bin/env python3
"""
Task 2 test generator. 25 points per group (1–4).

Group 1: shallow trees, sample QDWWQDDDW
Group 2: random trees, len ≤ 100
Group 3: deep trees, tie-break cases
Group 4: max length 1365
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from gen_common import POINTS_PER_GROUP, TESTS_PER_GROUP, add_gen_args, default_seed, write_tests

TASK_DIR = Path(__file__).resolve().parent
COLORS = list("WROYGCBVD")
MAX_LEN = 1365
SAMPLE = "QDWWQDDDW\n"


def build_tree(rng: random.Random, depth: int, max_depth: int) -> str:
    if depth >= max_depth or (depth > 1 and rng.random() < 0.35):
        return rng.choice(COLORS)
    parts = [build_tree(rng, depth + 1, max_depth) for _ in range(4)]
    return "Q" + "".join(parts)


def random_tree(rng: random.Random, max_depth: int, max_len: int) -> str:
    for _ in range(50):
        s = build_tree(rng, 1, max_depth)
        if len(s) <= max_len:
            return s
    return "W"


def build_balanced_depth(d: int) -> str:
    if d <= 0:
        return "W"
    return "Q" + "".join(build_balanced_depth(d - 1) for _ in range(4))


def build_tie_tree() -> str:
    """Equal area for W and D at top level split."""
    return "Q" + "W" * 2 + "D" * 2


def cases_for_group(group: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    if group == 1:
        cases = [SAMPLE, "W\n", "QWWWW\n", build_tie_tree() + "\n"]
        while len(cases) < TESTS_PER_GROUP:
            cases.append(build_tree(rng, 1, 3) + "\n")
        return cases[:TESTS_PER_GROUP]

    if group == 2:
        return [random_tree(rng, 5, 100) + "\n" for _ in range(TESTS_PER_GROUP)]

    if group == 3:
        cases = [build_tie_tree() + "\n", build_balanced_depth(4) + "\n"]
        while len(cases) < TESTS_PER_GROUP:
            depth = rng.randint(4, 7)
            cases.append(build_tree(rng, 1, depth) + "\n")
        return cases[:TESTS_PER_GROUP]

    cases = []
    for depth in (5, 6, 5):
        s = build_balanced_depth(depth)
        if len(s) <= MAX_LEN:
            cases.append(s + "\n")
    while len(cases) < TESTS_PER_GROUP:
        depth = 5 if rng.random() < 0.7 else 6
        s = build_balanced_depth(depth)
        if len(s) <= MAX_LEN:
            cases.append(s + "\n")
        else:
            cases.append(random_tree(rng, 5, MAX_LEN) + "\n")
    return cases[:TESTS_PER_GROUP]


def main() -> None:
    parser = argparse.ArgumentParser(description=f"Task 2 generator ({POINTS_PER_GROUP} pts/group)")
    add_gen_args(parser)
    args = parser.parse_args()
    seed = default_seed(args.group, args.seed)
    cases = cases_for_group(args.group, seed)
    write_tests(TASK_DIR, args.out, args.group, cases)
    print(f"Wrote {len(cases)} tests to {args.out / f'group{args.group}'}")


if __name__ == "__main__":
    main()
