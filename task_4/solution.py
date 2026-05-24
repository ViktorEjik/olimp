#!/usr/bin/env python3
"""Task 4: Gnome chests — parse gnome numerals, max |S_K - S_L|."""

import sys

DIGITS = [
    (10, "<?"),
    (9, "<!!!"),
    (8, "<!!"),
    (7, "<!"),
    (6, "<"),
    (5, ">?"),
    (4, ">!!!"),
    (3, ">!!"),
    (2, ">!"),
    (1, ">"),
]
TOKEN_BY_LEN = sorted(
    [("()", 0)] + [(s, v) for v, s in DIGITS],
    key=lambda x: -len(x[0]),
)


def parse_gnome(s: str) -> int:
    if s == "()":
        return 0
    pos = 0
    n = len(s)
    value = 0
    power = 0
    while pos < n:
        for tok, digit in TOKEN_BY_LEN:
            if s.startswith(tok, pos):
                value += digit * (10**power)
                pos += len(tok)
                power += 1
                break
        else:
            raise ValueError(f"bad gnome numeral at {pos}: {s!r}")
    return value


def encode_gnome(n: int) -> str:
    if n == 0:
        return "()"
    parts: list[str] = []
    x = n
    while x > 0:
        x, r = divmod(x - 1, 10)
        digit = r + 1  # digits 1..10, no zero
        for val, tok in DIGITS:
            if val == digit:
                parts.append(tok)
                break
    return "".join(parts)


def solve(lines: list[str]) -> tuple[str, str]:
    n = int(lines[0])
    values = [parse_gnome(lines[i + 1]) for i in range(n)]
    min_val = min(values)
    max_val = max(values)
    target_diff = max_val - min_val
    best_k = best_l = None
    best_sum = None
    for i in range(n):
        for j in range(i + 1, n):
            if abs(values[i] - values[j]) != target_diff:
                continue
            s = (i + 1) + (j + 1)
            if best_sum is None or s < best_sum:
                best_sum = s
                best_k, best_l = i + 1, j + 1
    assert best_k is not None and best_l is not None
    return encode_gnome(best_k), encode_gnome(best_l)


def main() -> None:
    lines = sys.stdin.read().splitlines()
    while lines and lines[-1] == "":
        lines.pop()
    k, l = solve(lines)
    print(k)
    print(l)


if __name__ == "__main__":
    main()
