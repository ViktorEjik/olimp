#!/usr/bin/env python3
"""Task 2: Quadtree — max area color with tie-break B<C<D<G<O<R<V<W<Y."""

from __future__ import annotations

import sys
from fractions import Fraction

TIE_ORDER = "BCDGORVWY"
COLORS = set("WROYGCBVD")


def parse_tree(s: str, pos: int = 0, depth: int = 1) -> tuple[dict[str, Fraction], int]:
    if pos >= len(s):
        raise ValueError("unexpected end")
    ch = s[pos]
    if ch == "Q":
        total: dict[str, Fraction] = {}
        p = pos + 1
        for _ in range(4):
            child, p = parse_tree(s, p, depth + 1)
            for c, a in child.items():
                total[c] = total.get(c, Fraction(0)) + a
        return total, p
    if ch in COLORS:
        area = Fraction(1, 4 ** (depth - 1))
        return {ch: area}, pos + 1
    raise ValueError(f"invalid char {ch!r}")


def format_binary(area: Fraction) -> str:
    if area.denominator & (area.denominator - 1) != 0:
        raise ValueError("area denominator must be power of 2")
    num = area.numerator
    den = area.denominator
    if num == 0:
        return "0.0"
    if num >= den:
        whole = num // den
        frac_num = num % den
        if frac_num == 0:
            return f"{whole}.0"
        bits = []
        f = frac_num
        while f:
            f *= 2
            bits.append(str(f // den))
            f %= den
        return f"{whole}." + "".join(bits)
    bits = []
    n, d = num, den
    while n:
        n *= 2
        bits.append(str(n // d))
        n %= d
    return "0." + "".join(bits)


def solve(s: str) -> tuple[str, str]:
    areas, _ = parse_tree(s.strip())
    best_color = max(areas.keys(), key=lambda c: (areas[c], TIE_ORDER.index(c)))
    return best_color, format_binary(areas[best_color])


def main() -> None:
    s = sys.stdin.readline().strip()
    color, frac = solve(s)
    print(color)
    print(frac)


if __name__ == "__main__":
    main()
