import importlib.util
import sys
from math import ceil
from poke_env import Player
from poke_env.ps_client.server_configuration import (
    LocalhostServerConfiguration,
    ServerConfiguration,
)

def get_poke_env_player_from_path(path: str, team_path: str):
    # Name the module (you can give it any name)
    module_name = path.stem  # This will use the file name (without extension) as the module name

    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    teamfile = open(team_path)
    team = teamfile.read()
    teamfile.close()
        
    
    # Find the class dynamically
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, type) and issubclass(attr, object) and issubclass(attr, Player):
            return attr(team=team, battle_format="gen6ou", # Any format for which the team is legal works here.
                        server_configuration=LocalhostServerConfiguration,
                        log_level=10)
        
    raise AttributeError("No suitable class found in the module.")

def split_players_into_n_groups(players: list, n: int):
    size = len(players) // n
    groups = []

    for i in range(0, size * n, size):
        groups.append(players[i : i + size])

    for i in range(size * n, len(players)):
        groups[i % (size * n)].append(players[i])

    return groups
  

def create_schedule(teams_list: list):
    if(len(teams_list) % 2) != 0:
        teams_list.append(None)

    x = teams_list[0:int(len(teams_list)/2)]
    y = teams_list[int(len(teams_list)/2):len(teams_list)]

    rounds = []

    for i in range(len(teams_list)-1):
        matches = {}
        if i != 0: 
            x.insert(1,y.pop(0))
            y.append(x.pop())
        rounds.append(matches)
        for j in range(len(x)):
                matches[x[j]] = y[j]

    return rounds