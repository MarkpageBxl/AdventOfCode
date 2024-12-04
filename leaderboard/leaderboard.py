#!/usr/bin/env python

import argparse
import csv
import json
from datetime import datetime, timedelta

import pytz

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()

with open(args.file) as fp:
    data = json.load(fp)

start = datetime(2024, 12, 1, tzinfo=pytz.timezone("EST"))
end = datetime(2024, 12, 25, tzinfo=pytz.timezone("EST"))
dt = start
days = []
while dt <= datetime.now(tz=pytz.timezone("Europe/Brussels")) and dt <= end:
    days.append(dt.day)
    dt += timedelta(days=1)

with open("leaderboard.csv", "w", newline="") as fp:
    writer = csv.DictWriter(fp, fieldnames=["id", "name", "day", "part", "ts"])
    writer.writeheader()

    for id, member in data["members"].items():
        record = {"id": id, "name": member["name"]}
        for day in days:
            day = str(day)
            record["day"] = day
            if day in member["completion_day_level"]:
                dayta = member["completion_day_level"][str(day)]
                for part in ("1", "2"):
                    record["part"] = part
                    if part in dayta:
                        record["ts"] = pytz.timezone("Europe/Brussels").localize(
                            datetime.fromtimestamp(dayta[part]["get_star_ts"])
                        )
                    else:
                        record["ts"] = None
                    writer.writerow(record)
            else:
                for part in ("1", "2"):
                    record["part"] = part
                    record["ts"] = None
                    writer.writerow(record)
