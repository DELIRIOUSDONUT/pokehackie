import asyncio

from poke_env.player import RandomPlayer
from poke_env import AccountConfiguration, ShowdownServerConfiguration

import importlib
module = importlib.import_module("players.POKE-BOT.bot")


# Runs a bot player on the actual pokemon showdown server
# Due to ISP spam detection issues, the bot can only be tested by challenging it directly
async def main():
    # Initialize player
    myTeamFile = open("prod-testing/players/POKE-BOT/team.txt")
    myTeam = myTeamFile.read()
    myTeamFile.close()

    player = module.MyPokeBot(
        account_configuration=AccountConfiguration("insert-bot-name", "insert-bot-password"),
        server_configuration=ShowdownServerConfiguration,
        team=myTeam
    )

    # Sending challenges to 'your_username'
    #await player.send_challenges("hmtesting", n_challenges=1)

    # Accepting one challenge from any user
    await player.accept_challenges(None, 1)
    print("Battle over!")

    # Accepting three challenges from 'your_username'
    #await player.accept_challenges('your_username', 3)

    # Playing 5 games on the ladder
    #await player.ladder(5)

    # Print the rating of the player and its opponent after each battle
    #for battle in player.battles.values():
        #print(battle.rating, battle.opponent_rating)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())