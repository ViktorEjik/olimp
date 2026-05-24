#!/usr/bin/env python3
"""
Task 5 test generator. 25 points per group.

Group 1: N<=20, official sample (N=14 per actual string length)
Group 2: N<=500, letters break naive sort
Group 3: N<=5000, -1 cases
Group 4: N=50000 stress
"""

from __future__ import annotations

import random
import string
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from gen_common import TESTS_PER_GROUP, add_cli, write_tests  # noqa: E402

DIGITS = string.digits + string.ascii_lowercase + string.ascii_uppercase
OFFICIAL = "14\naA334422551100"


def build_cases(group: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    cases: list[str] = []

    if group == 1:
        cases.append(OFFICIAL)
        while len(cases) < TESTS_PER_GROUP:
            n = rng.randint(5, 20)
            s = "".join(rng.choice(string.digits) for _ in range(n))
            cases.append(f"{n}\n{s}")
        return cases

    if group == 2:
        while len(cases) < TESTS_PER_GROUP:
            n = rng.randint(50, 500)
            pool = list("zzzzZZZZ") + list("0123456789") * 5
            s = "".join(rng.choice(pool) for _ in range(n))
            cases.append(f"{n}\n{s}")
        return cases

    if group == 3:
        while len(cases) < TESTS_PER_GROUP:
            if len(cases) % 4 == 0:
                n = rng.randint(10, 100)
                s = "".join(rng.choice("23456789abcdef") for _ in range(n))
            else:
                n = rng.randint(500, 5000)
                s = "".join(rng.choice(DIGITS) for _ in range(n))
            cases.append(f"{n}\n{s}")
        return cases

    while len(cases) < TESTS_PER_GROUP:
        n = 50_000 if len(cases) < 3 else rng.randint(40_000, 50_000)
        s = "".join(rng.choice(DIGITS) for _ in range(n))
        cases.append(f"{n}\n{s}")
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
