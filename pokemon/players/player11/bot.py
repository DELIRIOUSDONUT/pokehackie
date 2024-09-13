import sys
sys.path.append('../players')
from players.gen6player import Gen6Player

class MyPlayer(Gen6Player):
    def choose_move(self, battle):
        return self.choose_random_move(battle)