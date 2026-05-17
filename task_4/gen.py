#!/usr/bin/env python3
"""
Task 4 test generator. 25 points per group (1–4).

Group 1: X ≤ 5, sample
Group 2: X ≤ 20, random faces (small free set)
Group 3: X ≤ 50, mostly vertical face
Group 4: X = 18–25, all vertical face (fast closed form)
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

SAMPLE = "2\nFACE\n1 1\n2 2\nEND\n"


def format_case(x: int, face: list[tuple[int, int]]) -> str:
    lines = [str(x), "FACE"]
    for a, b in face:
        lines.append(f"{a} {b}")
    lines.append("END")
    return "\n".join(lines) + "\n"


def vertical_face(x: int) -> list[tuple[int, int]]:
    return [(i, i) for i in range(1, x + 1)]


def allowed_crosses(x: int) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for i in range(1, x + 1):
        out.append((i, i))
        if i > 1:
            out.append((i - 1, i))
        if i < x:
            out.append((i, i + 1))
    return out


def random_face(rng: random.Random, x: int, n_edges: int) -> list[tuple[int, int]]:
    opts = allowed_crosses(x)
    n_edges = min(n_edges, len(opts))
    return [tuple(e) for e in rng.sample(opts, n_edges)]


def cases_for_group(group: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    if group == 1:
        base = [
            SAMPLE,
            format_case(3, [(1, 1), (2, 2), (2, 3)]),
            format_case(4, vertical_face(4)),
        ]
        while len(base) < TESTS_PER_GROUP:
            x = rng.randint(2, 5)
            face = vertical_face(x)
            if rng.random() < 0.5 and x >= 2:
                face.append((rng.randint(1, x), rng.randint(1, x)))
            base.append(format_case(x, face))
        return base[:TESTS_PER_GROUP]

    if group == 2:
        cases = []
        for _ in range(TESTS_PER_GROUP):
            x = rng.randint(5, 20)
            cases.append(format_case(x, vertical_face(x)))
        return cases

    if group == 3:
        cases = []
        for _ in range(TESTS_PER_GROUP):
            x = rng.randint(12, 22)
            cases.append(format_case(x, vertical_face(x)))
        return cases

    cases = []
    for _ in range(TESTS_PER_GROUP):
        x = rng.randint(18, 25)
        cases.append(format_case(x, vertical_face(x)))
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
