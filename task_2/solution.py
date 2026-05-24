#!/usr/bin/env python3
"""Task 2: Quadtree — max area color + binary fraction output."""

import sys
from fractions import Fraction

TIE_ORDER = "BCDGORVWY"


def format_binary(frac: Fraction) -> str:
    if frac == 0:
        return "0.0"
    if frac == 1:
        return "1.0"
    n = frac.numerator
    d = frac.denominator
    whole = n // d
    rem = n % d
    bits: list[str] = []
    for _ in range(60):
        rem *= 2
        bits.append("1" if rem >= d else "0")
        rem %= d
        if rem == 0:
            break
    while bits and bits[-1] == "0":
        bits.pop()
    if not bits:
        return f"{whole}.0"
    return f"{whole}." + "".join(bits)


def solve(s: str) -> tuple[str, str]:
    areas: dict[str, Fraction] = {}

    def parse(pos: list[int], depth: int) -> None:
        ch = s[pos[0]]
        pos[0] += 1
        if ch == "Q":
            for _ in range(4):
                parse(pos, depth + 1)
        else:
            area = Fraction(1, 4 ** (depth - 1))
            areas[ch] = areas.get(ch, Fraction(0)) + area

    parse([0], 1)
    max_area = max(areas.values())
    best_color = max(
        (c for c, a in areas.items() if a == max_area),
        key=lambda c: TIE_ORDER.index(c),
    )
    return best_color, format_binary(max_area)


def main() -> None:
    s = sys.stdin.readline().strip()
    color, area = solve(s)
    print(color)
    print(area)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        assert format_binary(Fraction(9, 16)) == "0.1001"
        assert format_binary(Fraction(0)) == "0.0"
        assert format_binary(Fraction(1)) == "1.0"
        print("ok")
    else:
        main()
