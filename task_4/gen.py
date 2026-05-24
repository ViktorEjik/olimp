#!/usr/bin/env python3
"""
Task 4 test generator. 25 points per group.

Group 1: N<=5, short strings, official sample
Group 2: N<=50
Group 3: N<=200, long strings, tie-break K+L
Group 4: N=500, len<=100
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from gen_common import TESTS_PER_GROUP, add_cli, write_tests  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from solution import encode_gnome  # noqa: E402

OFFICIAL = "2\n()\n>!!!>!<?>"

DIGIT_TOKENS = [">", ">!", ">!!", ">!!!", ">?", "<", "<!", "<!!", "<!!!", "<?"]


def random_gnome_value(rng: random.Random, max_digits: int = 8) -> str:
    if rng.random() < 0.1:
        return "()"
    n = rng.randint(1, 10**max_digits - 1)
    return encode_gnome(n)


def build_cases(group: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    cases: list[str] = []

    if group == 1:
        cases.append(OFFICIAL)
        while len(cases) < TESTS_PER_GROUP:
            n = rng.randint(2, 5)
            rows = [random_gnome_value(rng, 3) for _ in range(n)]
            cases.append(str(n) + "\n" + "\n".join(rows))
        return cases

    if group == 2:
        while len(cases) < TESTS_PER_GROUP:
            n = rng.randint(2, 50)
            rows = [random_gnome_value(rng, 5) for _ in range(n)]
            cases.append(str(n) + "\n" + "\n".join(rows))
        return cases

    if group == 3:
        while len(cases) < TESTS_PER_GROUP:
            n = rng.randint(50, 200)
            rows = []
            for i in range(n):
                if i < 2:
                    rows.append(random_gnome_value(rng, 12))
                else:
                    rows.append(random_gnome_value(rng, 8))
            cases.append(str(n) + "\n" + "\n".join(rows))
        return cases

    while len(cases) < TESTS_PER_GROUP:
        n = 500 if len(cases) % 2 == 0 else rng.randint(400, 500)
        rows = [random_gnome_value(rng, 15) for _ in range(n)]
        cases.append(str(n) + "\n" + "\n".join(rows))
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
