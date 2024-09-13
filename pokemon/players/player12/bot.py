from players.gen3player import Gen3Player
class MyPlayer(Gen3Player):
    def choose_move(self, battle):
        return self.choose_random_move(battle)