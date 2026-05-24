#!/usr/bin/env python3
"""Task 5: Maximum valid factorial-base (FBC) number from multiset."""

import sys

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
VAL = {c: i for i, c in enumerate(DIGITS)}


def solve(s: str) -> str:
    freq = [0] * 62
    for ch in s:
        if ch in VAL:
            freq[VAL[ch]] += 1

    length = 0
    for k in range(1, 62):
        if sum(freq[0 : k + 1]) >= k:
            length = k
        else:
            break

    if length == 0:
        return "0" if freq[0] else "-1"

    remaining = freq[:]
    result: list[str] = []

    for pos in range(length, 0, -1):
        for d in range(min(pos, 61), -1, -1):
            if remaining[d] > 0:
                result.append(DIGITS[d])
                remaining[d] -= 1
                break
        else:
            return "-1"

    while len(result) > 1 and result[0] == "0":
        result.pop(0)

    return "".join(result)


def main() -> None:
    data = sys.stdin.read().splitlines()
    n = int(data[0])
    s = data[1].strip()[:n]
    print(solve(s))


if __name__ == "__main__":
    main()
