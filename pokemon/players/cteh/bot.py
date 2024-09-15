import sys
sys.path.append('../players')
from players.gen6player import Gen6Player
from poke_env.environment.pokemon_type import PokemonType
from poke_env.environment.weather import Weather
class MyPokeBot(Gen6Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.azumarill_used_belly_drum = False
        self.tyranitar_used_stealth_rock = False
        self.belly_drum_index = 0
        self.excadril_used_swords_dance = False
        self.team_order = ['Tyranitar', 'Excadrill', 'Serperior', 'Azumarill', 'Zapdos', 'Latios']  # Set your desired order here

    def teampreview(self, battle):
        # Example: Always choose a specific Pokémon by name (e.g., 'Pikachu')
        members = list(range(1, len(battle.team) + 1))
        
        return "/team " + "".join([str(c) for c in members])
    
    

    # Define bot logic here in choose_move
    # Now, it will consider enemy type effectiveness as well as base power
    def choose_move(self, battle):
        # if battle.active_pokemon.species == 'Azumarill' and not self.azumarill_used_belly_drum:
        #         belly_drum_move = next((move for move in battle.available_moves if move.id == 'bellydrum'), None)
        #         if belly_drum_move:
        #             self.azumarill_used_belly_drum = True
        #             print("Using Belly Drum")
        #             return self.create_order(belly_drum_move)
        #         else:
        #             print("Belly Drum not found in available moves")
        print("Active Pokemon: ", battle.active_pokemon.species)
        print(f"item is {battle.opponent_active_pokemon.item}")
        print(f"enemy ability is {battle.available_moves}")
        print(f"the field is or {battle.field_start}")
        if battle.active_pokemon.species == 'tyranitar' and battle.active_pokemon.fainted:
                    print(battle.available_moves)
                    print("Switching to Excadrill")
                    excadrill = next((pokemon for pokemon in battle.available_switches if pokemon.species == 'excadrill'), None)
                    latios = next((pokemon for pokemon in battle.available_switches if pokemon.species == 'latios'), None)
                    volcanion = next((pokemon for pokemon in battle.available_switches if pokemon.species == 'volcanion'), None)
                    print(f"enemy is {battle.opponent_active_pokemon.item}")
                    print(battle.opponent_active_pokemon.type_1)
                    print(battle.opponent_active_pokemon.type_2)
                    if battle.opponent_active_pokemon.type_1 == PokemonType.WATER or battle.opponent_active_pokemon.type_2 ==PokemonType.WATER:
                        print("Switching to volc")
                        return self.create_order(volcanion)
                    if excadrill:
                # Check effectiveness between Excadrill and opponent
                        excadrill_effectiveness = battle.opponent_active_pokemon.damage_multiplier(excadrill.type_1)
                        excadrill_effectiveness *= battle.opponent_active_pokemon.damage_multiplier(excadrill.type_2)
                        print("Excadrill effectiveness: ", excadrill_effectiveness)
                        opponent_effectiveness = max(excadrill.damage_multiplier(excadrill.type_1), excadrill.damage_multiplier(excadrill.type_2))
                        
                        print("Opponent effectiveness: ", opponent_effectiveness)
                        # If opponent is effec tive against Excadrill and Excadrill is not effective, switch to Latios
                        if excadrill_effectiveness < 1 and opponent_effectiveness >= 1:
                            print("Switching to Latios")
                            return self.create_order(latios)
                        else:
                            print("Switching to Excadrill")
                            return self.create_order(excadrill)
        if battle.active_pokemon.species == 'excadrill' and battle.active_pokemon.fainted:
                    print("Switching to serperior")
                    serperior = next((pokemon for pokemon in battle.available_switches if pokemon.species == 'serperior'), None)
                    volcanion = next((pokemon for pokemon in battle.available_switches if pokemon.species == 'volcanion'), None)
                    azumarill = next((pokemon for pokemon in battle.available_switches if pokemon.species == 'azumarill'), None)
                    latios = next((pokemon for pokemon in battle.available_switches if pokemon.species == 'latios'), None)
                    #untested method, not sure if next will work properly since we only created one iterator instance
                    if volcanion:
                        if battle.opponent_active_pokemon.type_1 == PokemonType.WATER or battle.opponent_active_pokemon.type_2 ==PokemonType.WATER:
                            print("Switching to volc")
                            return self.create_order(volcanion)
                    
                    if serperior:
                        if battle.opponent_active_pokemon.type_1 == PokemonType.GROUND or battle.opponent_active_pokemon.type_2 ==PokemonType.GROUND or battle.opponent_active_pokemon.type_1 == PokemonType.WATER or battle.opponent_active_pokemon.type_2 ==PokemonType.WATER or battle.opponent_active_pokemon.type_1 == PokemonType.ROCK or battle.opponent_active_pokemon.type_2 ==PokemonType.ROCK:
                            print("Switching to serperior")
                            return self.create_order(serperior)
                    
                    if azumarill:
                        if battle.opponent_active_pokemon.type_1 == PokemonType.FIRE or battle.opponent_active_pokemon.type_2 ==PokemonType.FIRE or battle.opponent_active_pokemon.type_1 == PokemonType.GROUND or battle.opponent_active_pokemon.type_2 ==PokemonType.GROUND or battle.opponent_active_pokemon.type_1 == PokemonType.ROCK or battle.opponent_active_pokemon.type_2 ==PokemonType.ROCK:
                            print("Switching to azumarill")
                            return self.create_order(azumarill)
                    if latios:
                        print("Switching to latios")
                        return self.create_order(latios)    
        if battle.active_pokemon.species == 'serperior' and battle.active_pokemon.fainted:
                    volcanion = next((pokemon for pokemon in battle.available_switches if pokemon.species == 'volcanion'), None)
                    excadrill = next((pokemon for pokemon in battle.available_switches if pokemon.species == 'excadrill'), None)
                    latios = next((pokemon for pokemon in battle.available_switches if pokemon.species == 'latios'), None)
                    if volcanion:
                        if battle.opponent_active_pokemon.type_1 == PokemonType.WATER or battle.opponent_active_pokemon.type_2 ==PokemonType.WATER:
                            print("Switching to volc")
                            return self.create_order(volcanion)
                    print("Switching to azumarill")
                    azumarill = next((pokemon for pokemon in battle.available_switches if pokemon.species == 'azumarill'), None)
                    if azumarill:
                        if battle.opponent_active_pokemon.type_1 == PokemonType.FIRE or battle.opponent_active_pokemon.type_2 ==PokemonType.FIRE or battle.opponent_active_pokemon.type_1 == PokemonType.GROUND or battle.opponent_active_pokemon.type_2 ==PokemonType.GROUND or battle.opponent_active_pokemon.type_1 == PokemonType.ROCK or battle.opponent_active_pokemon.type_2 ==PokemonType.ROCK:
                            return self.create_order(azumarill)
                    if excadrill:
                # Check effectiveness between Excadrill and opponent
                        excadrill_effectiveness = battle.opponent_active_pokemon.damage_multiplier(excadrill.type_1)
                        excadrill_effectiveness *= battle.opponent_active_pokemon.damage_multiplier(excadrill.type_2)
                        print("Excadrill effectiveness: ", excadrill_effectiveness)
                        opponent_effectiveness = max(excadrill.damage_multiplier(excadrill.type_1), excadrill.damage_multiplier(excadrill.type_2))
                        
                        print("Opponent effectiveness: ", opponent_effectiveness)
                        # If opponent is effec tive against Excadrill and Excadrill is not effective, switch to Latios
                        if excadrill_effectiveness < 1 or opponent_effectiveness >= 1:
                            print("Switching to Latios")
                            pass
                        else:
                            print("Switching to Excadrill")
                            return self.create_order(excadrill)
                    if latios:
                        print("Switching to latios")
                        return self.create_order(latios)
                    
                    
        if battle.active_pokemon.species == 'latios' and battle.active_pokemon.fainted:
                    volcanion = next((pokemon for pokemon in battle.available_switches if pokemon.species == 'volcanion'), None)
                    if volcanion:
                        if battle.opponent_active_pokemon.type_1 == PokemonType.WATER or battle.opponent_active_pokemon.type_2 ==PokemonType.WATER:
                            print("Switching to volc")
                            return self.create_order(volcanion)
                    print("Switching to latios")
                    excadrill = next((pokemon for pokemon in battle.available_switches if pokemon.species == 'excadrill'), None)

                    azumarill = next((pokemon for pokemon in battle.available_switches if pokemon.species == 'azumarill'), None)
                    serperior = next((pokemon for pokemon in battle.available_switches if pokemon.species == 'serperior'), None)
                    if azumarill:
                        if battle.opponent_active_pokemon.type_1 == PokemonType.FIRE or battle.opponent_active_pokemon.type_2 ==PokemonType.FIRE or battle.opponent_active_pokemon.type_1 == PokemonType.GROUND or battle.opponent_active_pokemon.type_2 ==PokemonType.GROUND or battle.opponent_active_pokemon.type_1 == PokemonType.ROCK or battle.opponent_active_pokemon.type_2 ==PokemonType.ROCK:
                            print("Switching to azumarill")
                            return self.create_order(azumarill)
                    if serperior:
                        if battle.opponent_active_pokemon.type_1 == PokemonType.GROUND or battle.opponent_active_pokemon.type_2 ==PokemonType.GROUND or battle.opponent_active_pokemon.type_1 == PokemonType.WATER or battle.opponent_active_pokemon.type_2 ==PokemonType.WATER or battle.opponent_active_pokemon.type_1 == PokemonType.ROCK or battle.opponent_active_pokemon.type_2 ==PokemonType.ROCK:
                            print("Switching to serperior")
                            return self.create_order(serperior)
                    if excadrill:
                        if excadrill:
                # Check effectiveness between Excadrill and opponent
                            excadrill_effectiveness = battle.opponent_active_pokemon.damage_multiplier(excadrill.type_1)
                            excadrill_effectiveness *= battle.opponent_active_pokemon.damage_multiplier(excadrill.type_2)
                            print("Excadrill effectiveness: ", excadrill_effectiveness)
                            opponent_effectiveness = max(excadrill.damage_multiplier(excadrill.type_1), excadrill.damage_multiplier(excadrill.type_2))
                            
                            print("Opponent effectiveness: ", opponent_effectiveness)
                            # If opponent is effec tive against Excadrill and Excadrill is not effective, switch to Latios
                            if excadrill_effectiveness < 1 and opponent_effectiveness >= 1:
                                pass
                            else:
                                print("Switching to Excadrill")
                                return self.create_order(excadrill)
                    if volcanion:
                        print("Switching to volc")
                        return self.create_order(volcanion)
                    
        if battle.active_pokemon.species == "volcanion" and battle.active_pokemon.fainted:
                    print("Switching to azumarill")
                    azumarill = next((pokemon for pokemon in battle.available_switches if pokemon.species == 'azumarill'), None)
                    serperior = next((pokemon for pokemon in battle.available_switches if pokemon.species == 'serperior'), None)
                    excadrill = next((pokemon for pokemon in battle.available_switches if pokemon.species == 'excadrill'), None)
                    latios = next((pokemon for pokemon in battle.available_switches if pokemon.species == 'latios'), None)
                    if azumarill:
                        if battle.opponent_active_pokemon.type_1 == PokemonType.FIRE or battle.opponent_active_pokemon.type_2 ==PokemonType.FIRE or battle.opponent_active_pokemon.type_1 == PokemonType.GROUND or battle.opponent_active_pokemon.type_2 ==PokemonType.GROUND or battle.opponent_active_pokemon.type_1 == PokemonType.ROCK or battle.opponent_active_pokemon.type_2 ==PokemonType.ROCK:
                            print("Switching to azumarill")
                            return self.create_order(azumarill)
                    if battle.opponent_active_pokemon.type_1 == PokemonType.GROUND or battle.opponent_active_pokemon.type_2 ==PokemonType.GROUND or battle.opponent_active_pokemon.type_1 == PokemonType.WATER or battle.opponent_active_pokemon.type_2 ==PokemonType.WATER or battle.opponent_active_pokemon.type_1 == PokemonType.ROCK or battle.opponent_active_pokemon.type_2 ==PokemonType.ROCK:
                        print("Switching to serperior")
                        if serperior:
                            return self.create_order(serperior)
                    if excadrill:
                # Check effectiveness between Excadrill and opponent
                        excadrill_effectiveness = battle.opponent_active_pokemon.damage_multiplier(excadrill.type_1)
                        excadrill_effectiveness *= battle.opponent_active_pokemon.damage_multiplier(excadrill.type_2)
                        print("Excadrill effectiveness: ", excadrill_effectiveness)
                        opponent_effectiveness = max(excadrill.damage_multiplier(excadrill.type_1), excadrill.damage_multiplier(excadrill.type_2))
                        
                        print("Opponent effectiveness: ", opponent_effectiveness)
                        # If opponent is effec tive against Excadrill and Excadrill is not effective, switch to Latios
                        if excadrill_effectiveness < 1 and opponent_effectiveness >= 1:
                            print("Switching to Latios")
                            pass
                        else:
                            print("Switching to Excadrill")
                            return self.create_order(excadrill)
                    if latios:
                         return self.create_order(latios)
        if battle.available_moves:
            if battle.active_pokemon.species == 'excadrill':
                 print("loop hit 1")
                 for i in battle.opponent_active_pokemon.possible_abilities:
                      print("loop hit")
                      if i =="levitate":
                            print("levitate")
                            iron_head_move = next((move for move in battle.available_moves if move.id == 'ironhead'), None)
                            sword_dance = next((move for move in battle.available_moves if move.id == 'swordsdance'), None)
                            if self.excadril_used_swords_dance != True and sword_dance:
                                self.excadril_used_swords_dance = True
                                return self.create_order(sword_dance)
                            return self.create_order(iron_head_move)
                      else:
                           pass
            best_move = None
            best_score = -float('inf')  # Use negative infinity to ensure any valid move is better
            
            for move in battle.available_moves:
                # Get the base power of the move
                # if battle.active_pokemon.species == 'Azumarill' and not self.azumarill_used_belly_drum and move.id == 'move bellydrum':
                #     self.azumarill_used_belly_drum = True
                #     print("Using Belly Drum")
                #     return self.create_order(move)
                move_power = move.base_power

                # Get the effectiveness of the move on the active enemy Pokemon
                effectiveness = battle.opponent_active_pokemon.damage_multiplier(move)

                stab = 1.5 if move.type in [battle.active_pokemon.type_1, battle.active_pokemon.type_2] else 1.0
                
                # Calculate an overall score using base power and effectiveness
                move_score = move_power * effectiveness *stab
                if move.id == 'bellydrum' and not self.azumarill_used_belly_drum:
                    move_score = float('inf')
                    self.azumarill_used_belly_drum = True
                # Track the move with the highest score
                if move.id == 'stealthrock' and not self.tyranitar_used_stealth_rock:
                    print("Using Stealth Rock")
                    move_score = float('inf')
                    self.tyranitar_used_stealth_rock = True
                if move.id =="swordsdance" and not self.excadril_used_swords_dance:
                    if Weather.SANDSTORM in battle.weather:
                        move_score = float('inf')
                        self.excadril_used_swords_dance = True
                if move_score > best_score:
                    best_score = move_score
                    best_move = move
            return self.create_order(best_move)
        else:
            return self.choose_random_move(battle)