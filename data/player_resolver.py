from data.fetcher import fetch_players


def build_player_index():
    players = fetch_players()

    index = {}
    for p in players:
        index[p["player_id"]] = p["web_name"]

    return index
