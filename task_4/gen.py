#!/usr/bin/env python3
"""
Task 4 test generator. 25 points per group (1–4).

Group 1: N 2–5, short strings, sample
Group 2: N ≤ 50
Group 3: N ≤ 200, long strings, tie K+L
Group 4: N = 500, max string length
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
sys.path.insert(0, str(TASK_DIR))

SAMPLE = "2\n()\n>!!!>!<?>\n"

from solution import encode_gnome  # noqa: E402


def random_gnome_value(rng: random.Random, max_digits: int) -> int:
    digits = [rng.randint(0, 9) for _ in range(rng.randint(1, max_digits))]
    total = 0
    for i, d in enumerate(digits):
        total += d * (10**i)
    return total


def case(n: int, values: list[int]) -> str:
    lines = [str(n)] + [encode_gnome(v) for v in values]
    return "\n".join(lines) + "\n"


def cases_for_group(group: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    if group == 1:
        cases = [SAMPLE, case(2, [0, 5]), case(3, [1, 10, 100])]
        while len(cases) < TESTS_PER_GROUP:
            n = rng.randint(2, 5)
            vals = [random_gnome_value(rng, 3) for _ in range(n)]
            cases.append(case(n, vals))
        return cases[:TESTS_PER_GROUP]

    if group == 2:
        cases = []
        for _ in range(TESTS_PER_GROUP):
            n = rng.randint(2, 50)
            cases.append(case(n, [random_gnome_value(rng, 8) for _ in range(n)]))
        return cases

    if group == 3:
        cases = []
        for _ in range(TESTS_PER_GROUP):
            n = rng.randint(50, 200)
            vals = [random_gnome_value(rng, 15) for _ in range(n)]
            vals[0] = min(vals)
            vals[-1] = max(vals) + 1
            cases.append(case(n, vals))
        return cases

    cases = []
    for _ in range(TESTS_PER_GROUP):
        n = 500
        vals = [random_gnome_value(rng, 25) for _ in range(n)]
        cases.append(case(n, vals))
    return cases


def main() -> None:
    parser = argparse.ArgumentParser(description=f"Task 4 generator ({POINTS_PER_GROUP} pts/group)")
    add_gen_args(parser)
    args = parser.parse_args()
    seed = default_seed(args.group, args.seed)
    cases = cases_for_group(args.group, seed)
    write_tests(TASK_DIR, args.out, args.group, cases)
    print(f"Wrote {len(cases)} tests to {args.out / f'group{args.group}'}")


if __name__ == "__main__":
    main()
