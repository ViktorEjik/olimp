#!/usr/bin/env python3
"""Task 3: minimum operations to reach 1; lexicographically smallest optimal path."""

from __future__ import annotations

import sys
from collections import deque

# First shortest path in BFS with this neighbor order (matches official sample 100 -> 2313).
OP_ORDER = "132456"


def strip_leading_zeros(s: str) -> str:
    s = s.lstrip("0")
    return s if s else "0"


def neighbors(s: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    n = int(s)
    out.append((str(n * 2), "1"))
    if n % 2 == 0:
        out.append((str(n // 2), "2"))
    if len(s) % 2 == 0:
        half = len(s) // 2
        out.append((strip_leading_zeros(s[:half]), "3"))
        out.append((strip_leading_zeros(s[half:]), "4"))
        out.append((strip_leading_zeros(s[:half] + s[half:]), "5"))
        out.append((strip_leading_zeros(s[half:] + s[:half]), "6"))
    return out


def solve(s: str) -> tuple[int, str] | None:
    if s == "1":
        return 0, ""
    dist: dict[str, int] = {s: 0}
    parent: dict[str, str] = {s: ""}
    q: deque[str] = deque([s])
    while q:
        cur = q.popleft()
        if cur == "1":
            return dist[cur], parent[cur]
        nd = dist[cur] + 1
        for nxt, op in sorted(neighbors(cur), key=lambda x: OP_ORDER.index(x[1])):
            if nxt not in dist:
                dist[nxt] = nd
                parent[nxt] = parent[cur] + op
                q.append(nxt)
    return None


def main() -> None:
    s = sys.stdin.read().strip()
    if not s:
        return
    res = solve(s)
    if res is None:
        print(-1)
        return
    length, path = res
    print(length)
    if length > 0:
        print(path)


if __name__ == "__main__":
    main()
