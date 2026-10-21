#!/usr/bin/env python3
"""Roll fair W6 using the operating system's cryptographic randomness."""
import argparse
import json
import re
import secrets
from datetime import datetime, timezone


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roll-id", required=True, help="Unique ID from the announced probe")
    parser.add_argument("--count", type=int, choices=(1, 2), default=2,
                        help="2 for a normal roll; 1 for an agreed luck reroll")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z][a-z0-9-]*", args.roll_id):
        parser.error("roll-id must use lowercase ASCII letters, digits and hyphens")
    dice = [secrets.randbelow(6) + 1 for _ in range(args.count)]
    print(json.dumps({
        "roll_id": args.roll_id,
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "tool",
        "generator": "python.secrets.randbelow / operating-system CSPRNG",
        "sides": 6,
        "dice": dice,
        "sum": sum(dice),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
