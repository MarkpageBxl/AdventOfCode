#!/usr/bin/env python

import csv
import json
import os
from datetime import datetime, timedelta

import pytz
import requests

LEADERBOARD_URL = "https://adventofcode.com/2024/leaderboard/private/view/4311749.json"
LEADERBOARD_FILE = "leaderboard.json"
LEADERBOARD_OUTPUT = "leaderboard.csv"


def update_leaderboard():
    with open("session_cookie") as fp:
        cookies = {"session": fp.read().strip()}

    resp = requests.get(LEADERBOARD_URL, cookies=cookies)
    resp.raise_for_status()
    data = resp.json()

    with open("leaderboard.json", "w") as fp:
        json.dump(data, fp, indent=2)


grace_period = datetime.now() - timedelta(minutes=15)
grace_period_ts = grace_period.timestamp()

if (
    os.path.exists(LEADERBOARD_FILE)
    and os.stat(LEADERBOARD_FILE).st_mtime < grace_period_ts
):
    print("Leaderboard file expired. Fetching from API.")
    try:
        update_leaderboard()
        print("Leaderboard successfully updated.")
    except:
        print("An error occurred while updating the leaderboard. Aborting.")
        raise
else:
    print("Leaderboard file still fresh. Not updating.")

with open(LEADERBOARD_FILE) as fp:
    data = json.load(fp)

start = datetime(2024, 12, 1, tzinfo=pytz.timezone("EST"))
end = datetime(2024, 12, 25, tzinfo=pytz.timezone("EST"))
dt = start
days = []
while dt <= datetime.now(tz=pytz.timezone("Europe/Brussels")) and dt <= end:
    days.append(dt.day)
    dt += timedelta(days=1)

with open(LEADERBOARD_OUTPUT, "w", newline="") as fp:
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

print(f"Data successfully written to {LEADERBOARD_OUTPUT}. Here it comes!")
print()
with open(LEADERBOARD_OUTPUT) as fp:
    print(fp.read(), end="")
