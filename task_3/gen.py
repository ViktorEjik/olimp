#!/usr/bin/env python3
"""
Task 3 test generator. 25 points per group (1–4).

Group 1: sample, short reachable numbers
Group 2: length 20–40
Group 3: length up to 80 + unreachable (-1)
Group 4: length 100 stress
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

SAMPLE = "100\n"


def rand_digits(rng: random.Random, length: int, lo: int = 1) -> str:
    first = rng.randint(lo, 9)
    rest = "".join(str(rng.randint(0, 9)) for _ in range(length - 1))
    return str(first) + rest


def cases_for_group(group: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    if group == 1:
        base = [
            SAMPLE,
            "1\n",
            "2\n",
            "10\n",
            "12\n",
        ]
        while len(base) < TESTS_PER_GROUP:
            base.append(rand_digits(rng, rng.randint(1, 5)) + "\n")
        return base[:TESTS_PER_GROUP]

    if group == 2:
        return [rand_digits(rng, rng.randint(20, 40)) + "\n" for _ in range(TESTS_PER_GROUP)]

    if group == 3:
        cases = ["9999999999999999999999999999999999999999999999999999999999\n"] * 3
        while len(cases) < TESTS_PER_GROUP:
            cases.append(rand_digits(rng, rng.randint(40, 80)) + "\n")
        return cases[:TESTS_PER_GROUP]

    return [rand_digits(rng, 100) + "\n" for _ in range(TESTS_PER_GROUP)]


def main() -> None:
    parser = argparse.ArgumentParser(description=f"Task 3 generator ({POINTS_PER_GROUP} pts/group)")
    add_gen_args(parser)
    args = parser.parse_args()
    seed = default_seed(args.group, args.seed)
    cases = cases_for_group(args.group, seed)
    write_tests(TASK_DIR, args.out, args.group, cases)
    print(f"Wrote {len(cases)} tests to {args.out / f'group{args.group}'}")


if __name__ == "__main__":
    main()
