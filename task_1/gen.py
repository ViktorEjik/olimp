#!/usr/bin/env python3
"""
Task 1 test generator. 25 points per group (1–4).

Group 1: |a| ≤ 10, positive, sample included
Group 2: |a| ≤ 10^4, mixed signs
Group 3: near int32 limits
Group 4: full int32 range stress
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

SAMPLE = "1 2 1 3 1 4\n"
INT32_MIN = -2_147_483_648
INT32_MAX = 2_147_483_647


def case_line(nums: list[int]) -> str:
    return " ".join(map(str, nums)) + "\n"


def cases_group1() -> list[str]:
    return [
        SAMPLE,
        case_line([1, 1, 1, 2, 2, 3]),
        case_line([5, -2, 3, 4, 1, 6]),
        case_line([10, 1, 9, 2, 8, 3]),
    ]


def random_case(rng: random.Random, lo: int, hi: int) -> str:
    nums = [rng.randint(lo, hi) for _ in range(6)]
    # avoid all zeros in denominators positions — brute force skips zero denom
    if all(x == 0 for x in nums):
        nums[0] = 1
    return case_line(nums)


def cases_for_group(group: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    if group == 1:
        base = cases_group1()
        while len(base) < TESTS_PER_GROUP:
            base.append(random_case(rng, 1, 10))
        return base[:TESTS_PER_GROUP]

    if group == 2:
        return [random_case(rng, -10_000, 10_000) for _ in range(TESTS_PER_GROUP)]

    if group == 3:
        cases = [random_case(rng, INT32_MAX - 1000, INT32_MAX) for _ in range(3)]
        cases += [random_case(rng, INT32_MIN, INT32_MIN + 1000) for _ in range(3)]
        while len(cases) < TESTS_PER_GROUP:
            cases.append(random_case(rng, -2_000_000_000, 2_000_000_000))
        return cases[:TESTS_PER_GROUP]

    return [random_case(rng, INT32_MIN, INT32_MAX) for _ in range(TESTS_PER_GROUP)]


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
