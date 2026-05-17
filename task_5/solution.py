#!/usr/bin/env python3
"""Task 5: minimum tiles visited on hexagonal-snub grid (O(1) metric)."""

from __future__ import annotations

import sys


def min_tiles(a1: int, b1: int, a2: int, b2: int) -> int:
    if a1 == a2 and b1 == b2:
        return 1
    du = a2 - a1
    dv = b2 - b1
    dw = -(du + dv)
    d = max(abs(du), abs(dv), abs(dw))
    return d + 1


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    a1, b1, a2, b2 = data[:4]
    print(min_tiles(a1, b1, a2, b2))


if __name__ == "__main__":
    main()
