#!/usr/bin/env python3
"""
Task 5 test generator. 25 points per group (1–4).

Group 1: N ≤ 20, sample, digits 0-9
Group 2: N ≤ 500, cases breaking naive sort
Group 3: N ≤ 5000, -1 answers
Group 4: N = 50000, full alphabet
"""

from __future__ import annotations

import argparse
import random
import string
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from gen_common import POINTS_PER_GROUP, TESTS_PER_GROUP, add_gen_args, default_seed, write_tests

TASK_DIR = Path(__file__).resolve().parent
DIGITS = string.digits + string.ascii_lowercase + string.ascii_uppercase
SAMPLE = "15\naA334422551100\n"


def random_string(rng: random.Random, n: int, alphabet: str) -> str:
    return "".join(rng.choice(alphabet) for _ in range(n))


def impossible_case(rng: random.Random) -> str:
    """Many high letters, cannot satisfy position constraints."""
    n = rng.randint(30, 80)
    s = random_string(rng, n, "zZYXWV")
    return f"{n}\n{s}\n"


def cases_for_group(group: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    if group == 1:
        cases = [SAMPLE, f"3\n012\n", f"5\n00000\n"]
        while len(cases) < TESTS_PER_GROUP:
            n = rng.randint(5, 20)
            cases.append(f"{n}\n{random_string(rng, n, string.digits)}\n")
        return cases[:TESTS_PER_GROUP]

    if group == 2:
        cases = []
        for _ in range(TESTS_PER_GROUP):
            n = rng.randint(50, 500)
            # mix many large letters
            s = random_string(rng, n, "aA" + string.digits)
            cases.append(f"{n}\n{s}\n")
        return cases

    if group == 3:
        cases = [impossible_case(rng) for _ in range(3)]
        while len(cases) < TESTS_PER_GROUP:
            n = rng.randint(500, 5000)
            cases.append(f"{n}\n{random_string(rng, n, DIGITS)}\n")
        return cases[:TESTS_PER_GROUP]

    cases = []
    for _ in range(TESTS_PER_GROUP):
        n = 50000
        cases.append(f"{n}\n{random_string(rng, n, DIGITS)}\n")
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
