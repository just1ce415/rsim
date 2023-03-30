from src.constants import *
from entities.characters.character import Character
from entities.enemies.enemy import Enemy

from typing import List, Dict

class Environment:
    def __init__(
            self, team:List[Character], actions:List,
            n_targets:int, enemy_res:Dict[str: float], enemy_lvl:int,
            loggers:str
        ):
        self.time_passed = 0
        self.swap_cd = 0
        self.loggers = loggers
        self.team = team
        self.onfield_character = self.team[0]
        self.weapons = [character.weapon for character in self.team]
        self.set_bonuses = [character.dynamic_set_bonus for character in self.team]
        self.data = {}
        self.__init_data()
        self.summons_and_adaptives = []
        self.dendro_cores = []
        self.current_action = None
        self.particle_sets = []
        self.actions = actions
        self.n_targets = n_targets
        self.enemies = [Enemy(enemy_lvl, enemy_res) for _ in range(self.n_targets)]
        for character in self.team:
            character.set_team(self.team)
            character.set_enemies(self.enemies)
        self.__activate_resonanse()

    def start(self):
        while len(self.actions) > 0 or self.current_action is not None:
            self.time_passed += 1/FPS

    def __activate_resonanse(self):
        pass

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
                    "level_multiplier": [],
                    "reaction_bonus": [],
                    "quadratic_factor": [],
                    "dmg_type": [],
                    "hp_level": [],
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
                    "level_multiplier": [],
                    "reaction_bonus": [],
                    "quadratic_factor": [],
                    "dmg_type": [],
                    "hp_level": [],
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
                    "level_multiplier": [],
                    "reaction_bonus": [],
                    "quadratic_factor": [],
                    "dmg_type": [],
                    "hp_level": [],
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
                    "level_multiplier": [],
                    "reaction_bonus": [],
                    "quadratic_factor": [],
                    "dmg_type": [],
                    "hp_level": [],
                    "outgoing_damage": []
                }
            },
            "er_info": {
                self.team[0]: {
                    "particle_energy_each_rotation": [],
                    "energy_each_rotation": [],
                    "cost_each_rotation": [],
                    "actual_er_each_rotation": []
                },
                self.team[1]: {
                    "particle_energy_each_rotation": [],
                    "energy_each_rotation": [],
                    "cost_each_rotation": [],
                    "actual_er_each_rotation": []
                },
                self.team[2]: {
                    "particle_energy_each_rotation": [],
                    "energy_each_rotation": [],
                    "cost_each_rotation": [],
                    "actual_er_each_rotation": []
                },
                self.team[3]: {
                    "particle_energy_each_rotation": [],
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