import csv
from datetime import datetime

import matplotlib.pyplot as plt


dates = []
players = []

with open("data/steam_players.csv", "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        dates.append(datetime.strptime(row["date"], "%Y-%m-%d"))
        players.append(int(row["value"]))


plt.figure(figsize=(14, 6))

plt.plot(
    dates,
    players,
    linewidth=1.5
)

plt.title("PUBG Daily Player Trend")
plt.xlabel("Date")
plt.ylabel("Players")

plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    "reports/player_trend.png",
    dpi=150,
    bbox_inches="tight"
)

plt.show()

from collections import defaultdict

monthly_sum = defaultdict(int)
monthly_count = defaultdict(int)

for date, player in zip(dates, players):
    key = date.strftime("%Y-%m")
    monthly_sum[key] += player
    monthly_count[key] += 1

months = sorted(monthly_sum.keys())
monthly_avg = [
    monthly_sum[month] / monthly_count[month]
    for month in months
]

plt.figure(figsize=(12, 6))

plt.bar(
    months,
    monthly_avg
)

plt.title("PUBG Monthly Average Players")
plt.xlabel("Month")
plt.ylabel("Average Players")

plt.xticks(rotation=45)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    "reports/monthly_average.png",
    dpi=150,
    bbox_inches="tight"
)

plt.show()

# 세 번째 그래프: 최근 30일 + 7일 이동평균

recent_dates = dates[-30:]
recent_players = players[-30:]

moving_average = []

for i in range(len(recent_players)):
    start = max(0, i - 6)
    window = recent_players[start:i + 1]
    moving_average.append(sum(window) / len(window))

plt.figure(figsize=(12, 6))

plt.plot(
    recent_dates,
    recent_players,
    label="Daily Players",
    linewidth=1.5
)

plt.plot(
    recent_dates,
    moving_average,
    label="7-Day Moving Average",
    linewidth=2.5
)

plt.title("PUBG Recent 30 Days Player Trend")
plt.xlabel("Date")
plt.ylabel("Players")

plt.legend()
plt.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "reports/recent_30d_moving_average.png",
    dpi=150,
    bbox_inches="tight"
)

plt.show()