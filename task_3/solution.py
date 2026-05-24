#!/usr/bin/env python3
"""Task 3: Elevator — shortest path; tie-break: lexicographically minimal AB-string."""

import sys
from collections import deque

FLOOR_LIMIT = 10**6
INF = 10**9


def solve_one(a: int, b: int, target: int) -> list[str]:
    if target == 0:
        return []

    start = 0
    dist: dict[int, int] = {start: 0}
    best: dict[int, str] = {start: ""}
    q = deque([start])

    while q:
        floor = q.popleft()
        d = dist[floor]
        path = best[floor]
        for op, nxt in (("A", floor + a), ("B", floor * b)):
            if abs(nxt) > FLOOR_LIMIT:
                continue
            nd = d + 1
            cand = path + op
            if nxt not in dist or nd < dist[nxt] or (nd == dist[nxt] and cand < best[nxt]):
                if nxt not in dist:
                    q.append(nxt)
                dist[nxt] = nd
                best[nxt] = cand
                if nxt == target:
                    return list(cand)

    if target not in dist:
        return []
    return list(best[target])


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    a = int(next(it))
    b = int(next(it))
    out_lines: list[str] = []
    for _ in range(n):
        x = int(next(it))
        path = solve_one(a, b, x)
        if not path:
            out_lines.append("0")
        else:
            out_lines.extend(path)
    sys.stdout.write("\n".join(out_lines) + ("\n" if out_lines else ""))


if __name__ == "__main__":
    main()
