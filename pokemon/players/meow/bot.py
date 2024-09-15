# Don't change these import settings
import sys
sys.path.append('../players')
from players.gen6player import Gen6Player

# Import the required classes    
from poke_env.environment.move import Move
from poke_env.environment.pokemon import Pokemon

class MyPokeBot(Gen6Player):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rocks_count = 0  # Initialize a counter for setting Stealth Rock
        self.roost = 0  # Initialize a counter for using Roost


    def choose_move(self, battle):
        
        if battle.available_moves:
            # Get the active Pokémon
            active_pokemon = battle.active_pokemon
            opponent_pokemon = battle.opponent_active_pokemon
            print("Active Pokemon: ", active_pokemon)
            print("Available moves:", battle.available_moves)
            #available_moves = battle.available_moves
        
            # Define move logic for Keldeo
            if active_pokemon.species == "keldeo":
                print("Keldeo", active_pokemon.type_1, active_pokemon.type_2)

                # Use Hydro Pump if it's super effective
                if opponent_pokemon and (opponent_pokemon.type_1 in ["Fire", "Ground", "Rock"] or opponent_pokemon.type_2 in ["Fire",   "Ground", "Rock"]):
                    print("Hydro Pump")
                    return self.create_order(Move("hydropump", 6))

                # Use Secret Sword if it's super effective
                if opponent_pokemon and (opponent_pokemon.type_1 in ["Normal", "Rock", "Steel", "Ice", "Dark"] or opponent_pokemon.type_2   in ["Normal", "Rock", "Steel", "Ice", "Dark"]):
                    print("Secret Sword")
                    return self.create_order(Move("secretsword", 6))

                # Use Scald if it's super effective
                if opponent_pokemon and (opponent_pokemon.type_1 in ["Fire", "Ground", "Rock"] or opponent_pokemon.type_2 in ["Fire",   "Ground", "Rock"]):
                    print("Scald")
                    return self.create_order(Move("scald", 6))

                # Use Icy Wind if it's super effective
                if opponent_pokemon and (opponent_pokemon.type_1 in ["Flying", "Ground", "Grass", "Dragon"] or opponent_pokemon.type_2 in   ["Flying", "Ground", "Grass", "Dragon"]):
                    print("Icy Wind")
                    return self.create_order(Move("icywind", 6))

                # Default move if no specific logic applies
                return self.choose_random_move(battle)


            # Define move logic for Excadrill
            if active_pokemon.species == "excadrill":
                print("Excadrill", active_pokemon.type_1, active_pokemon.type_2)

                # Use Earthquake if it's super effective
                if opponent_pokemon and (opponent_pokemon.type_1 in ["Fire", "Electric", "Rock", "Steel", "Poison"] or opponent_pokemon.    type_2 in ["Fire", "Electric", "Rock", "Steel", "Poison"]):
                    print("Earthquake")
                    return self.create_order(Move("earthquake", 6))

                # Use Iron Head if it's super effective
                if opponent_pokemon and (opponent_pokemon.type_1 in ["Fairy", "Ice", "Rock"] or opponent_pokemon.type_2 in ["Fairy", "Ice", "Rock"]):
                    print("Iron Head")
                    return self.create_order(Move("ironhead", 6))

                # Use Rock Slide if it's super effective
                if opponent_pokemon and (opponent_pokemon.type_1 in ["Flying", "Bug", "Fire", "Ice"] or opponent_pokemon.type_2 in  ["Flying", "Bug", "Fire", "Ice"]):
                    print("Rock Slide")
                    return self.create_order(Move("rockslide", 6))

                # Use Rapid Spin to remove hazards
                if battle.side_conditions or battle.opponent_side_conditions:
                    print("Rapid Spin")
                    return self.create_order(Move("rapidspin", 6))
                
                # Default move if no specific logic ap
                return self.choose_random_move(battle)


            # Define move logic for Thundurus
            if active_pokemon.species == "thundurus":
                print("Thundurus", active_pokemon.type_1, active_pokemon.type_2)

                # Use Thunderbolt if it's super effective
                if opponent_pokemon and (opponent_pokemon.type_1 in ["Water", "Flying"] or opponent_pokemon.type_2 in ["Water", "Flying"]):
                    print("Thunderbolt")
                    return self.create_order(Move("thunderbolt", 6))

                # Use Hidden Power Ice if it's super effective
                if opponent_pokemon and (opponent_pokemon.type_1 in ["Flying", "Ground", "Grass", "Dragon"] or opponent_pokemon.type_2 in   ["Flying", "Ground", "Grass", "Dragon"]):
                    print("Hidden Power Ice")
                    return self.create_order(Move("hiddenpowerice", 6))

                # Use Focus Blast if it's super effective
                if opponent_pokemon and (opponent_pokemon.type_1 in ["Normal", "Rock", "Steel", "Ice", "Dark"] or opponent_pokemon.type_2   in ["Normal", "Rock", "Steel", "Ice", "Dark"]):
                    print("Focus Blast")
                    return self.create_order(Move("focusblast", 6))

                # Use Thunder Wave to paralyze the opponent
                #if opponent_pokemon and not opponent_pokemon.status:
                #    print("Thunder Wave")
                #    return self.create_order(Move("thunderwave", 6))

                # Default move if no specific logic ap
                return self.choose_random_move(battle)


            # Define move logic for Bisharp
            if active_pokemon.species == "bisharp":
                print("Bisharp", active_pokemon.type_1, active_pokemon.type_2)

                # Use Knock Off to remove items
                if opponent_pokemon and opponent_pokemon.item is not None:
                    print("Knock Off")
                    return self.create_order(Move("knockoff", 6))

                # Use Iron Head if it's super effective
                if opponent_pokemon and (opponent_pokemon.type_1 in ["Fairy", "Ice", "Rock"] or opponent_pokemon.type_2 in ["Fairy", "Ice", "Rock"]):
                    print("Iron Head")
                    return self.create_order(Move("ironhead", 6))

                # Use Sucker Punch for priority
                if opponent_pokemon and (opponent_pokemon.type_1 in ["Fairy", "Ice", "Rock"] or opponent_pokemon.type_2 in ["Fairy", "Ice", "Rock"]):
                    print("Sucker Punch")
                    return self.create_order(Move("suckerpunch", 6))

                # Use Swords Dance to boost attack
                if not active_pokemon.boosts["atk"]:
                    print("Swords Dance")
                    return self.create_order(Move("swordsdance", 6))
                
                # Default move if no specific logic ap
                return self.choose_random_move(battle)
            
            
            # Define move logic for Garchomp
            if active_pokemon.species == "garchomp":
                print("Garchomp", active_pokemon.type_1, active_pokemon.type_2)

                # Use Earthquake if it's super effective
                if opponent_pokemon and (opponent_pokemon.type_1 in ["Fire", "Electric", "Rock", "Steel", "Poison"] or opponent_pokemon.type_2 in ["Fire", "Electric", "Rock", "Steel", "Poison"]):
                    print("Earthquake")
                    return self.create_order(Move("earthquake", 6))

                # Use Dragon Tail if it's super effective
                if opponent_pokemon and (opponent_pokemon.type_1 in ["Dragon"] or opponent_pokemon.type_2 in ["Dragon"]):
                    print("Dragon Tail")
                    return self.create_order(Move("dragontail", 6))

                # Use Fire Blast if it's super effective
                if opponent_pokemon and (opponent_pokemon.type_1 in ["Steel", "Grass", "Bug", "Ice"] or opponent_pokemon.type_2 in  ["Steel", "Grass", "Bug", "Ice"]):
                    print("Fire Blast")
                    return self.create_order(Move("fireblast", 6))

                # Use Stealth Rock to set entry hazards
                if not battle.side_conditions and self.rocks_count < 1:
                    self.rocks_count += 1
                    print(f"rocks_count (used {self.rocks_count} times)")
                    return self.create_order(Move("stealthrock", 6))
                
                # Default move if no specific logic ap
                return self.choose_random_move(battle)
            
            
            # Define move logic for Latias
            if active_pokemon.species == "latias":
                print("Latias", active_pokemon.type_1, active_pokemon.type_2)

                # Use Draco Meteor if it's super effective
                if opponent_pokemon and (opponent_pokemon.type_1 in ["Dragon"] or opponent_pokemon.type_2 in ["Dragon"]):
                    print("Draco Meteor")
                    return self.create_order(Move("dracometeor", 6))

                # Use Psyshock if it's super effective
                if opponent_pokemon and (opponent_pokemon.type_1 in ["Fighting", "Poison"] or opponent_pokemon.type_2 in ["Fighting",   "Poison"]):
                    print("Psyshock")
                    return self.create_order(Move("psyshock", 6))

                # Use Defog to remove hazards
                #if battle.side_conditions or battle.opponent_side_conditions:
                #    print("Defog")
                #    return self.create_order(Move("defog", 6))

                # Use Roost to heal if Latias's HP is low
                if active_pokemon.current_hp_fraction < 0.5 and self.roost < 16:
                    self.roost += 1
                    print("Roost", self.roost)
                    return self.create_order(Move("roost", 6))

                # Default move if no specific logic ap
                return self.choose_random_move(battle)
            
            
        else:
            print("Default move")
            return self.choose_random_move(battle)
        
        print("Default move")
        return self.choose_random_move(battle)
