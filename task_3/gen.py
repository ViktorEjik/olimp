#!/usr/bin/env python3
"""
Task 3 test generator. 25 points per group (100 total).

Group 1: N=1..3, small |A|,|B|,|X|
Group 2: N<=50, |values|<=100
Group 3: N<=200, negative A/B, many unreachable X
Group 4: N<=999, |values|<1000 (statement max)
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from gen_common import TESTS_PER_GROUP, add_cli, write_tests  # noqa: E402

OFFICIAL = "1 1 2\n9\n"


def build_cases(group: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    cases: list[str] = []

    if group == 1:
        cases.append(OFFICIAL)
        presets = [
            (1, 2, 3, [5]),
            (2, 1, 2, [3, 7]),
            (1, 3, 2, [27]),
            (1, -1, 2, [4]),
            (1, 5, 2, [31]),
        ]
        for n, a, b, xs in presets:
            lines = [f"{n} {a} {b}"] + [str(x) for x in xs]
            cases.append("\n".join(lines))
        while len(cases) < TESTS_PER_GROUP:
            n = rng.randint(1, 3)
            a = rng.randint(1, 5)
            b = rng.choice([2, 3, -2])
            if a == 0 or b == 0:
                continue
            xs = [rng.randint(1, 20) for _ in range(n)]
            cases.append(f"{n} {a} {b}\n" + "\n".join(map(str, xs)))
        return cases[:TESTS_PER_GROUP]

    if group == 2:
        while len(cases) < TESTS_PER_GROUP:
            n = rng.randint(1, 50)
            a = rng.randint(-100, 100)
            b = rng.randint(-100, 100)
            if a == 0 or b == 0:
                continue
            xs = [rng.randint(-99, 99) or 1 for _ in range(n)]
            cases.append(f"{n} {a} {b}\n" + "\n".join(map(str, xs)))
        return cases

    if group == 3:
        while len(cases) < TESTS_PER_GROUP:
            n = rng.randint(50, 200)
            a = rng.randint(-500, 500)
            b = rng.randint(-500, 500)
            if a == 0 or b == 0:
                continue
            xs = []
            for _ in range(n):
                if rng.random() < 0.3:
                    xs.append(rng.choice([997, 999, 503, 127]))
                else:
                    xs.append(rng.randint(-999, 999) or 1)
            cases.append(f"{n} {a} {b}\n" + "\n".join(map(str, xs)))
        return cases

    # group 4
    while len(cases) < TESTS_PER_GROUP:
        n = rng.randint(200, 999)
        a = rng.randint(-999, 999)
        b = rng.randint(-999, 999)
        if a == 0 or b == 0:
            continue
        xs = [rng.randint(-999, 999) or 1 for _ in range(n)]
        cases.append(f"{n} {a} {b}\n" + "\n".join(map(str, xs)))
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
