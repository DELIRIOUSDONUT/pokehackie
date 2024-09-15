from poke_env.environment import AbstractBattle, MoveCategory
from poke_env.environment.pokemon import Pokemon
from poke_env.environment.side_condition import SideCondition
import sys
sys.path.append('../players')
from players.gen6player import Gen6Player

class RulesBased(Gen6Player):
    # Rules based bot with dmg heuristics
    ENTRY_HAZARDS = {
        "spikes": SideCondition.SPIKES,
        "stealthrock": SideCondition.STEALTH_ROCK,
        "stickyweb": SideCondition.STICKY_WEB,
        "toxicspikes": SideCondition.TOXIC_SPIKES,
    }

    ANTI_HAZARDS_MOVES = {"rapidspin", "defog"}

    def estimate_matchup(self, pokemon: Pokemon, opponent: Pokemon):
        score = self._calculate_type_advantage(pokemon, opponent)
        score += self._calculate_speed_advantage(pokemon, opponent)
        score += self._calculate_hp_advantage(pokemon, opponent)
        return score

    def _calculate_type_advantage(self, pokemon: Pokemon, opponent: Pokemon):
        max_damage_to_opponent = float('-inf')
        for t in pokemon.types:
            if t is not None:
                damage_multiplier = opponent.damage_multiplier(t)
                if damage_multiplier > max_damage_to_opponent:
                    max_damage_to_opponent = damage_multiplier

        max_damage_to_self = float('-inf')  
        for t in opponent.types:
            if t is not None:
                damage_multiplier = pokemon.damage_multiplier(t)
                if damage_multiplier > max_damage_to_self:
                    max_damage_to_self = damage_multiplier

        return max_damage_to_opponent - max_damage_to_self

    def _calculate_speed_advantage(self, pokemon: Pokemon, opponent: Pokemon):
        if pokemon.base_stats["spe"] > opponent.base_stats["spe"]:
            return 0.1
        elif opponent.base_stats["spe"] > pokemon.base_stats["spe"]:
            return -0.1
        return 0

    def _calculate_hp_advantage(self, pokemon: Pokemon, opponent: Pokemon):
        return (
            pokemon.current_hp_fraction * 0.4
            - opponent.current_hp_fraction * 0.4
        )

    def should_switch_out(self, battle: AbstractBattle):
        active = battle.active_pokemon
        opponent = battle.opponent_active_pokemon

        if any(self.estimate_matchup(p, opponent) > 0 for p in battle.available_switches):
            if self._should_switch_due_to_boosts(active) or self.estimate_matchup(active, opponent) < -2:
                return True
        return False

    def _should_switch_due_to_boosts(self, active: Pokemon):
        if active.boosts["def"] <= -3 or active.boosts["spd"] <= -3:
            return True
        if active.boosts["atk"] <= -3 and active.stats["atk"] >= active.stats["spa"]:
            return True
        if active.boosts["spa"] <= -3 and active.stats["atk"] <= active.stats["spa"]:
            return True
        return False

    def stat_estimation(self, pokemon: Pokemon, stat: str):
        boost = (2 + pokemon.boosts[stat]) / 2 if pokemon.boosts[stat] > 1 else 2 / (2 - pokemon.boosts[stat])
        return ((2 * pokemon.base_stats[stat] + 31) + 5) * boost
    
    def physical_ratio_form(self, pokemon: Pokemon, opponent: Pokemon):
        return self.stat_estimation(pokemon, "atk") / self.stat_estimation(opponent, "def")
    def special_ratio_form(self, pokemon: Pokemon, opponent: Pokemon):
        return self.stat_estimation(pokemon, "spa") / self.stat_estimation(opponent, "spd")

    def choose_move(self, battle: AbstractBattle):
        active = battle.active_pokemon
        opponent = battle.opponent_active_pokemon

        if battle.available_moves and (not self.should_switch_out(battle) or not battle.available_switches):
            return self._choose_best_move(battle, active, opponent)

        if battle.available_switches:
            return self._choose_best_switch(battle, opponent)

        return self.choose_random_move(battle)

    def _choose_best_move(self, battle: AbstractBattle, pokemon: Pokemon, opponent: Pokemon):
        normal_attack_ratio = self.physical_ratio_form(pokemon, opponent)
        special_attack_ratio = self.special_ratio_form(pokemon, opponent)

        remaining_pokemon = len([p for p in battle.team.values() if p.fainted is False])
        remaining_opponents = 6 - len([p for p in battle.opponent_team.values() if p.fainted is True])

        for move in battle.available_moves:
            if self._should_set_entry_hazard(remaining_opponents, move, battle):
                return self.create_order(move)
            if self._should_remove_hazards(remaining_pokemon, move, battle):
                return self.create_order(move)

        if self._should_use_boosting_move(pokemon, opponent):
            boosting_move = self._find_boosting_move(battle)
            if boosting_move:
                return self.create_order(boosting_move)

        move = self._find_most_damaging_move(battle, pokemon, opponent, normal_attack_ratio, special_attack_ratio)
        return self.create_order(move)

    def _should_set_entry_hazard(self, remaining_opponents, move, battle: AbstractBattle):
        return (
            remaining_opponents >= 3
            and move.id in self.ENTRY_HAZARDS
            and self.ENTRY_HAZARDS[move.id] not in battle.opponent_side_conditions
        )

    def _should_remove_hazards(self, remaining_pokemon, move, battle: AbstractBattle):
        return battle.side_conditions and move.id in self.ANTI_HAZARDS_MOVES and remaining_pokemon >= 2

    def _should_use_boosting_move(self, pokemon: Pokemon, opponent: Pokemon):
        return pokemon.current_hp_fraction == 1 and self.estimate_matchup(pokemon, opponent) > 0

    def _find_boosting_move(self, battle):
        for move in battle.available_moves:
            if move.boosts and sum(move.boosts.values()) >= 2 and move.target == "self":
                return move
        return None

    def _find_most_damaging_move(self, battle: AbstractBattle, pokemon: Pokemon, opponent: Pokemon, physical_ratio, special_ratio):
        return max(
            battle.available_moves,
            key=lambda m: m.base_power
            * (1.5 if m.type in pokemon.types else 1)
            * (physical_ratio if m.category == MoveCategory.PHYSICAL else special_ratio)
            * m.accuracy
            * m.expected_hits
            * opponent.damage_multiplier(m),
        )

    def _choose_best_switch(self, battle: AbstractBattle, opponent: Pokemon):
        return self.create_order(
            max(
                battle.available_switches,
                key=lambda s: self.estimate_matchup(s, opponent),
            )
        )