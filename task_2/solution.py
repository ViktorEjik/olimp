#!/usr/bin/env python3
"""Task 2: recover vote counts from blockchain with at most one corrupted block."""

from __future__ import annotations

import sys

M = 1_999_871


def parse_blocks(tokens: list[int]) -> tuple[int, list[tuple[int, int, list[int]]]]:
    k = tokens[0]
    i = 1
    blocks: list[tuple[int, int, list[int]]] = []
    while i < len(tokens):
        count = tokens[i]
        total = tokens[i + 1]
        i += 2
        if count == 0:
            blocks.append((0, total, []))
            break
        votes = tokens[i : i + count]
        i += count
        blocks.append((count, total, votes))
    return k, blocks


def uncorrupt_candidates(stored: list[int], required_mod: int) -> list[list[int]]:
    fixed_sum = sum(v + 1 for v in stored if v > 1)
    n1 = sum(1 for v in stored if v == 1)
    out: list[list[int]] = []
    for need_twos in range(n1 + 1):
        total = fixed_sum + n1 + need_twos
        if total % M != required_mod:
            continue
        true: list[int] = []
        twos_left = need_twos
        for v in stored:
            if v > 1:
                true.append(v + 1)
            elif twos_left > 0:
                true.append(2)
                twos_left -= 1
            else:
                true.append(1)
        out.append(true)
    return out


def run_chain(
    k: int,
    blocks: list[tuple[int, int, list[int]]],
    corrupt_idx: int | None,
    true_at_corrupt: list[int] | None,
) -> list[int] | None:
    totals = [0] * (k + 1)
    prev_sum = 0
    data_blocks = len(blocks) - 1

    for bi in range(data_blocks):
        c, s, stored = blocks[bi]
        if bi == 0:
            if s != 0:
                return None
        elif s != prev_sum % M:
            return None

        if corrupt_idx == bi:
            if true_at_corrupt is None:
                return None
            true_votes = true_at_corrupt
        else:
            true_votes = stored

        for v in true_votes:
            if v < 1 or v > k:
                return None
            totals[v] += 1
        prev_sum = sum(true_votes)

    if blocks[-1][0] != 0 or blocks[-1][1] != prev_sum % M:
        return None
    return totals[1:]


def solve_with_corrupt(
    k: int, blocks: list[tuple[int, int, list[int]]], corrupt_idx: int | None
) -> list[int] | None:
    if corrupt_idx is None:
        return run_chain(k, blocks, None, None)

    stored = blocks[corrupt_idx][2]
    required = blocks[corrupt_idx + 1][1]
    answers: list[list[int]] = []
    for true_votes in uncorrupt_candidates(stored, required):
        res = run_chain(k, blocks, corrupt_idx, true_votes)
        if res is not None:
            answers.append(res)
    if len(answers) != 1:
        return None
    return answers[0]


def solve(k: int, blocks: list[tuple[int, int, list[int]]]) -> list[int]:
    if not blocks or blocks[-1][0] != 0:
        raise ValueError("invalid blockchain")
    answers: list[list[int]] = []
    for corrupt in [None, *range(len(blocks) - 1)]:
        res = solve_with_corrupt(k, blocks, corrupt)
        if res is not None:
            answers.append(res)
    if len(answers) != 1:
        raise ValueError(f"expected unique solution, got {len(answers)}")
    return answers[0]


def main() -> None:
    tokens = list(map(int, sys.stdin.read().split()))
    k, blocks = parse_blocks(tokens)
    totals = solve(k, blocks)
    print(" ".join(map(str, totals)))


if __name__ == "__main__":
    main()
