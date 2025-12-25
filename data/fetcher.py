import requests

FPL_BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"

def fetch_players():
    response = requests.get(FPL_BOOTSTRAP_URL, timeout=30)
    response.raise_for_status()
    data = response.json()

    players = []

    for p in data["elements"]:
        players.append({
            "player_id": p["id"],
            "name": p["web_name"],
            "price": p["now_cost"],  # still x10 (e.g. 86 = £8.6)
            "transfers_in": p["transfers_in"],
            "transfers_out": p["transfers_out"],
            "transfers_in_event": p["transfers_in_event"],
            "transfers_out_event": p["transfers_out_event"],
            "status": p["status"],
        })

    return players


if __name__ == "__main__":
    players = fetch_players()
    print(players[:5])
