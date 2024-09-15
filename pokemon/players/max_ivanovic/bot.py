# Don't change these import settings
import sys
sys.path.append('../players')
from players.gen6player import Gen6Player

class MyPokeBot(Gen6Player):
    
    # Define bot logic here in choose_move
    # Check poke-env documentation for help 
    # Focus is on Battle, Pokemon, Player and Move classes
    # For now, default logic is to choose the move with the greatest base power..

    # Always return a value with [return self.create_order(move)]
    def choose_move(self, battle):
        # Get the current active Pokémon and opponent’s status
        active_pokemon = battle.active_pokemon
        opponent = battle.opponent_active
        opponent_last_move = opponent.last_move if opponent else None

        # Sableye Strategy
        if active_pokemon.name == "Sableye":
            if active_pokemon.current_hp <= 0.65 * active_pokemon.max_hp:
                if battle.can_use_move('Recover'):
                    return self.create_order('Recover')

            if opponent.status != 'burn':
                if battle.can_use_move('Will-O-Wisp'):
                    return self.create_order('Will-O-Wisp')

            if opponent.status != 'poison':
                if battle.can_use_move('Toxic'):
                    return self.create_order('Toxic')

            if battle.can_use_move('Foul Play'):
                return self.create_order('Foul Play')

        # Whimsicott Strategy
        if active_pokemon.name == "Whimsicott":
            if active_pokemon.current_hp > 0.60 * active_pokemon.max_hp:
                if battle.can_use_move('Leech Seed'):
                    return self.create_order('Leech Seed')
            else:
                if battle.can_use_move('Protect'):
                    return self.create_order('Protect')
                if battle.can_use_move('Giga Drain'):
                    return self.create_order('Giga Drain')
                if battle.can_use_move('Moonblast'):
                    return self.create_order('Moonblast')

        # Dugtrio Strategy
        if active_pokemon.name == "Dugtrio":
            if opponent.current_hp <= 0.20 * opponent.max_hp:
                if battle.can_use_move('Sucker Punch'):
                    return self.create_order('Sucker Punch')

            if active_pokemon.current_hp > 0.90 * active_pokemon.max_hp:
                if battle.can_use_move('Earthquake'):
                    return self.create_order('Earthquake')

            if battle.can_use_move('Reversal'):
                return self.create_order('Reversal')

            if battle.can_use_move('Endure'):
                return self.create_order('Endure')

        # Togekiss Strategy
        if active_pokemon.name == "Togekiss":
            if active_pokemon.current_hp <= 0.60 * active_pokemon.max_hp:
                if battle.can_use_move('Roost'):
                    return self.create_order('Roost')

            if opponent.status != 'paralysis':
                if battle.can_use_move('Thunder Wave'):
                    return self.create_order('Thunder Wave')

            if battle.can_use_move('Air Slash'):
                return self.create_order('Air Slash')

            if battle.can_use_move('Flamethrower'):
                return self.create_order('Flamethrower')

        # Shedinja Strategy
        if active_pokemon.name == "Shedinja":
            if opponent.current_hp <= 0.20 * opponent.max_hp:
                if battle.can_use_move('Shadow Sneak'):
                    return self.create_order('Shadow Sneak')

            if opponent_last_move not in ['Fire', 'Flying', 'Rock', 'Ghost', 'Dark']:
                if battle.can_use_move('Swords Dance'):
                    return self.create_order('Swords Dance')

            if battle.can_use_move('Protect'):
                return self.create_order('Protect')

            if battle.can_use_move('X-Scissor'):
                return self.create_order('X-Scissor')

        # Shuckle Strategy
        if active_pokemon.name == "Shuckle":
            if active_pokemon.current_hp <= 0.30 * active_pokemon.max_hp:
                if battle.can_use_move('Protect'):
                    return self.create_order('Protect')

            if opponent.status != 'poison':
                if battle.can_use_move('Toxic'):
                    return self.create_order('Toxic')

            if battle.can_use_move('Power Split'):
                return self.create_order('Power Split')

            if battle.can_use_move('Sand Tomb'):
                return self.create_order('Sand Tomb')

        # Default Move Selection
        if battle.available_moves:
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            return self.create_order(best_move)
        else:
            return self.choose_random_move(battle)