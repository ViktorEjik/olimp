#!/usr/bin/env python3
"""Task 1: count tetra-evil numbers (even ones in tetranacci representation)."""

from __future__ import annotations

import sys

T: list[int] = [0, 0, 0, 1]
while T[-1] < 2**24:
    T.append(T[-1] + T[-2] + T[-3] + T[-4])


def ones_in_representation(n: int) -> int:
    if n == 0:
        return 0
    hi = max(p for p in range(0, len(T) - 4) if T[p + 4] <= n)
    rem = n
    cnt = 0
    prev3 = 0
    for p in range(hi, -1, -1):
        w = T[p + 4]
        use = 1 if w <= rem and (prev3 & 7) != 7 else 0
        if use:
            rem -= w
            cnt += 1
        prev3 = ((prev3 << 1) | use) & 7
    if rem != 0:
        raise ValueError(f"cannot represent {n}")
    return cnt


def is_tetra_evil(n: int) -> bool:
    return ones_in_representation(n) % 2 == 0


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = [int(x) for x in data[1 : 1 + n]]
    ans = sum(1 for x in nums if is_tetra_evil(x))
    print(ans)


if __name__ == "__main__":
    main()
