#!/usr/bin/env python3
"""Task 3: Lift — BFS shortest path; tie-break: prefer B over A when backtracking."""

from __future__ import annotations

import sys
from collections import deque

STATE_LIMIT = 2_000_000


def bfs_dist(a: int, b: int) -> dict[int, int]:
    dist: dict[int, int] = {0: 0}
    q: deque[int] = deque([0])
    while q:
        floor = q.popleft()
        d = dist[floor]
        for nxt in (floor + a, floor * b):
            if abs(nxt) > STATE_LIMIT:
                continue
            if nxt not in dist:
                dist[nxt] = d + 1
                q.append(nxt)
    return dist


def shortest_path(a: int, b: int, target: int, dist: dict[int, int]) -> str | None:
    if target not in dist:
        return None
    steps: list[str] = []
    cur = target
    while cur != 0:
        d = dist[cur]
        chosen: tuple[str, int] | None = None
        if b != 0 and cur % b == 0:
            prev = cur // b
            if dist.get(prev) == d - 1:
                chosen = ("B", prev)
        if chosen is None:
            prev = cur - a
            if dist.get(prev) == d - 1:
                chosen = ("A", prev)
        if chosen is None:
            return None
        sym, cur = chosen
        steps.append(sym)
    steps.reverse()
    return "".join(steps)


def solve_case(a: int, b: int, target: int) -> list[str]:
    if target == 0:
        return ["0"]
    dist = bfs_dist(a, b)
    path = shortest_path(a, b, target, dist)
    if path is None:
        return ["0"]
    return list(path)


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
        out_lines.extend(solve_case(a, b, x))
    sys.stdout.write("\n".join(out_lines))
    if out_lines:
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
