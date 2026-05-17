#!/usr/bin/env python3
"""
Task 5 test generator. 25 points per group (1–4).

Group 1: sample, |coord| ≤ 10
Group 2: |coord| ≤ 10^4
Group 3: edge cases (same tile, large distance)
Group 4: |coord| near 2·10^9
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

SAMPLE = "0 2 1 1\n"
LIM = 2_000_000_000


def case(a1: int, b1: int, a2: int, b2: int) -> str:
    return f"{a1} {b1} {a2} {b2}\n"


def cases_for_group(group: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    if group == 1:
        base = [
            SAMPLE,
            case(0, 0, 0, 0),
            case(0, 0, 1, 0),
            case(2, 3, 5, 1),
        ]
        while len(base) < TESTS_PER_GROUP:
            a1, b1 = rng.randint(-10, 10), rng.randint(-10, 10)
            a2, b2 = rng.randint(-10, 10), rng.randint(-10, 10)
            base.append(case(a1, b1, a2, b2))
        return base[:TESTS_PER_GROUP]

    if group == 2:
        cases = []
        for _ in range(TESTS_PER_GROUP):
            bound = 10_000
            a1, b1 = rng.randint(-bound, bound), rng.randint(-bound, bound)
            a2, b2 = rng.randint(-bound, bound), rng.randint(-bound, bound)
            cases.append(case(a1, b1, a2, b2))
        return cases

    if group == 3:
        cases = [
            case(0, 0, 0, 0),
            case(5, 5, 5, 5),
            case(0, 0, 100, -50),
            case(-100, 200, 100, -200),
        ]
        while len(cases) < TESTS_PER_GROUP:
            a1, b1 = rng.randint(-500, 500), rng.randint(-500, 500)
            da, db = rng.randint(-200, 200), rng.randint(-200, 200)
            cases.append(case(a1, b1, a1 + da, b1 + db))
        return cases[:TESTS_PER_GROUP]

    cases = []
    for _ in range(TESTS_PER_GROUP):
        a1, b1 = rng.randint(-LIM, LIM), rng.randint(-LIM, LIM)
        a2, b2 = rng.randint(-LIM, LIM), rng.randint(-LIM, LIM)
        cases.append(case(a1, b1, a2, b2))
    return cases


def main() -> None:
    parser = argparse.ArgumentParser(description=f"Task 5 generator ({POINTS_PER_GROUP} pts/group)")
    add_gen_args(parser)
    args = parser.parse_args()
    seed = default_seed(args.group, args.seed)
    cases = cases_for_group(args.group, seed)
    write_tests(TASK_DIR, args.out, args.group, cases)
    print(f"Wrote {len(cases)} tests to {args.out / f'group{args.group}'}")


if __name__ == "__main__":
    main()
