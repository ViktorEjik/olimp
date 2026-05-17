#!/usr/bin/env python3
"""Task 1: Superfractions — maximize sum of three fractions from 6 integers."""

from __future__ import annotations

import itertools
import sys
from fractions import Fraction


def solve(nums: list[int]) -> tuple[int, int]:
    best: Fraction | None = None
    for perm in itertools.permutations(nums):
        k, l, m, n, p, q = perm
        if l == 0 or n == 0 or q == 0:
            continue
        value = Fraction(k, l) + Fraction(m, n) + Fraction(p, q)
        if best is None or value > best:
            best = value
    assert best is not None
    return best.numerator, best.denominator


def main() -> None:
    nums = list(map(int, sys.stdin.read().split()))
    x, y = solve(nums)
    print(x, y)


if __name__ == "__main__":
    main()
