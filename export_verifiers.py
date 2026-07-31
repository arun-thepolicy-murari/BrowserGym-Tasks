#!/usr/bin/env python3
"""Extract a standalone verifier module for each task, from the gym's real source.

``server/verifiers.py`` holds all 285 task suites in one 14k-line file. The wave-1
package only carried a snippet of each suite, which does not run on its own because
it references shared helpers defined elsewhere in that file.

This walks the AST from a task's ``_suite_mNN`` and pulls in exactly the module-level
definitions it actually uses (transitively), so each task gets its own readable,
importable verifier containing nothing from any other task:

    task_env/<slug>/verifier_standalone.py

Run with the gym's Python:  _ref/venv/bin/python export_verifiers.py
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GYM = ROOT / "browser-gym-seed-to-cua-gym"
SRC = GYM / "server" / "verifiers.py"
OUT = ROOT / "task_env"

HEADER = '''"""Standalone verifier for {task_id}.

Extracted from server/verifiers.py by export_verifiers.py — this file contains the
task's own suite plus only the shared helpers it references, and nothing belonging to
any other task. Scored via POST /_harness/verify in the gym.
"""
'''


def source_of(node: ast.stmt, lines: list[str]) -> str:
    """Source for a node, including any decorators (get_source_segment drops them)."""
    start = node.lineno
    for dec in getattr(node, "decorator_list", []):
        start = min(start, dec.lineno)
    # step back over the decorator's own '@' line when it spans multiple lines
    while start > 1 and lines[start - 2].lstrip().startswith("@"):
        start -= 1
    return "\n".join(lines[start - 1: node.end_lineno])


def module_index(tree: ast.Module) -> tuple[dict[str, ast.stmt], list[ast.stmt]]:
    """Map every module-level name to its defining node; keep imports separately."""
    defs: dict[str, ast.stmt] = {}
    imports: list[ast.stmt] = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(node)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defs[node.name] = node
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    defs[target.id] = node
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            defs[node.target.id] = node
        elif isinstance(node, ast.If):
            imports.append(node)  # the TYPE_CHECKING block
    return defs, imports


def names_used(node: ast.AST) -> set[str]:
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)} | {
        n.attr for n in ast.walk(node) if isinstance(n, ast.Attribute)
    }


def collect(root_name: str, defs: dict[str, ast.stmt]) -> list[str]:
    """Transitively gather the module-level names the suite depends on."""
    seen: set[str] = set()
    order: list[str] = []

    def visit(name: str) -> None:
        if name in seen or name not in defs:
            return
        seen.add(name)
        for dep in sorted(names_used(defs[name])):
            if dep != name:
                visit(dep)
        order.append(name)

    visit(root_name)
    return order


def main() -> int:
    data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    source = SRC.read_text(encoding="utf-8")
    lines = source.splitlines()
    tree = ast.parse(source)
    defs, imports = module_index(tree)

    import_src = "\n".join(source_of(n, lines) for n in imports)

    written = 0
    for task in data["tasks"]:
        mnum = task["mnum"].lower()
        suite_name = f"_suite_{mnum}"
        if suite_name not in defs:
            print(f"  !! {task['mnum']}: {suite_name} not found in verifiers.py")
            continue

        names = collect(suite_name, defs)
        body = "\n\n\n".join(source_of(defs[n], lines).rstrip() for n in names)

        shim = (
            "\n\n\ndef build_suite(task_id: str = {tid!r}) -> TaskSuite:\n"
            '    """This task only — the gym dispatches all 285 suites by id."""\n'
            "    return {suite}()\n"
        ).format(tid=task["task_id"], suite=suite_name)

        out_dir = OUT / task["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        text = HEADER.format(task_id=task["task_id"]) + "\n" + import_src + "\n\n\n" + body + shim
        (out_dir / "verifier_standalone.py").write_text(text, encoding="utf-8")

        try:
            compile(text, "verifier_standalone.py", "exec")
        except SyntaxError as e:
            print(f"  !! {task['mnum']}: generated file does not compile: {e}")
            continue

        helpers = [n for n in names if n != suite_name]
        print(f"  {task['mnum']:<5} {len(text.splitlines()):>4} lines, {len(helpers)} shared helper(s)")
        written += 1

    print(f"\nwrote {written} standalone verifiers under {OUT}")
    return 0 if written == len(data["tasks"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
