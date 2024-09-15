# Don't change these import settings
import sys

from poke_env import AccountConfiguration, ServerConfiguration
from poke_env.teambuilder.teambuilder import Teambuilder
from poke_env.environment.move_category import MoveCategory
from poke_env.environment.pokemon import Pokemon
from poke_env.environment.pokemon_type import PokemonType
from poke_env.environment.side_condition import SideCondition
from poke_env.environment.target import Target
from poke_env.environment.abstract_battle import AbstractBattle
from poke_env.environment.move_category import MoveCategory
import random
sys.path.append('../players')
from players.gen6player import Gen6Player

class MyPokeBot(Gen6Player):
    
    # Define bot logic here in choose_move
    # Check poke-env documentation for help 
    # Focus is on Battle, Pokemon, Player and Move classes

    # Always return a value with [return self.create_order(move)]
    def __init__(self, account_configuration: AccountConfiguration | None = None, *, avatar: str | None = None, battle_format: str = "gen6ou", log_level: int | None = None, max_concurrent_battles: int = 1, accept_open_team_sheet: bool = False, save_replays: bool | str = True, server_configuration: ServerConfiguration | None = None, start_timer_on_battle_start: bool = False, start_listening: bool = True, ping_interval: float | None = 20, ping_timeout: float | None = 20, team: str | Teambuilder | None = None):
        super().__init__(account_configuration, avatar=avatar, battle_format=battle_format, log_level=log_level, max_concurrent_battles=max_concurrent_battles, accept_open_team_sheet=accept_open_team_sheet, save_replays=save_replays, server_configuration=server_configuration, start_timer_on_battle_start=start_timer_on_battle_start, start_listening=start_listening, ping_interval=ping_interval, ping_timeout=ping_timeout, team=team)
        self.enemy_team = {}
    
    ENTRY_HAZARDS = {
        "spikes": SideCondition.SPIKES,
        "stealhrock": SideCondition.STEALTH_ROCK,
        "stickyweb": SideCondition.STICKY_WEB,
        "toxicspikes": SideCondition.TOXIC_SPIKES,
    }

    ANTI_HAZARDS_MOVES = {"rapidspin", "defog"}

    SPEED_TIER_COEFICIENT = 0.1
    HP_FRACTION_COEFICIENT = 0.4
    SWITCH_OUT_MATCHUP_THRESHOLD = -2

    def _estimate_matchup(self, me, you, opMove, opDamage):
        score = max([you.damage_multiplier(t) for t in me.types if t is not None])
        print(score)
        print([you.damage_multiplier(t) for t in me.types if t is not None])
        score -= max(
            [me.damage_multiplier(t) for t in you.types if t is not None]
        )
        print(score)
        if opMove != None:
            score += you.damage_multiplier(opMove)
        print(score)
        if me.base_stats["spe"] > you.base_stats["spe"]:
            score += self.SPEED_TIER_COEFICIENT
        elif you.base_stats["spe"] > me.base_stats["spe"]:
            score -= self.SPEED_TIER_COEFICIENT
        print(score)

        move = opMove
        physical_ratio = self.correct_stats(me, "atk") / self.correct_stats(
            you, "def"
        )
        special_ratio = self.correct_stats(me, "spa") / self.correct_stats(
            you, "spd"
        )

        if opDamage != None:
            opDamage = move.base_power * (1.5 if move.type in me.types else 1) * (physical_ratio if move.category == MoveCategory.PHYSICAL else special_ratio) * move.expected_hits* you.damage_multiplier(move)

            if me.current_hp > opDamage:
                score += 1
            elif me.current_hp <= opDamage:
                score -= 1
        print(score)
        score += me.current_hp_fraction * self.HP_FRACTION_COEFICIENT
        score -= you.current_hp_fraction * self.HP_FRACTION_COEFICIENT
        print(score)
        return score

    
    def _should_switch_out(self, battle: AbstractBattle):
        active = battle.active_pokemon
        opponent = battle.opponent_active_pokemon
        # If there is a decent switch in...
        if [
            m
            for m in battle.available_switches
            if self._estimate_matchup(m, opponent) > 0
        ]:
            # ...and a 'good' reason to switch out
            if active.boosts["def"] <= -3 or active.boosts["spd"] <= -3:
                return True
            if (
                active.boosts["atk"] <= -3
                and active.stats["atk"] >= active.stats["spa"]
            ):
                return True
            if (
                active.boosts["spa"] <= -3
                and active.stats["atk"] <= active.stats["spa"]
            ):
                return True
            if (
                self._estimate_matchup(active, opponent)
                < self.SWITCH_OUT_MATCHUP_THRESHOLD
            ):
                return True
        return False


    def choose_move(self, battle: AbstractBattle):
        try:
            currMon = battle.active_pokemon
            opMon = battle.opponent_active_pokemon
    
            print(battle.available_moves)
            enemy_move = None
            opdamage = None
            if battle.available_moves:
                print("there are moves")
                highest_damage_move, damage = self.damage_calc(currMon, opMon, battle)
                print(f"my best move {highest_damage_move}")
                if len(opMon.moves) != 0:
                    enemy_move, opdamage = self.damage_calc(opMon, currMon, battle)
                    print(f"my opponents best {enemy_move}")
                else:
                    enemy_move = None
                    opdamage = None
                priority = 6
                opHP = ((2 * opMon.base_stats["hp"] + 31) + 5) * opMon.current_hp/100 # find their hp
                if damage >= opHP:
                    if currMon.base_stats["spe"] > opMon.base_stats["spe"]: # assume no ones gonna make a slow mon somehow faster cuz they aint liddat
                        if battle.can_mega_evolve:
                            return self.create_order(highest_damage_move, mega=True)

                        return self.create_order(highest_damage_move)
                    
                    elif enemy_move != None and opdamage != None:
                        if opdamage >= currMon.current_hp and currMon.current_hp_fraction >= 0.5:
                            # consider switching
                            if battle.available_switches:
                                switches = battle.available_switches
                                return self.create_order(
                                    max(
                                        switches,
                                        key=lambda s: self._estimate_matchup(s, opMon, enemy_move, opdamage),
                                    )
                                )
                # consider switching if u would take 4 turns to kills  
                elif (((2 * opMon.base_stats["hp"] + 31) + 5) - damage)/ ((2 * opMon.base_stats["hp"] + 31) + 5) <0.25: # 
                    if battle.available_switches:
                                switches = battle.available_switches
                                return self.create_order(
                                    max(
                                        switches,
                                        key=lambda s: self._estimate_matchup(s, opMon, enemy_move, opdamage),
                                    )
                                )
                if battle.can_mega_evolve:
                            return self.create_order(highest_damage_move, mega=True)

                return self.create_order(highest_damage_move)
            else:
                if battle.available_switches:
                                switches = battle.available_switches
                                return self.create_order(
                                    max(
                                        switches,
                                        key=lambda s: self._estimate_matchup(s, opMon, enemy_move, opdamage),
                                    )
                                )

            # ai for aron
            if currMon._species == "aron":
                # click endeavor
                print(opMon.possible_abilities)
                if PokemonType.GHOST in opMon.types:
                    print("you should switch")
                else:
                    if currMon.current_hp_fraction == 1 and opMon.current_hp_fraction >= 0.06:
                        return self.create_order(battle.available_moves[0])
                    
                    if currMon.current_hp_fraction == 1 and opMon.current_hp_fraction < 0.06:
                        # click metal burst
                        if PokemonType.ROCK in opMon.types or PokemonType.STEEL in opMon.types or PokemonType.GROUND in opMon.types:
                            return self.create_order(battle.available_moves[3])

                        if PokemonType.POISON in opMon.types:
                            return self.create_order(battle.available_moves[2])
                        else:
                            return self.create_order(battle.available_moves[random.randint(1,2)])
                    
            


        except:
            if battle.available_moves:
                best_move = max(battle.available_moves, key=lambda move: move.base_power)

                if battle.can_mega_evolve:
                    return self.create_order(best_move, mega=True)

                return self.create_order(best_move)
            else:
                return self.choose_random_move(battle)
        
    def correct_stats(self, mon: Pokemon, stat: str):
        # Stats boosts value
        if mon.boosts[stat] > 1:
            boost = (2 + mon.boosts[stat]) / 2
        else:
            boost = 2 / (2 - mon.boosts[stat])
        return ((2 * mon.base_stats[stat] + 31) + 5) * boost
    
    def damage_calc(self, me, you, battle):
        

        physical_ratio = self.correct_stats(me, "atk") / self.correct_stats(
            you, "def"
        )
        special_ratio = self.correct_stats(me, "spa") / self.correct_stats(
            you, "spd"
        )
        print(physical_ratio)
        print(special_ratio)
        max_move = None
        damage = 0
        #for m in me.moves.values:

        move = max(
                me.moves.values(),
                key=lambda m: m.base_power
                * (1.5 if m.type in me.types else 1)
                * (
                    physical_ratio
                    if m.category == MoveCategory.PHYSICAL
                    else special_ratio
                )
                * m.expected_hits
                * you.damage_multiplier(m),
            )
        
        damage = move.base_power * (1.5 if move.type in me.types else 1) * (physical_ratio if move.category == MoveCategory.PHYSICAL else special_ratio) * move.expected_hits* you.damage_multiplier(move)
        return move, damage
    
