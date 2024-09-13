# Don't change these import settings
import sys
sys.path.append('../players')
from players.gen6player import Gen6Player

class MyPokeBot(Gen6Player):
    
    # Define bot logic here in choose move
    # Check poke-env documentation for help 
    # Focus is on Battle, Pokemon, Player and Move classes
    # For now, default logic is to choose the move with the greatest base power..

    # Always return a value with [return self.create_order(move)]
    def choose_move(self, battle):
        if battle.available_moves:
            best_move = max(battle.available_moves, key=lambda move: move.base_power)

            if battle.can_mega_evolve:
                return self.create_order(best_move, mega=True)

            return self.create_order(best_move)
        else:
            return self.choose_random_move(battle)