#!/usr/bin/env python3
"""
Task 1 test generator. 25 points per group.

Group 1: |a|<=10, positive, official sample
Group 2: |a|<=10^4, mixed signs
Group 3: near int32 limits
Group 4: full int32 stress
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from gen_common import TESTS_PER_GROUP, add_cli, write_tests  # noqa: E402

OFFICIAL = "1 2 1 3 1 4\n"
INT32_MIN = -2_147_483_648
INT32_MAX = 2_147_483_647


def build_cases(group: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    cases: list[str] = []

    if group == 1:
        cases.append(OFFICIAL.strip())
        while len(cases) < TESTS_PER_GROUP:
            vals = [rng.randint(1, 10) for _ in range(6)]
            cases.append(" ".join(map(str, vals)))
        return cases

    if group == 2:
        while len(cases) < TESTS_PER_GROUP:
            vals = [rng.randint(-10_000, 10_000) or 1 for _ in range(6)]
            if any(v == 0 for v in vals):
                continue
            cases.append(" ".join(map(str, vals)))
        return cases

    if group == 3:
        while len(cases) < TESTS_PER_GROUP:
            vals = [rng.randint(INT32_MIN // 2, INT32_MAX // 2) for _ in range(6)]
            if any(v == 0 for v in vals):
                continue
            cases.append(" ".join(map(str, vals)))
        return cases

    while len(cases) < TESTS_PER_GROUP:
        if len(cases) % 3 == 0:
            vals = [rng.randint(INT32_MIN, INT32_MAX) for _ in range(6)]
        else:
            vals = [rng.choice([INT32_MIN, INT32_MAX, -1, 1]) for _ in range(6)]
        if any(v == 0 for v in vals):
            continue
        cases.append(" ".join(map(str, vals)))
    return cases


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    add_cli(parser)
    args = parser.parse_args()
    task_dir = Path(__file__).resolve().parent
    seed = args.seed if args.seed is not None else args.group * 1000
    cases = build_cases(args.group, seed)
    write_tests(cases, group=args.group, out=args.out, solution=task_dir / "solution.py")
    print(f"Wrote {len(cases)} tests to {args.out / f'group{args.group}'}")
