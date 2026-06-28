#!/usr/bin/env python3
# Copyright (c) 2026 [authors anonymised for double-blind review]
# SPDX-License-Identifier: MIT
"""Build the full-model substrate from a clone of airbus/apollo-11-sysml-v2.

Concatenates every .sysml file in the pinned clone, in sorted path order,
with file-boundary markers, so the probe's "complete published model"
substrate is reproducible byte-for-byte from upstream.

Usage:
  python build_full_substrate.py /path/to/apollo-11-sysml-v2 \
         ../substrate/apollo-model-full-6e9c93f.sysml
"""

import pathlib
import subprocess
import sys

PINNED = "6e9c93fe7d80c5ca3534bb14b10ab374a643ef2d"


def main() -> None:
    clone = pathlib.Path(sys.argv[1])
    out = pathlib.Path(sys.argv[2])
    try:
        sha = subprocess.run(
            ["git", "-C", str(clone), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:
        sha = "unknown (not a git clone)"
    header = (
        "// COMPLETE Apollo 11 SysML v2 model (MPL-2.0, copyright Airbus)\n"
        f"// Source: https://github.com/airbus/apollo-11-sysml-v2 @ {sha}\n"
        f"// Expected pin: {PINNED}\n"
        "// Every .sysml file in the repository, concatenated in sorted path\n"
        "// order with boundary markers. No content selection was applied.\n\n"
    )
    parts = [header]
    files = sorted(clone.rglob("*.sysml"))
    for f in files:
        rel = f.relative_to(clone).as_posix()
        parts.append(f"\n// ======== FILE: {rel} ========\n")
        parts.append(f.read_text(encoding="utf-8", errors="replace"))
    text = "".join(parts)
    out.write_text(text, encoding="utf-8")
    print(f"{len(files)} files, {len(text.splitlines())} lines -> {out}")
    if sha != PINNED:
        print(f"WARNING: clone is at {sha}, not the pinned {PINNED}")


if __name__ == "__main__":
    main()
