import json
from datetime import datetime, timezone
from pathlib import Path

from data.fetcher import fetch_players

# --- FORCE directory creation ---
SNAPSHOT_DIR = Path("data2/snapshots")
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)


def take_snapshot():
    players = fetch_players()

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    out_file = SNAPSHOT_DIR / f"{timestamp}.json"

    snapshot = {
        "timestamp": timestamp,
        "players": [
            {
                "player_id": p["player_id"],
                "price": p["price"],
                "status": p["status"],
            }
            for p in players
        ],
    }

    with open(out_file, "w") as f:
        json.dump(snapshot, f, indent=2)

    print(f"Snapshot saved → {out_file}")


if __name__ == "__main__":
    take_snapshot()
