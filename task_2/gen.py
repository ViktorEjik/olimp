#!/usr/bin/env python3
"""
Task 2 test generator. 25 points per group (1–4).

Group 1: K ≤ 6, sample, few blocks
Group 2: K ≤ 50, ~10^4 votes
Group 3: long chain, ambiguous corruption (many 1s)
Group 4: K = 255, up to 10^6 votes
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

SAMPLE = "6\n10 0 1 2 3 4 5 6 1 2 1 3\n0 28\n"
M = 1_999_871


def has_unique_solution(case: str) -> bool:
    sys.path.insert(0, str(TASK_DIR))
    try:
        from solution import parse_blocks, solve  # noqa: WPS433

        tokens = list(map(int, case.split()))
        solve(*parse_blocks(tokens))
        return True
    except (ValueError, ImportError):
        return False
    finally:
        if str(TASK_DIR) in sys.path:
            sys.path.remove(str(TASK_DIR))


def corrupt_votes(votes: list[int]) -> list[int]:
    return [v - 1 if v > 1 else 1 for v in votes]


def build_chain(k: int, blocks: list[list[int]], corrupt_idx: int | None) -> str:
    tokens = [k]
    prev_sum = 0
    for bi, true_votes in enumerate(blocks):
        stored = corrupt_votes(true_votes) if corrupt_idx == bi else true_votes
        tokens.append(len(stored))
        tokens.append(prev_sum % M)
        tokens.extend(stored)
        prev_sum = sum(true_votes)
    tokens.append(0)
    tokens.append(prev_sum % M)
    return " ".join(map(str, tokens)) + "\n"


def random_chain(
    rng: random.Random,
    k: int,
    n_blocks: int,
    votes_total: int,
    corrupt: int | None,
    tries: int = 50,
) -> str:
    for _ in range(tries):
        blocks = random_blocks(rng, k, n_blocks, votes_total)
        case = build_chain(k, blocks, corrupt)
        if has_unique_solution(case):
            return case
    blocks = random_blocks(rng, k, n_blocks, votes_total)
    return build_chain(k, blocks, None)


def random_blocks(rng: random.Random, k: int, n_blocks: int, votes_total: int) -> list[list[int]]:
    blocks: list[list[int]] = []
    remaining = votes_total
    for bi in range(n_blocks):
        if bi == n_blocks - 1:
            cnt = remaining
        else:
            cnt = rng.randint(1, max(1, remaining - (n_blocks - bi - 1)))
        remaining -= cnt
        blocks.append([rng.randint(1, k) for _ in range(cnt)])
    return blocks


def cases_for_group(group: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    if group == 1:
        base = [
            SAMPLE,
            build_chain(3, [[1, 2, 1], [2, 3]], None),
            build_chain(4, [[2, 2, 2, 3], [4, 2]], 0),
        ]
        while len(base) < TESTS_PER_GROUP:
            k = rng.randint(2, 6)
            corrupt = rng.choice([None, 0])
            base.append(
                random_chain(rng, k, rng.randint(2, 5), rng.randint(5, 50), corrupt)
            )
        return base[:TESTS_PER_GROUP]

    if group == 2:
        cases = []
        for _ in range(TESTS_PER_GROUP):
            k = rng.randint(10, 50)
            total = rng.randint(1000, 10_000)
            corrupt = rng.choice([None, 0])
            cases.append(
                random_chain(rng, k, rng.randint(5, 40), total, corrupt)
            )
        return cases

    if group == 3:
        cases = []
        for _ in range(TESTS_PER_GROUP // 2):
            k = rng.randint(5, 20)
            block = [1] * rng.randint(10, 30)
            blocks = [block, [rng.randint(2, k) for _ in range(rng.randint(5, 15))]]
            case = build_chain(k, blocks, 0)
            if has_unique_solution(case):
                cases.append(case)
        while len(cases) < TESTS_PER_GROUP:
            k = rng.randint(20, 60)
            total = rng.randint(5000, 30_000)
            cases.append(random_chain(rng, k, rng.randint(10, 40), total, None))
        return cases

    cases = []
    for _ in range(TESTS_PER_GROUP):
        k = 255
        total = rng.randint(800_000, 1_000_000)
        cases.append(random_chain(rng, k, rng.randint(80, 200), total, None))
    return cases


def main() -> None:
    parser = argparse.ArgumentParser(description=f"Task 2 generator ({POINTS_PER_GROUP} pts/group)")
    add_gen_args(parser)
    args = parser.parse_args()
    seed = default_seed(args.group, args.seed)
    cases = cases_for_group(args.group, seed)
    write_tests(TASK_DIR, args.out, args.group, cases)
    print(f"Wrote {len(cases)} tests to {args.out / f'group{args.group}'}")


if __name__ == "__main__":
    main()
