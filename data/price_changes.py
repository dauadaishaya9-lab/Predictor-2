import json
from pathlib import Path
from datetime import datetime

SNAPSHOT_DIR = Path("data2/snapshots")
DELTA_DIR = Path("data2/deltas")

# --- FORCE directory creation ---
DELTA_DIR.mkdir(parents=True, exist_ok=True)


def load_snapshot(path: Path):
    with open(path, "r") as f:
        return json.load(f)


def detect_price_changes():
    snapshots = sorted(SNAPSHOT_DIR.glob("*.json"))

    if len(snapshots) < 2:
        print("Not enough snapshots.")
        return

    prev = load_snapshot(snapshots[-2])
    curr = load_snapshot(snapshots[-1])

    prev_prices = {p["player_id"]: p["price"] for p in prev["players"]}

    deltas = []

    for p in curr["players"]:
        pid = p["player_id"]
        if pid not in prev_prices:
            continue

        old = prev_prices[pid]
        new = p["price"]

        if old != new:
            deltas.append({
                "player_id": pid,
                "old_price": old,
                "new_price": new,
                "direction": "UP" if new > old else "DOWN",
            })

    if not deltas:
        print("No price changes.")
        return

    ts = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
    out_file = DELTA_DIR / f"{ts}.json"

    with open(out_file, "w") as f:
        json.dump(deltas, f, indent=2)

    print(f"Deltas saved → {out_file}")


if __name__ == "__main__":
    detect_price_changes()
