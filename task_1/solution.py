#!/usr/bin/env python3
"""Task 1: Superfractions — maximize sum of three fractions from 6 numbers."""

import sys
from fractions import Fraction
from itertools import permutations


def solve(nums: list[int]) -> tuple[int, int]:
    best: Fraction | None = None
    for k, l, m, n, p, q in permutations(nums):
        if l == 0 or n == 0 or q == 0:
            continue
        val = Fraction(k, l) + Fraction(m, n) + Fraction(p, q)
        if best is None or val > best:
            best = val
    assert best is not None
    return best.numerator, best.denominator


def main() -> None:
    nums = list(map(int, sys.stdin.read().split()))
    x, y = solve(nums)
    print(x, y)


if __name__ == "__main__":
    main()
