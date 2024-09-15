from tournament_utils import *
from tournament_player import TournamentPlayer
from pathlib import Path
import time
import asyncio
from collections import defaultdict

NUM_PLAYERS_AFTER_GROUPS = 1

class Tournament:
    def __init__(self):
        self.players = []
        self.tournament_players = []

    def add_player(self, player: TournamentPlayer):
        self.players.append(player)

    async def play(self, player_one: TournamentPlayer, player_two: TournamentPlayer) -> TournamentPlayer:
        if(player_one == None and player_two == None):
            return None
        if(player_one == None and player_two != None):
            return player_two
        if(player_one != None and player_two == None):
            return player_one
        print(f"\t\tMatch between {player_one} and {player_two} started")
        print(player_one.bot.format)
        print(player_two.bot.format)

        p1 = player_one.bot
        p2 = player_two.bot

        await p1.battle_against(p2, n_battles=1)

        # check most recent battle winner
        for tag, battle in p1.battles.items():
            winner = player_one
            if battle.won:
                winner = player_two

            # we have to reset the battle counts os we dont get confused
            p1.reset_battles()
            p2.reset_battles()

        print(f"\t\t{winner} won")
        return winner

    async def group_stage(self):
        print("Starting group stage...")
        groups = split_players_into_n_groups(self.players, NUM_PLAYERS_AFTER_GROUPS)
        for i, group in enumerate(groups):
            print(f"Group {i} - {group}")

            match_scores = defaultdict(set)

            rounds = create_schedule(group)
            for i, round in enumerate(rounds):
                print(f"\tRound {i + 1}")
                print(f"\t\t{round}")

                for player_one, player_two in round.items():
                    if player_one is None or player_two is None:
                        continue

                    winner = await asyncio.gather(self.play(player_one, player_two))
                    if player_one == winner:
                        match_scores[player_one].add(player_two)
                    else:
                        match_scores[player_two].add(player_one)

            # find winner of group
            group_winner = None
            max_size = -1

            # this wouldn't work for three way ties
            for player, won_against_set in match_scores.items():
                if len(won_against_set) == max_size and group_winner in won_against_set:
                    group_winner = player
                    max_size = len(won_against_set)
                    
                if len(won_against_set) > max_size:
                    group_winner = player
                    max_size = len(won_against_set)
            
            self.tournament_players.append(group_winner)

    async def finals(self, players, round = 0):
        if len(players) == 1:
            return players[0]
    
        winners = []

        print(f"Round {round + 1}")
        
        # Simulate matches for each pair of players
        for i in range(0, len(players), 2):
            player1 = players[i]
            player2 = players[i + 1]
            winner = await self.play(player1, player2)
            winners.append(winner)
        
        # Recursively call tournament for the winners
        return await self.finals(winners, round + 1)

async def main():
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    # define tournament class
    tournament = Tournament()

    # Define the base folder
    players_folder = Path('pokemon\players')

    for player_folder in players_folder.iterdir():
        if player_folder.is_dir() and "__pycache__" not in player_folder.__str__():
            # Extract the player folder name
            player_name = player_folder.name
            print(player_folder)
            
            # Define paths for bot.py and team.txt
            bot_path = player_folder / 'bot.py'
            team_path = player_folder / 'team.txt'

            player = TournamentPlayer(player_name, bot_path, team_path)

            tournament.add_player(player)

    await tournament.group_stage()

    print("Finished group stage. Here are the finalists:")
    for finalist in tournament.tournament_players:
        print(finalist)

    print("Starting the finals")
    winner = await tournament.finals(tournament.tournament_players)
    print(f"The winner is {winner}")


if __name__ == "__main__":
    asyncio.run(main())