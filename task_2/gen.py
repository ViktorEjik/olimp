#!/usr/bin/env python3
"""
Task 2 test generator. 25 points per group.

Group 1: small trees, official sample
Group 2: random, len<=100
Group 3: deep trees, tie-break cases
Group 4: max length 1365
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from gen_common import TESTS_PER_GROUP, add_cli, write_tests  # noqa: E402

COLORS = "WROYGCBVD"
OFFICIAL = "QDWWQDDDW"


def random_tree(rng: random.Random, max_depth: int) -> str:
    def build(depth: int) -> str:
        if depth >= max_depth or (depth > 1 and rng.random() < 0.35):
            return rng.choice(COLORS)
        return "Q" + "".join(build(depth + 1) for _ in range(4))

    return build(1)


def tie_tree(rng: random.Random) -> str:
    # Four equal quarters, two colors tie for 1/2 each — pick later in TIE_ORDER
    c1, c2 = rng.sample("BCDGORVWY", 2)
    return f"Q{c1}{c1}{c2}{c2}"


def max_tree() -> str:
    def build(depth: int) -> str:
        if depth == 0:
            return "W"
        return "Q" + "".join(build(depth - 1) for _ in range(4))

    return build(5)  # length (4^6 - 1) / 3 = 1365


def build_cases(group: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    cases: list[str] = []

    if group == 1:
        cases.append(OFFICIAL)
        cases.extend([rng.choice(COLORS) for _ in range(3)])
        while len(cases) < TESTS_PER_GROUP:
            cases.append(random_tree(rng, max_depth=3))
        return cases[:TESTS_PER_GROUP]

    if group == 2:
        while len(cases) < TESTS_PER_GROUP:
            depth = rng.randint(2, 5)
            t = random_tree(rng, depth)
            if len(t) <= 100:
                cases.append(t)
        return cases

    if group == 3:
        cases.append(tie_tree(rng))
        while len(cases) < TESTS_PER_GROUP:
            if rng.random() < 0.4:
                cases.append(tie_tree(rng))
            else:
                cases.append(random_tree(rng, max_depth=7))
        return cases

    cases.append(max_tree())

    def large_tree() -> str:
        s = rng.choice(COLORS)
        while len(s) < 1200:
            leaves = [i for i, ch in enumerate(s) if ch != "Q"]
            i = rng.choice(leaves)
            c = s[i]
            s = s[:i] + "Q" + c * 4 + s[i + 1 :]
            if len(s) > 1365:
                return max_tree()
        return s

    while len(cases) < TESTS_PER_GROUP:
        cases.append(large_tree())
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
