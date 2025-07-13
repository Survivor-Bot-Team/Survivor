import csv
from datetime import datetime

def log_match(warzone, clan_a, clan_b, player_count, match_type):
    with open("warzone_log.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), warzone, clan_a, clan_b, f"{player_count}v{player_count}", match_type])
