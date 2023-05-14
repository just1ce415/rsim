from src.constants import *
from src.damage import *
from entities.characters.character import Character
from entities.enemies.enemy import Enemy
from src.event import Event
from src.entities.summons_and_adaptives.adaptive import *
from src.entities.summons_and_adaptives.summon import Summon
from src.entities.summons_and_adaptives.reaction_summons import *
from src.entities.weapons.weapon import Weapon
from src.entities.artifacts.set_bonus import SetBonus
from src.entities.other.particle_set import ParticleSet

from typing import List, Dict
from random import random

class Environment:
    def __init__(
            self, team:List[Character], actions:List,
            n_targets:int, enemy_res:Dict[str: float], enemy_lvl:int,
            loggers:str
        ):
        self.time_passed = 0
        self.swap_cd = 0
        self.loggers = loggers
        self.team: List[Character] = team
        self.onfield_character = self.team[0]
        self.team[0].on_field = True
        self.weapons: List[Weapon] = [character.weapon for character in self.team]
        self.set_bonuses: List[SetBonus] = [character.dynamic_set_bonus for character in self.team]
        self.data = {}
        self.__init_data()
        self.summons_and_adaptives: List[Summon] = []
        self.dendro_cores: List[DendroCore] = []
        self.current_action = None
        self.particle_sets: List[ParticleSet] = []
        self.actions: List[Action] = actions
        self.n_targets = n_targets
        self.enemies: List[Enemy] = [Enemy(enemy_lvl, enemy_res) for _ in range(self.n_targets)]
        for character in self.team:
            character.set_team(self.team)
            character.set_enemies(self.enemies)
        self.rupture_icd = {
            self.team[0]: [0, True],
            self.team[1]: [0, True],
            self.team[2]: [0, True],
            self.team[3]: [0, True]
        }
        self.__activate_resonanse()

    def start(self):
        while len(self.actions) > 0 or self.current_action is not None:
            for weapon in self.weapons:
                weapon.time_passes(1/FPS)
            for set_bonus in self.set_bonuses:
                set_bonus.time_passes(1/FPS)
            for character in self.team:
                character.time_passes(1/FPS)
            for i, summon in enumerate(self.summons_and_adaptives):
                summon.time_passes(1/FPS)
                if summon.dmg_stats_ready:
                    # if summon can apply element
                    if summon.icd_group:
                        # Last index is for character and weapon reaction
                        reactions_total = [0 for _ in range(len(self.enemies) + 1)]
                        # Apply element to enemies
                        if summon.apply_to_enemy:
                            for enemy_index in summon.targets:
                                if summon.icd_group.try_apply_element(self.enemies[enemy_index]):
                                    reactions = self.enemies[enemy_index].\
                                    gauge_status.apply_element(summon.elemental_type, summon.gu)
                                    reactions_total[enemy_index] = reactions
                                # notify everyone regardless of whether summon applied element of not
                                self.__notify_all(Event(
                                    event_type=CHARACTER_ATTACKS, character_one=summon.summoner, attack_type=summon.attack_type,
                                    dmg_type=summon.dmg_type, attack_elemental_type=summon.elemental_type,
                                    enemy=self.enemies[enemy_index]
                                    ))
                        # Apply element to summons (Dendro Lumin burst)
                        if summon.apply_to_enemy:
                            for app_summon in self.summons_and_adaptives:
                                pass
                        # Apply element to dendro cores
                        if summon.apply_to_enemy:
                            for dendro_core in self.dendro_cores:
                                pass
                        # Apply element to character
                        if summon.apply_to_character:
                            for character in self.team:
                                pass
                        # Apply element to weapons
                        if summon.apply_to_weapon:
                            for weapon in self.weapons:
                                pass
                        # Decide what this func will do
                        self.__process_reactions(reactions_total)
                    # else summon does not apply element
                    else:
                        for enemy_index in summon.targets:
                            self.__notify_all(Event(
                                event_type=CHARACTER_ATTACKS, character_one=summon.summoner, attack_type=summon.attack_type,
                                dmg_type=summon.dmg_type, attack_elemental_type=PHYS,
                                enemy=self.enemies[enemy_index]
                                ))
                    # Calc outgoing talent damage for target of interest (always 0th enemy)
                    if 0 in summon.targets:
                        # Shall we calculate general dmg or talent dmg here?
                        temp_damage = general_dmg(
                            summon.base_hp, summon.base_atk, summon.base_def, summon.flat_hp, summon.flat_atk,
                            summon.flat_def, summon.hp_percent, summon.atk_percent, summon.def_percent,
                            summon.em, summon.mv_hp, summon.mv_atk, summon.mv_def, summon.mv_em,
                            summon.flat_dmg, summon.dmg_bonus, summon.crit_ratio, summon.cd, summon.cr,
                            summon.reaction_multiplier, summon.level, summon.reaction_bonus
                            )
                        outgoing_damage = outgoing_dmg_multiplicative(
                            temp_damage, summon.level, self.enemies[0].level, self.enemies[0].resistance[summon.elemental_type],
                            self.enemies[0].def_shred, self.enemies[0].def_ignore
                        )
                        self.__write_dmg(summon, outgoing_damage)
                    # notify everyone that hit was performed
                    for enemy_index in summon.targets:
                        cr = get_cr(summon.cd, summon.cr, summon.crit_ratio)
                        scored = random() < cr
                        self.__notify_all(Event(
                            event_type=CHARACTER_HITS, character_one=summon.summoner, attack_type=summon.attack_type,
                            dmg_type=summon.dmg_type, attack_elemental_type=summon.elemental_type,
                            enemy=self.enemies[enemy_index], scored_crit=scored
                        ))

                if summon.heal_stats_ready:
                    pass
                if summon.hp_reduced:
                    pass
                if summon.shield_stats_ready:
                    pass
                if summon.particle_set:
                    pass
                if summon.summon:
                    pass
                if summon.timedout:
                    del self.summons_and_adaptives[i]

            if self.current_action is None:
                self.current_action = self.actions.pop(0)
            self.current_action.time_passes(1/FPS)
            if self.current_action.dmg_stats_ready:
                pass
            if self.current_action.heal_stats_ready:
                pass
            if self.current_action.hp_reduced:
                pass
            if self.current_action.shield_stats_ready:
                pass
            if self.current_action.particle_set:
                pass
            if self.current_action.summon:
                pass
            if self.current_action.dash:
                pass
            if self.current_action.jump:
                pass
            if self.current_action.wait:
                pass
            if self.current_action.swap:
                pass
            if self.current_action.timedout:
                self.current_action = None
            
            for i, dendro_core in enumerate(self.dendro_cores):
                pass

            for i, particle_set in enumerate(self.particle_sets):
                particle_set.time_passes(1/FPS)
                if particle_set.timedout:
                    self.__notify_all(Event(
                    PICKED_PARTICLE, character_one=self.onfield_character, particle_type=particle_set.element))
                    del self.particle_sets[i]

            self.time_passed += 1/FPS
            self.swap_cd = max(0, self.swap_cd - 1/FPS)

    def __activate_resonanse(self):
        element_list = [char.elemental_type for char in self.team]
        if element_list.count(PYRO) >= 2:
            for char in self.team:
                char.atk_percent += 0.25
        if element_list.count(HYDRO) >= 2:
            for char in self.team:
                char.hp_percent += 0.25
        if element_list.count(ELECTRO) >= 2:
            self.summons_and_adaptives.append(ElectroResonance(self.team[0]))
        if element_list.count(CRYO) >= 2:
            self.summons_and_adaptives.append(CryoResonance(self.team[0]))
        if element_list.count(ANEMO) >= 2:
            for char in self.team:
                char.cooldown_reduction += 0.05
                char.ca_stamina_decrease += 0.15
                char.dash_stamina_decrease += 0.15
        if element_list.count(GEO) >= 2:
            for char in self.team:
                char.shield_strength += 0.15
            self.summons_and_adaptives.append(GeoResonance(self.team[0]))
        if element_list.count(DENDRO) >= 2:
            for char in self.team:
                char.em += 50
            self.summons_and_adaptives.append(DendroResonance(self.team[0]))

    def __notify_all(self, event:Event):
        for weapon in self.weapons:
            weapon.notify(event)
        for set_bonus in self.set_bonuses:
            set_bonus.notify(event)
        for summon in self.summons_and_adaptives:
            summon.notify(event)

    def __hitlag_extend_all(self, seconds:float):
        for weapon in self.weapons:
            weapon.hitlag_extension(seconds)
        for set_bonus in self.set_bonuses:
            set_bonus.hitlag_extension(seconds)
        for summon in self.summons_and_adaptives:
            summon.hitlag_extension(seconds)

    def __write_dmg(self, summon:Summon, outgoing_damage):
        self.data["dmg_info"][summon.summoner]["time"].append(self.time_passed)
        self.data["dmg_info"][summon.summoner]["base_hp"].append(summon.base_hp)
        self.data["dmg_info"][summon.summoner]["base_atk"].append(summon.base_atk)
        self.data["dmg_info"][summon.summoner]["base_def"].append(summon.base_def)
        self.data["dmg_info"][summon.summoner]["flat_hp"].append(summon.flat_hp)
        self.data["dmg_info"][summon.summoner]["flat_atk"].append(summon.flat_atk)
        self.data["dmg_info"][summon.summoner]["flat_def"].append(summon.flat_def)
        self.data["dmg_info"][summon.summoner]["hp_percent"].append(summon.hp_percent)
        self.data["dmg_info"][summon.summoner]["atk_percent"].append(summon.atk_percent)
        self.data["dmg_info"][summon.summoner]["def_percent"].append(summon.def_percent)
        self.data["dmg_info"][summon.summoner]["em"].append(summon.em)
        self.data["dmg_info"][summon.summoner]["mv_atk"].append(summon.mv_atk)
        self.data["dmg_info"][summon.summoner]["mv_hp"].append(summon.mv_hp)
        self.data["dmg_info"][summon.summoner]["mv_def"].append(summon.mv_def)
        self.data["dmg_info"][summon.summoner]["mv_em"].append(summon.mv_em)
        self.data["dmg_info"][summon.summoner]["flat_dmg"].append(summon.flat_dmg)
        self.data["dmg_info"][summon.summoner]["dmg_bonus"].append(summon.dmg_bonus)
        self.data["dmg_info"][summon.summoner]["crit_ratio"].append(summon.crit_ratio)
        self.data["dmg_info"][summon.summoner]["cd"].append(summon.cd)
        self.data["dmg_info"][summon.summoner]["cr"].append(summon.cr)
        self.data["dmg_info"][summon.summoner]["reaction_multiplier"].append(summon.reaction_multiplier)
        self.data["dmg_info"][summon.summoner]["level"].append(summon.level)
        self.data["dmg_info"][summon.summoner]["reaction_bonus"].append(summon.reaction_bonus)
        self.data["dmg_info"][summon.summoner]["quadric_factor"].append(summon.quadratic_factor)
        self.data["dmg_info"][summon.summoner]["dmg_type"].append(summon.dmg_type)
        self.data["dmg_info"][summon.summoner]["element"].append(summon.elemental_type)
        self.data["dmg_info"][summon.summoner]["hp_level"].append(summon.summoner.hp_level)
        self.data["dmg_info"][summon.summoner]["targeting"].append("ST" if len(summon.targets) == 1 else "AOE")
        self.data["dmg_info"][summon.summoner]["outgoing_damage"].append(outgoing_damage)

    def __write_er(self, summon:Summon):
        self.data["er_info"][summon.summoner]["energy_each_rotation"].append(summon.summoner.energy)
        self.data["er_info"][summon.summoner]["cost_each_rotation"].append(summon.summoner.burst_cost)
        self.data["er_info"][summon.summoner]["actual_er_each_rotation"].append(summon.summoner.er)

    def __write_defensive(self, shielding_instance, healing_instance, summon:Summon):
        self.data["defensive_info"][summon.summoner]["time"].append(self.time_passed)
        self.data["defensive_info"][summon.summoner]["shielding_instances"].append(shielding_instance)
        self.data["defensive_info"][summon.summoner]["healing_instances"].append(healing_instance)

    def __process_reactions(reactions_total:List[List[str, float, int, Summon, List[str, float]]]):
        """
        Processes all reactions triggered, but damage is written only for the main target - 0.
        Returns multiplicative reaction factor, if any, else 1.
        """
        return 1

    def __init_data(self):
        self.data = {
            "time_spent": 0,
            "dmg_info": {
                self.team[0]: {
                    "time": [],
                    "base_hp": [],
                    "base_atk": [],
                    "base_def": [],
                    "flat_hp": [],
                    "flat_atk": [],
                    "flat_def": [],
                    "hp_percent": [],
                    "atk_percent": [],
                    "def_percent": [],
                    "em": [],
                    "mv_atk": [],
                    "mv_hp": [],
                    "mv_def": [],
                    "mv_em": [],
                    "flat_dmg": [],
                    "dmg_bonus": [],
                    "crit_ratio": [],
                    "cd": [],
                    "cr": [],
                    "reaction_multiplier": [],
                    "level": [],
                    "reaction_bonus": [],
                    "quadratic_factor": [],
                    "dmg_type": [],
                    "element": [],
                    "hp_level": [],
                    "targeting": [],
                    "outgoing_damage": []
                },
                self.team[1]: {
                    "time": [],
                    "base_hp": [],
                    "base_atk": [],
                    "base_def": [],
                    "flat_hp": [],
                    "flat_atk": [],
                    "flat_def": [],
                    "hp_percent": [],
                    "atk_percent": [],
                    "def_percent": [],
                    "em": [],
                    "mv_atk": [],
                    "mv_hp": [],
                    "mv_def": [],
                    "mv_em": [],
                    "flat_dmg": [],
                    "dmg_bonus": [],
                    "crit_ratio": [],
                    "cd": [],
                    "cr": [],
                    "reaction_multiplier": [],
                    "level": [],
                    "reaction_bonus": [],
                    "quadratic_factor": [],
                    "dmg_type": [],
                    "element": [],
                    "hp_level": [],
                    "targeting": [],
                    "outgoing_damage": []
                },
                self.team[2]: {
                    "time": [],
                    "base_hp": [],
                    "base_atk": [],
                    "base_def": [],
                    "flat_hp": [],
                    "flat_atk": [],
                    "flat_def": [],
                    "hp_percent": [],
                    "atk_percent": [],
                    "def_percent": [],
                    "em": [],
                    "mv_atk": [],
                    "mv_hp": [],
                    "mv_def": [],
                    "mv_em": [],
                    "flat_dmg": [],
                    "dmg_bonus": [],
                    "crit_ratio": [],
                    "cd": [],
                    "cr": [],
                    "reaction_multiplier": [],
                    "level": [],
                    "reaction_bonus": [],
                    "quadratic_factor": [],
                    "dmg_type": [],
                    "element": [],
                    "hp_level": [],
                    "targeting": [],
                    "outgoing_damage": []
                },
                self.team[3]: {
                    "time": [],
                    "base_hp": [],
                    "base_atk": [],
                    "base_def": [],
                    "flat_hp": [],
                    "flat_atk": [],
                    "flat_def": [],
                    "hp_percent": [],
                    "atk_percent": [],
                    "def_percent": [],
                    "em": [],
                    "mv_atk": [],
                    "mv_hp": [],
                    "mv_def": [],
                    "mv_em": [],
                    "flat_dmg": [],
                    "dmg_bonus": [],
                    "crit_ratio": [],
                    "cd": [],
                    "cr": [],
                    "reaction_multiplier": [],
                    "level": [],
                    "reaction_bonus": [],
                    "quadratic_factor": [],
                    "dmg_type": [],
                    "element": [],
                    "hp_level": [],
                    "targeting": [],
                    "outgoing_damage": []
                }
            },
            "er_info": {
                self.team[0]: {
                    "energy_each_rotation": [],
                    "cost_each_rotation": [],
                    "actual_er_each_rotation": []
                },
                self.team[1]: {
                    "energy_each_rotation": [],
                    "cost_each_rotation": [],
                    "actual_er_each_rotation": []
                },
                self.team[2]: {
                    "energy_each_rotation": [],
                    "cost_each_rotation": [],
                    "actual_er_each_rotation": []
                },
                self.team[3]: {
                    "energy_each_rotation": [],
                    "cost_each_rotation": [],
                    "actual_er_each_rotation": []
                }
            },
            "defensive_info": {
                self.team[0]: {
                    "time": [],
                    "shielding_instances": [],
                    "healing_instances": []
                },
                self.team[1]: {
                    "time": [],
                    "shielding_instances": [],
                    "healing_instances": []
                },
                self.team[2]: {
                    "time": [],
                    "shielding_instances": [],
                    "healing_instances": []
                },
                self.team[3]: {
                    "time": [],
                    "shielding_instances": [],
                    "healing_instances": []
                }
            }
        }
