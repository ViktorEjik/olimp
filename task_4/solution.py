#!/usr/bin/env python3
"""Task 4: Gnome chests — parse/encode gnome numerals, optimal pair."""

from __future__ import annotations

import sys

TOKENS: list[tuple[str, int]] = [
    (">!!!", 4),
    (">!!", 3),
    (">!", 2),
    ("<?>", 10),
    ("<!!!", 9),
    ("<!!", 8),
    ("<!", 7),
    (">?", 5),
    (">", 1),
    ("<", 6),
]
TOKEN_BY_VAL: dict[int, str] = {v: t for t, v in TOKENS}
SORTED_TOKENS = sorted(TOKENS, key=lambda x: -len(x[0]))


def parse_gnome(s: str) -> int:
    s = s.strip()
    if s == "()":
        return 0
    pos = 0
    total = 0
    power = 0
    while pos < len(s):
        matched = False
        for tok, val in SORTED_TOKENS:
            if s.startswith(tok, pos):
                total += val * (10**power)
                power += 1
                pos += len(tok)
                matched = True
                break
        if not matched:
            raise ValueError(f"cannot parse gnome at {pos}")
    return total


def encode_gnome(n: int) -> str:
    if n == 0:
        return "()"
    parts: list[str] = []
    while n > 0:
        d = n % 10
        n //= 10
        digit = 10 if d == 0 else d
        parts.append(TOKEN_BY_VAL[digit])
    return "".join(parts)


def solve(lines: list[str]) -> tuple[str, str]:
    n = int(lines[0])
    values = [parse_gnome(lines[i + 1]) for i in range(n)]
    best_diff = max(abs(values[i] - values[j]) for i in range(n) for j in range(i + 1, n))
    best_kl: tuple[int, int] | None = None
    for i in range(n):
        for j in range(i + 1, n):
            if abs(values[i] - values[j]) != best_diff:
                continue
            k, l = i + 1, j + 1
            if best_kl is None or k + l < best_kl[0] + best_kl[1]:
                best_kl = (k, l)
    assert best_kl is not None
    return encode_gnome(best_kl[0]), encode_gnome(best_kl[1])


def main() -> None:
    lines = [ln.rstrip("\r") for ln in sys.stdin.read().splitlines()]
    while lines and lines[-1] == "":
        lines.pop()
    k, l = solve(lines)
    print(k)
    print(l)


if __name__ == "__main__":
    main()
