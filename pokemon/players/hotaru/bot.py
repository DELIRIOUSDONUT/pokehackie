# Don't change these import settings
import sys
sys.path.append('../players')
from players.gen6player import Gen6Player

class MyPokeBot(Gen6Player):
    def choose_move(self, battle):
        my_pokemon = battle.active_pokemon
        opponent_pokemon = battle.opponent_active_pokemon

        if my_pokemon.species == 'Cloyster':
            if 'shellsmash' in [move.id for move in battle.available_moves]:
                if my_pokemon.current_hp_fraction == 1.0:
                    return self.create_order('shellsmash')
            if 'rapidspin' in [move.id for move in battle.available_moves] and battle.side_conditions:
                return self.create_order('rapidspin')
            if 'iciclespear' in [move.id for move in battle.available_moves]:
                return self.create_order('iciclespear')
            if 'explosion' in [move.id for move in battle.available_moves]:
                return self.create_order('explosion')

        elif my_pokemon.species == 'Aerodactyl':
            if 'stealthrock' not in battle.opponent_side_conditions and 'stealthrock' in [move.id for move in battle.available_moves]:
                return self.create_order('stealthrock')
            if 'taunt' in [move.id for move in battle.available_moves]:
                return self.create_order('taunt')
            attacking_moves = [move for move in battle.available_moves if move.id in ['earthquake', 'doubleedge']]
            if attacking_moves:
                best_move = max(attacking_moves, key=lambda move: move.base_power * move.accuracy)
                return self.create_order(best_move)

        elif my_pokemon.species == 'Scizor':
            if 'swordsdance' in [move.id for move in battle.available_moves]:
                if my_pokemon.current_hp_fraction > 0.5:
                    return self.create_order('swordsdance')
            attacking_moves = [move for move in battle.available_moves if move.category != MoveCategory.STATUS]
            if attacking_moves:
                def move_score(move):
                    if opponent_pokemon:
                        effectiveness = opponent_pokemon.damage_multiplier(move)
                        stab = 1.5 if move.type in my_pokemon.types else 1.0
                        return move.base_power * effectiveness * stab * move.accuracy
                    else:
                        return move.base_power * move.accuracy
                best_move = max(attacking_moves, key=move_score)
                if battle.can_mega_evolve:
                    return self.create_order(best_move, mega=True)
                else:
                    return self.create_order(best_move)

        elif my_pokemon.species == 'Weavile':
            if 'swordsdance' in [move.id for move in battle.available_moves]:
                if my_pokemon.current_hp_fraction == 1.0:
                    return self.create_order('swordsdance')
            attacking_moves = [move for move in battle.available_moves if move.category != MoveCategory.STATUS]
            if attacking_moves:
                def move_score(move):
                    if opponent_pokemon:
                        effectiveness = opponent_pokemon.damage_multiplier(move)
                        stab = 1.5 if move.type in my_pokemon.types else 1.0
                        return move.base_power * effectiveness * stab * move.accuracy
                    else:
                        return move.base_power * move.accuracy
                best_move = max(attacking_moves, key=move_score)
                return self.create_order(best_move)

        elif my_pokemon.species == 'Volcarona':
            if 'quiverdance' in [move.id for move in battle.available_moves]:
                if my_pokemon.current_hp_fraction > 0.5:
                    return self.create_order('quiverdance')
            attacking_moves = [move for move in battle.available_moves if move.category != MoveCategory.STATUS]
            if attacking_moves:
                def move_score(move):
                    if opponent_pokemon:
                        effectiveness = opponent_pokemon.damage_multiplier(move)
                        stab = 1.5 if move.type in my_pokemon.types else 1.0
                        return move.base_power * effectiveness * stab * move.accuracy
                    else:
                        return move.base_power * move.accuracy
                best_move = max(attacking_moves, key=move_score)
                return self.create_order(best_move)

        elif my_pokemon.species == 'Thundurus-Therian':
            if 'nastyplot' in [move.id for move in battle.available_moves]:
                if my_pokemon.current_hp_fraction > 0.5:
                    return self.create_order('nastyplot')
            attacking_moves = [move for move in battle.available_moves if move.category != MoveCategory.STATUS]
            if attacking_moves:
                def move_score(move):
                    if opponent_pokemon:
                        effectiveness = opponent_pokemon.damage_multiplier(move)
                        stab = 1.5 if move.type in my_pokemon.types else 1.0
                        return move.base_power * effectiveness * stab * move.accuracy
                    else:
                        return move.base_power * move.accuracy
                best_move = max(attacking_moves, key=move_score)
                return self.create_order(best_move)

        else:
            setup_moves = {'swordsdance', 'shellsmash', 'quiverdance', 'nastyplot'}
            available_setup_moves = [
                move for move in battle.available_moves if move.id in setup_moves
            ]
            if available_setup_moves and my_pokemon.current_hp_fraction > 0.5:
                return self.create_order(available_setup_moves[0])

            if battle.available_moves:
                def move_score(move):
                    if opponent_pokemon:
                        effectiveness = opponent_pokemon.damage_multiplier(move)
                        stab = 1.5 if move.type in my_pokemon.types else 1.0
                        return move.base_power * effectiveness * stab * move.accuracy
                    else:
                        return move.base_power * move.accuracy
                best_move = max(battle.available_moves, key=move_score)
                return self.create_order(best_move)
            else:
                return self.choose_random_move(battle)
