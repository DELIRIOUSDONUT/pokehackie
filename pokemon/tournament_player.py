from tournament_utils import *

class TournamentPlayer:
    num_players = 0

    def __init__(self, name: str, bot_path: str, team_path: str):
        self.id = TournamentPlayer.num_players
        self.name = name
        self.bot = get_poke_env_player_from_path(bot_path, team_path)

        print(f"Instantiated player {self.id} - {self.name}, format: {self.bot.format}")

        TournamentPlayer.num_players += 1

    def __str__(self):
        return f"{self.name}"
    
    def __repr__(self):
        return self.__str__()