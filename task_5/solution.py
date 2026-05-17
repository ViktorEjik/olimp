#!/usr/bin/env python3
"""Task 5: Maximum factorial-base (FBC) number from multiset."""

from __future__ import annotations

import sys

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
VAL = {ch: i for i, ch in enumerate(DIGITS)}
MAX_POS = 61


def max_length(counts: list[int]) -> int:
    length = 0
    for k in range(1, MAX_POS + 1):
        if sum(counts[d] for d in range(k + 1)) >= k:
            length = k
        else:
            break
    return length


def construct(counts: list[int], length: int) -> str:
    result: list[str] = []
    for pos in range(length, 0, -1):
        for d in range(min(pos, MAX_POS), -1, -1):
            if counts[d] > 0:
                counts[d] -= 1
                result.append(DIGITS[d])
                break
    while len(result) > 1 and result[0] == "0":
        result.pop(0)
    return "".join(result)


def solve(s: str) -> str:
    counts = [0] * 62
    for ch in s:
        if ch not in VAL:
            return "-1"
        counts[VAL[ch]] += 1
    if sum(counts) == 0:
        return "-1"
    length = max_length(counts)
    if length == 0:
        return "0" if counts[0] > 0 else "-1"
    ans = construct(counts[:], length)
    return ans if ans else "-1"


def main() -> None:
    data = sys.stdin.read().splitlines()
    n = int(data[0].strip())
    s = data[1].strip()[:n]
    print(solve(s))


if __name__ == "__main__":
    main()
