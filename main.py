#!/usr/bin/env python3
"""Real-Life Patch Notes entry for make.fun.

Writes a single one-line patch note to /output/entry.txt.
Standard library only, deterministic, no network, no file reads.
"""

import os
import sys
import tempfile
from pathlib import Path

ENTRY = (
    "v1.8.3: fixed a bug where the stomach growled at maximum volume "
    "during silent meetings, then denied being hungry five seconds later."
)


def resolve_output_dir() -> Path:
    """Fallback chain: MAKEFUN_OUTPUT_DIR -> /output -> output/ -> tmp."""
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(Path(env_dir))
    candidates.append(Path("/output"))
    candidates.append(Path(__file__).resolve().parent / "output")
    candidates.append(Path(tempfile.gettempdir()))
    for candidate in candidates:
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            probe = candidate / ".makefun-write-probe"
            probe.write_text("", encoding="utf-8")
            probe.unlink()
            return candidate
        except OSError:
            continue
    return Path(tempfile.gettempdir())


def main() -> int:
    if not ENTRY or not ENTRY.strip():
        print("error: entry is empty or whitespace-only", file=sys.stderr)
        return 1
    if len(ENTRY) > 160:
        print(
            f"error: entry is {len(ENTRY)} characters, exceeds 160",
            file=sys.stderr,
        )
        return 1
    out_dir = resolve_output_dir()
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "entry.txt").write_text(ENTRY, encoding="utf-8")
    except OSError:
        try:
            fallback = Path(tempfile.gettempdir())
            fallback.mkdir(parents=True, exist_ok=True)
            (fallback / "entry.txt").write_text(ENTRY, encoding="utf-8")
        except OSError:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
