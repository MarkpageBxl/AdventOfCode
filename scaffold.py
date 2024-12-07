#!/usr/bin/env python

import argparse
import os
import shutil
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

CHALLENGE_URL = "https://adventofcode.com/{year}/day/{day}"

env = Environment(loader=FileSystemLoader("templates"), keep_trailing_newline=True)
header_template = env.get_template("header.j2")
prog_template = env.get_template("prog.py.j2")

parser = argparse.ArgumentParser()
parser.add_argument("year", type=int)
parser.add_argument("day", type=int)
parser.add_argument("--force", "-f", action="store_true")
parser.add_argument("--header", "-H", action="store_true")
args = parser.parse_args()

if args.header:
    for part in (1, 2):
        context = {
            "year": args.year,
            "day": args.day,
            "part": part,
            "url": CHALLENGE_URL.format(year=args.year, day=args.day),
            "fragment": "#part2" if part == 2 else "",
        }
        header = header_template.render(context)
        print(header)
        print()
    sys.exit(0)

padded_day = f"{args.day:02d}"
target_dir: Path = Path(str(args.year)) / padded_day

# Create directory
if os.path.isdir(target_dir):
    if args.force:
        print("Removing existing directory.")
        shutil.rmtree(target_dir)
    else:
        print("Directory already exists, aborting.")
        sys.exit(1)

# Generate scaffold
os.makedirs(target_dir)
input_path = target_dir / "input"
input_path.touch()
for part in (1, 2):
    demo_input = f"demo{part}"
    (target_dir / demo_input).touch()
    context = {
        "year": args.year,
        "day": args.day,
        "part": part,
        "demo_input": demo_input,
        "url": CHALLENGE_URL.format(year=args.year, day=args.day),
        "fragment": "#part2" if part == 2 else "",
    }
    prog_path = target_dir / f"part{part}.py"
    with open(prog_path, "w") as fp:
        fp.write(prog_template.render(context))
    os.chmod(prog_path, 0o755)

print("Scaffold successfully generated in:", target_dir)
