#!/usr/bin/env python3
"""
Task 3 test generator. 25 points per group (1–4).

Group 1: N 1–3, small |A|,|B|,|X|
Group 2: N ≤ 50, |A|,|B|,|X| ≤ 100
Group 3: N ≤ 200, unreachable X, negative A/B
Group 4: N ≤ 999, |A|,|B|,|X| < 1000 (statement limits)
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from gen_common import (  # noqa: E402
    POINTS_PER_GROUP,
    TESTS_PER_GROUP,
    add_gen_args,
    default_seed,
    write_tests,
)

TASK_DIR = Path(__file__).resolve().parent

SAMPLE = "1 1 2\n9\n"


def cases_group1() -> list[str]:
    return [
        SAMPLE.strip(),
        "2 2 3\n5\n7\n",
        "1 -1 2\n1\n-1\n",
        "3 1 2\n2\n4\n8\n",
    ]


def random_case(rng: random.Random, n_max: int, bound: int) -> str:
    n = rng.randint(1, n_max)
    while True:
        a = rng.randint(-bound + 1, bound - 1)
        b = rng.randint(-bound + 1, bound - 1)
        if a != 0 and b != 0:
            break
    lines = [f"{n} {a} {b}"]
    for _ in range(n):
        x = rng.randint(-bound + 1, bound - 1)
        while x == 0:
            x = rng.randint(-bound + 1, bound - 1)
        lines.append(str(x))
    return "\n".join(lines) + "\n"


def cases_for_group(group: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    if group == 1:
        base = cases_group1()
        while len(base) < TESTS_PER_GROUP:
            base.append(random_case(rng, 3, 10))
        return base[:TESTS_PER_GROUP]

    if group == 2:
        return [random_case(rng, 50, 100) for _ in range(TESTS_PER_GROUP)]

    if group == 3:
        cases = []
        for _ in range(TESTS_PER_GROUP // 2):
            cases.append(random_case(rng, 200, 500))
        # many unreachable
        for _ in range(TESTS_PER_GROUP - len(cases)):
            cases.append("4 7 11\n13\n17\n19\n23\n")
        return cases

    # group 4
    cases = [random_case(rng, 999, 999) for _ in range(TESTS_PER_GROUP - 1)]
    cases.insert(0, random_case(rng, 999, 999))
    return cases


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
