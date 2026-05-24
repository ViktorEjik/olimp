"""Shared utilities for olympiad test generators."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

TESTS_PER_GROUP = 12


def add_cli(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--group", type=int, choices=(1, 2, 3, 4), required=True)
    parser.add_argument("--out", type=Path, default=Path("tests"))
    parser.add_argument("--seed", type=int, default=None)


def group_dir(out: Path, group: int) -> Path:
    d = out / f"group{group}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def run_solution(solution: Path, inp: str) -> str:
    proc = subprocess.run(
        [sys.executable, str(solution)],
        input=inp,
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout


def write_tests(
    cases: list[str],
    *,
    group: int,
    out: Path,
    solution: Path,
) -> None:
    dest = group_dir(out, group)
    for i, inp in enumerate(cases, start=1):
        name = f"test{i:02d}"
        in_path = dest / f"{name}.in"
        ans_path = dest / f"{name}.ans"
        text = inp if inp.endswith("\n") else inp + "\n"
        in_path.write_text(text, encoding="utf-8")
        ans_path.write_text(run_solution(solution, text), encoding="utf-8")

