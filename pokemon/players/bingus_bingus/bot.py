# bingus bingus


# Don't change these import settings
import sys
sys.path.append('../players')
from players.gen6player import Gen6Player
from poke_env.environment.battle import Battle
from poke_env.player.battle_order import BattleOrder
from poke_env.environment.move import Move


class MyPokeBot(Gen6Player):
    
    def teampreview(self, battle: Battle) -> str:
        return '/team 123456'
    
    def choose_move(self, battle: Battle) -> BattleOrder:
        # If Bingus has million number of fans i am one of them . if Bingus has ten fans i am one of them.
        # if Bingus have only one fan and that is me . if Bingus has no fans, that means i am no more on the earth . 
        # if world against the Bingus, i am against the world. i love #Bingus till my last breath.. .. 
        # Die Hard fan of Bingus . Hit Like If you Think Bingus Best player & Smart In the world
        

        #import os; os.system('pause')
        #print(battle.turn)
        #print(battle.available_moves)
        #print(battle.available_switches)
        
        # shuckle do stuff at start
        try:
            if 'shuckle' in str(battle.active_pokemon):
                if battle.turn==1:
                    return self.create_order(battle.available_moves[0])
                elif battle.turn==2:
                    return self.create_order(battle.available_moves[1])
        except:
            pass
        
        # check if immune
        if battle.opponent_active_pokemon is not None and battle.active_pokemon is not None:
            if len(battle.opponent_active_pokemon.moves)==1:
                if list(battle.opponent_active_pokemon.moves.values())[0].base_power > 0 and battle.active_pokemon.damage_multiplier(list(battle.opponent_active_pokemon.moves.values())[0])!=0:
                    for pokemon in battle.available_switches:
                        if pokemon.damage_multiplier(list(battle.opponent_active_pokemon.moves.values())[0])==0:
                            return self.create_order(pokemon)
        
        
        # best move by damage
        if battle.available_moves and battle.opponent_active_pokemon is not None:
            best_move = max(battle.available_moves, key=lambda move: move.base_power * battle.opponent_active_pokemon.damage_multiplier(move))
            return self.create_order(best_move)
        
        # best move by base power
        if battle.available_moves:
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            return self.create_order(best_move)
        
        # switch
        
        if battle.opponent_active_pokemon is not None:
            best_dmg = 0
            best_pkm = battle.available_switches[0]
            for pokemon in battle.available_switches:
                for move in list(pokemon.moves.values()):
                    dmg = move.base_power * battle.opponent_active_pokemon.damage_multiplier(move)
                    if dmg > best_dmg:
                        best_dmg = dmg
                        best_pkm = pokemon
            return self.create_order(best_pkm)
        
        # idk
            
        return self.choose_random_move(battle)