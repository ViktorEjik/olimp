"""Shared utilities for olympiad test generators."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

TESTS_PER_GROUP = 10
POINTS_PER_GROUP = 25


def add_gen_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--group", type=int, required=True, choices=(1, 2, 3, 4))
    parser.add_argument("--out", type=Path, required=True, help="Output directory (e.g. task_1/tests)")
    parser.add_argument("--seed", type=int, default=None, help="RNG seed (default: 1000 + group)")


def group_dir(out: Path, group: int) -> Path:
    d = out / f"group{group}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_tests(
    task_dir: Path,
    out: Path,
    group: int,
    cases: list[str],
) -> None:
    """Write .in files and generate .ans via solution.py."""
    solution = task_dir / "solution.py"
    if not solution.is_file():
        raise FileNotFoundError(f"Missing solution: {solution}")

    gdir = group_dir(out, group)
    for i, content in enumerate(cases, start=1):
        name = f"test{i:02d}"
        in_path = gdir / f"{name}.in"
        ans_path = gdir / f"{name}.ans"
        text = content if content.endswith("\n") else content + "\n"
        in_path.write_text(text, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(solution)],
            input=text,
            capture_output=True,
            text=True,
            cwd=str(task_dir),
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"solution.py failed on {name} (group {group}):\n"
                f"stderr: {result.stderr}\nstdout: {result.stdout}"
            )
        ans_path.write_text(result.stdout, encoding="utf-8")


def default_seed(group: int, seed: int | None) -> int:
    return (1000 + group) if seed is None else seed
