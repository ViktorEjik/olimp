#!/usr/bin/env python3
"""
Task 1 test generator. 25 points per group (1–4).

Group 1: N ≤ 10, sample, A_i ≤ 10^3
Group 2: N ≤ 100, A_i ≤ 10^6
Group 3: N ≤ 500, A_i near 2^20…2^24
Group 4: N = 1000, A_i ≤ 2^24−1
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

SAMPLE = "4\n1\n0\n3\n732\n"
MAX_A = 2**24 - 1


def case_lines(rng: random.Random, n: int, lo: int, hi: int) -> str:
    lines = [str(n)] + [str(rng.randint(lo, hi)) for _ in range(n)]
    return "\n".join(lines) + "\n"


def cases_for_group(group: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    if group == 1:
        base = [
            SAMPLE,
            "3\n0\n1\n2\n",
            "5\n7\n14\n28\n56\n112\n",
        ]
        while len(base) < TESTS_PER_GROUP:
            base.append(case_lines(rng, rng.randint(1, 10), 0, 1000))
        return base[:TESTS_PER_GROUP]

    if group == 2:
        return [case_lines(rng, rng.randint(10, 100), 0, 10**6) for _ in range(TESTS_PER_GROUP)]

    if group == 3:
        cases = []
        for _ in range(TESTS_PER_GROUP // 2):
            cases.append(case_lines(rng, rng.randint(100, 500), 2**20, MAX_A))
        while len(cases) < TESTS_PER_GROUP:
            cases.append(case_lines(rng, rng.randint(50, 300), 0, 2**16))
        return cases

    return [case_lines(rng, 1000, 0, MAX_A) for _ in range(TESTS_PER_GROUP)]


def main() -> None:
    parser = argparse.ArgumentParser(description=f"Task 1 generator ({POINTS_PER_GROUP} pts/group)")
    add_gen_args(parser)
    args = parser.parse_args()
    seed = default_seed(args.group, args.seed)
    cases = cases_for_group(args.group, seed)
    write_tests(TASK_DIR, args.out, args.group, cases)
    print(f"Wrote {len(cases)} tests to {args.out / f'group{args.group}'}")


if __name__ == "__main__":
    main()
