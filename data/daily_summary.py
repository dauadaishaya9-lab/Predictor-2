import json
from pathlib import Path
from datetime import datetime

SNAPSHOT_DIR = Path("snapshots")


def load_snapshot(path: Path) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def daily_summary():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    snapshots = sorted(SNAPSHOT_DIR.glob(f"{today}*.json"))

    if len(snapshots) < 2:
        print("Not enough snapshots for daily summary.")
        return

    first = load_snapshot(snapshots[0])
    last = load_snapshot(snapshots[-1])

    first_prices = {p["player_id"]: p["price"] for p in first["players"]}

    rises, falls = [], []

    for p in last["players"]:
        pid = p["player_id"]
        if pid not in first_prices:
            continue

        diff = p["price"] - first_prices[pid]
        if diff > 0:
            rises.append(pid)
        elif diff < 0:
            falls.append(pid)

    print("DAILY SUMMARY")
    print("-------------")
    print("Risers IDs:", rises)
    print("Fallers IDs:", falls)


if __name__ == "__main__":
    daily_summary()
