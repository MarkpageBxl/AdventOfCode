#!/usr/bin/env python

import argparse
import csv
import json
from datetime import datetime

import pytz

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()

with open(args.file) as fp:
    data = json.load(fp)

with open("leaderboard.csv", "w", newline="") as fp:
    writer = csv.DictWriter(fp, fieldnames=["id", "name", "day", "part", "ts"])
    writer.writeheader()

    for id, member in data["members"].items():
        record = {"id": id, "name": member["name"]}
        for day, dayta in sorted(
            member["completion_day_level"].items(), key=lambda x: int(x[0])
        ):
            record["day"] = day
            for part in ("1", "2"):
                record["part"] = part
                if part in dayta:
                    record["ts"] = pytz.timezone("Europe/Brussels").localize(
                        datetime.fromtimestamp(dayta[part]["get_star_ts"])
                    )
                else:
                    record["ts"] = None
                writer.writerow(record)
