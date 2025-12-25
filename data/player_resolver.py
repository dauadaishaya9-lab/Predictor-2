import requests
from typing import Dict, List

FPL_BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"


def normalize(text: str) -> str:
    """Normalize user input or names for matching"""
    return " ".join(text.lower().strip().split())


def fetch_players() -> List[dict]:
    response = requests.get(FPL_BOOTSTRAP_URL, timeout=30)
    response.raise_for_status()
    data = response.json()

    players = []
    for p in data["elements"]:
        players.append({
            "player_id": p["id"],          # backend only
            "web_name": p["web_name"],     # frontend display
            "first_name": p["first_name"],
            "second_name": p["second_name"],
            "price": p["now_cost"],
            "status": p["status"],
        })

    return players


def build_player_index(players: List[dict]) -> Dict[str, int]:
    """
    Build a flexible lookup index:
    - web name
    - first name
    - second name
    - full name (both orders)
    """
    index = {}

    for p in players:
        pid = p["player_id"]

        names = set([
            p["web_name"],
            p["first_name"],
            p["second_name"],
            f"{p['first_name']} {p['second_name']}",
            f"{p['second_name']} {p['first_name']}",
        ])

        for name in names:
            index[normalize(name)] = pid

    return index


def resolve_player(user_input: str, index: Dict[str, int]) -> List[int]:
    """
    Resolve user input to player_id(s)
    Returns:
      - [] if no match
      - [id] if exact/unique match
      - [id1, id2, ...] if ambiguous
    """
    query = normalize(user_input)

    # Exact match
    if query in index:
        return [index[query]]

    # Partial match fallback
    matches = [
        pid for name, pid in index.items()
        if query in name
    ]

    # Remove duplicates while preserving order
    return list(dict.fromkeys(matches))


def build_id_to_name(players: List[dict]) -> Dict[int, str]:
    """Backend → Frontend translation"""
    return {p["player_id"]: p["web_name"] for p in players}


# --- Manual test (GitHub Actions friendly) ---
if __name__ == "__main__":
    players = fetch_players()
    index = build_player_index(players)
    id_to_name = build_id_to_name(players)

    tests = [
        "saka",
        "SAKA",
        "bukayo",
        "bukayo saka",
        "saka bukayo",
        "haaland",
        "mohamed",
    ]

    for t in tests:
        ids = resolve_player(t, index)
        if not ids:
            print(f"{t} -> NOT FOUND")
        elif len(ids) == 1:
            print(f"{t} -> {id_to_name[ids[0]]}")
        else:
            names = [id_to_name[i] for i in ids]
            print(f"{t} -> AMBIGUOUS: {names}")
