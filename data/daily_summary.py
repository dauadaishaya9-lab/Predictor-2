import json
from pathlib import Path
from datetime import datetime

DELTA_DIR = Path("data2/deltas")
SUMMARY_DIR = Path("data2/summaries")

# --- FORCE directory creation ---
SUMMARY_DIR.mkdir(parents=True, exist_ok=True)


def daily_summary():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    delta_files = sorted(DELTA_DIR.glob(f"{today}*.json"))

    if not delta_files:
        print("No deltas for today.")
        return

    rises = []
    falls = []

    for f in delta_files:
        with open(f, "r") as fh:
            changes = json.load(fh)

        for c in changes:
            if c["direction"] == "UP":
                rises.append(c["player_id"])
            else:
                falls.append(c["player_id"])

    summary = {
        "date": today,
        "rises": sorted(set(rises)),
        "falls": sorted(set(falls)),
    }

    out_file = SUMMARY_DIR / f"{today}.json"

    with open(out_file, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Daily summary saved → {out_file}")


if __name__ == "__main__":
    daily_summary()
