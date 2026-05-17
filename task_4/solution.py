#!/usr/bin/env python3
"""Task 4: count valid nonempty back-side lacings (face + back + row edges)."""

from __future__ import annotations

import sys


def allowed_crosses(x: int) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for i in range(1, x + 1):
        out.append((i, i))
        if i > 1:
            out.append((i - 1, i))
        if i < x:
            out.append((i, i + 1))
    return out


def is_valid_lacing(x: int, face: set[tuple[int, int]], back: set[tuple[int, int]]) -> bool:
    if face & back:
        return False
    cross = face | back

    def vid_top(i: int) -> int:
        return 2 * (i - 1)

    def vid_bot(i: int) -> int:
        return 2 * (i - 1) + 1

    adj: list[list[int]] = [[] for _ in range(2 * x)]
    for i in range(1, x):
        u, v = vid_top(i), vid_top(i + 1)
        adj[u].append(v)
        adj[v].append(u)
        u, v = vid_bot(i), vid_bot(i + 1)
        adj[u].append(v)
        adj[v].append(u)
    for a, b in cross:
        u, v = vid_top(a), vid_bot(b)
        adj[u].append(v)
        adj[v].append(u)

    seen = [False] * (2 * x)

    def dfs(u: int, depth: int) -> bool:
        if depth == 2 * x:
            return True
        seen[u] = True
        for v in adj[u]:
            if not seen[v]:
                if dfs(v, depth + 1):
                    seen[u] = False
                    return True
        seen[u] = False
        return False

    return any(dfs(s, 1) for s in range(2 * x))


def brute_count(x: int, face: set[tuple[int, int]], nonempty: bool) -> int:
    free = [e for e in allowed_crosses(x) if e not in face]
    total = 0
    for mask in range(1, 1 << len(free)):
        back = {free[i] for i in range(len(free)) if mask & (1 << i)}
        if is_valid_lacing(x, face, back):
            total += 1
    return total


def all_vertical_face(x: int, face: set[tuple[int, int]]) -> bool:
    return len(face) == x and all(a == b for a, b in face)


def count_back(x: int, face_pairs: list[tuple[int, int]]) -> int:
    face = set(face_pairs)
    free = [e for e in allowed_crosses(x) if e not in face]
    if all_vertical_face(x, face):
        return (1 << len(free)) - 1
    if len(free) <= 26:
        return brute_count(x, face, nonempty=True)
    return brute_count(x, face, nonempty=True)


def parse_input(lines: list[str]) -> tuple[int, list[tuple[int, int]]]:
    x = int(lines[0])
    i = 1
    if lines[i].strip() != "FACE":
        raise ValueError("expected FACE")
    i += 1
    face: list[tuple[int, int]] = []
    while i < len(lines) and lines[i].strip() != "END":
        a, b = map(int, lines[i].split())
        face.append((a, b))
        i += 1
    return x, face


def main() -> None:
    lines = [ln.rstrip("\r") for ln in sys.stdin.read().splitlines()]
    while lines and lines[-1] == "":
        lines.pop()
    x, face = parse_input(lines)
    print(count_back(x, face))


if __name__ == "__main__":
    main()
