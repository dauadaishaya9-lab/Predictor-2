import json
from datetime import datetime, timezone
from pathlib import Path

from data.fetcher import fetch_players


SNAPSHOT_DIR = Path("snapshots")
SNAPSHOT_DIR.mkdir(exist_ok=True)


def take_snapshot():
    players = fetch_players()

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    snapshot_file = SNAPSHOT_DIR / f"{timestamp}.json"

    snapshot = {
        "timestamp": timestamp,
        "players": [
            {
                "player_id": p["player_id"],
                "price": p["price"],
                "transfers_in": p["transfers_in"],
                "transfers_out": p["transfers_out"],
                "status": p["status"],
            }
            for p in players
        ],
    }

    with open(snapshot_file, "w") as f:
        json.dump(snapshot, f, indent=2)

    print(f"Snapshot saved: {snapshot_file}")


if __name__ == "__main__":
    take_snapshot()
