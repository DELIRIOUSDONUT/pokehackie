# Don't change these import settings
import sys
sys.path.append('../players')
from players.gen6player import Gen6Player

class MyPokeBot(Gen6Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.azumarill_belly_drum_used = False
        self.garchomp_stealth_rock_used = False
        self.talonflame_tailwind_used = False
        self.cloyster_shell_smash_used = False

    def choose_move(self, battle):
        # Azumarill's Belly Drum
        if battle.active_pokemon.species == "azumarill" and not self.azumarill_belly_drum_used:
            belly_drum = next((move for move in battle.available_moves if move.id == "bellydrum"), None)
            if belly_drum:
                self.azumarill_belly_drum_used = True
                return self.create_order(belly_drum)

        # Garchomp's Stealth Rock
        if battle.active_pokemon.species == "garchomp" and not self.garchomp_stealth_rock_used:
            stealth_rock = next((move for move in battle.available_moves if move.id == "stealthrock"), None)
            if stealth_rock:
                self.garchomp_stealth_rock_used = True
                return self.create_order(stealth_rock)
            
        # Talonflame's Tailwind
        if battle.active_pokemon.species == "talonflame" and not self.talonflame_tailwind_used:
            tailwind = next((move for move in battle.available_moves if move.id == "tailwind"), None)
            if tailwind:
                self.talonflame_tailwind_used = True
                return self.create_order(tailwind)
            
        # Cloyster's Shell Smash
        if battle.active_pokemon.species == "cloyster":
            shell_smash = next((move for move in battle.available_moves if move.id == "shellsmash"), None)
            if shell_smash:
                self.cloyster_shell_smash_used
                return self.create_order(shell_smash)
        
        if battle.available_moves:
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            if battle.can_mega_evolve:
                return self.create_order(best_move, mega=True)
            return self.create_order(best_move)
        else:
            return self.choose_random_move(battle)