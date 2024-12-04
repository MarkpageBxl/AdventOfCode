#!/usr/bin/env python

import argparse
import json
from datetime import datetime

import pytz

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()

with open(args.file) as fp:
    data = json.load(fp)

for id, member in data["members"].items():
    print(f"#{id}: {member['name']}")
    for day, dayta in sorted(
        member["completion_day_level"].items(), key=lambda x: int(x[0])
    ):
        for part in ("1", "2"):
            if part in dayta:
                print(
                    f"{int(day):02d}.{part}:",
                    pytz.timezone("Europe/Brussels").localize(
                        datetime.fromtimestamp(dayta[part]["get_star_ts"])
                    ),
                )
        print("-" * 5)
    print("=" * 10)
