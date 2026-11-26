"""Write the competition entry to the output directory.

Reads entry.txt next to this script and writes it verbatim to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output), then verifies the
copy matches by size and SHA-256. Standard library only.
"""

import hashlib
import os
import sys
from pathlib import Path


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.txt"
    data = source.read_bytes()
    text = data.decode("utf-8")
    if not text.strip():
        print("entry.txt is empty or whitespace only", file=sys.stderr)
        return 1
    if not 1 <= len(text) <= 200:
        print(f"entry is {len(text)} chars, gate is 1-200", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_bytes(data)
    written = target.read_bytes()
    if len(written) != len(data) or sha256_hex(written) != sha256_hex(data):
        print("verification failed: output differs from entry.txt",
              file=sys.stderr)
        return 1
    print(f"wrote {target} ({len(written)} bytes, "
          f"sha256 {sha256_hex(written)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
