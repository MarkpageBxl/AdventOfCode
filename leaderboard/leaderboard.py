#!/usr/bin/env python

import csv
import json
import os
import sqlite3
from collections.abc import Sequence
from datetime import datetime, timedelta
from typing import Any

import pytz
import requests

LEADERBOARD_URL = "https://adventofcode.com/2024/leaderboard/private/view/4311749.json"
LEADERBOARD_FILE = "leaderboard.json"
LEADERBOARD_OUTPUT_CSV = "leaderboard.csv"
LEADERBOARD_DB = "leaderboard.sqlite3"


def dict_factory(cursor: sqlite3.Cursor, row: Sequence[Any]):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


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

days = range(1, 26)

with sqlite3.connect(LEADERBOARD_DB) as conn:
    conn.execute(
        """
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """
    )
    conn.execute(
        """
            CREATE TABLE IF NOT EXISTS challenges (
                id INTEGER PRIMARY KEY,
                day INTEGER NOT NULL,
                part INTEGER NOT NULL,
                UNIQUE (day, part)
            )
        """
    )
    conn.execute(
        """
            CREATE TABLE IF NOT EXISTS results (
                member_id INTEGER NOT NULL,
                challenge_id INTEGER NOT NULL,
                ts TEXT,
                star_index INTEGER,
                PRIMARY KEY (member_id, challenge_id),
                FOREIGN KEY (member_id) REFERENCES members (id),
                FOREIGN KEY (challenge_id) REFERENCES challenges (id)
            )
        """
    )
    conn.execute("DROP VIEW IF EXISTS leaderboard_vw")
    conn.execute(
        """
            CREATE VIEW leaderboard_vw AS
            SELECT members.id AS member_id, name, challenges.id AS challenge_id, challenges.day, challenges.part, ts, star_index FROM members
            INNER JOIN challenges
            LEFT OUTER JOIN results ON members.id = results.member_id AND results.challenge_id = challenges.id
            ORDER BY members.id, challenges.day, challenges.part
        """
    )
    conn.execute("DELETE FROM results")
    conn.execute("DELETE FROM challenges")
    conn.execute("DELETE FROM members")
    challenges = {}
    for day in days:
        for part in (1, 2):
            cur = conn.execute(
                "INSERT INTO challenges VALUES (NULL, ?, ?)", (day, part)
            )
            challenges[(day, part)] = cur.lastrowid
    for id, member in data["members"].items():
        member_record = {"id": id, "name": member["name"]}
        conn.execute("INSERT INTO members VALUES (:id, :name)", member_record)
        for day in days:
            result = {"member_id": member["id"]}
            if str(day) in member["completion_day_level"]:
                dayta = member["completion_day_level"][str(day)]
                for part in ("1", "2"):
                    result["challenge_id"] = challenges[(day, int(part))]
                    result["ts"] = None
                    result["star_index"] = None
                    if part in dayta:
                        result["ts"] = pytz.timezone("Europe/Brussels").localize(
                            datetime.fromtimestamp(dayta[part]["get_star_ts"])
                        )
                        result["star_index"] = int(dayta[part]["star_index"])
                        conn.execute(
                            "INSERT INTO results VALUES (:member_id, :challenge_id, :ts, :star_index)",
                            result,
                        )

print("Data successfully loaded into database:", LEADERBOARD_DB)

with open(LEADERBOARD_OUTPUT_CSV, "w", newline="") as fp:
    writer = csv.DictWriter(
        fp,
        fieldnames=[
            "member_id",
            "name",
            "challenge_id",
            "day",
            "part",
            "ts",
            "star_index",
        ],
    )
    writer.writeheader()
    with sqlite3.connect(LEADERBOARD_DB) as conn:
        conn.row_factory = dict_factory
        cur = conn.execute(
            "SELECT member_id, name, challenge_id, day, part, ts, star_index FROM leaderboard_vw WHERE ts IS NOT NULL"
        )
        writer.writerows(cur)

print("Data successfully written to file:", LEADERBOARD_OUTPUT_CSV)
