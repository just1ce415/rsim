from src.entities.entity import Entity
from src.entities.enemies.enemy import Enemy
from src.constants import *

from typing import List

class Character(Entity):
    def __init__(
            self, level=90, talent_lvls=(9, 9, 9), constallation=0, crit_ratio=1/2
        ):
        # General info
        self.is_alive = True
        self.on_field = False
        self.affliction = NONE
        self.weapon_type = NONE
        self.elemental_type = NONE
        self.stamina = 240
        self._set_general_info()

        # Stamina info
        self.stamina_icd = 0
        # (ICD, is_able_to_dash)
        self.dash_icd = [0, True]
        self.dash_stamina_decrease = 0
        self.ca_stamina_decrease = 0

        # Equipment info
        self.level = level
        self.weapon = None
        self.flower = None
        self.feather = None
        self.sands = None
        self.goblet = None
        self.circlet = None
        self.set_bonus_counter = {}
        self.set_bonus1 = None
        self.set_bonus2 = None
        self.dynamic_set_bonus = None
        self.talent_lvls = talent_lvls
        self.constallation = constallation

        # Stats
        self.base_hp = 0
        self.base_atk = 0
        self.base_def = 0
        self.flat_hp = 0
        self.flat_atk = 0
        self.flat_def = 0
        self.hp_percent = 0
        self.atk_percent = 0
        self.def_percent = 0
        self.em = 0
        self.er = 1
        self._activate_base_stats()

        self.anemo_dmg_bonus = 0
        self.hydro_dmg_bonus = 0
        self.electro_dmg_bonus = 0
        self.dendro_dmg_bonus = 0
        self.cryo_dmg_bonus = 0
        self.pyro_dmg_bonus = 0
        self.geo_dmg_bonus = 0
        self.phys_dmg_bonus = 0

        self.crit_ratio = crit_ratio
        self.cd = 0.5
        self.cr = 0.05

        self.healing_bonus = 0
        self.healing_received = 0
        self.shield_strength = 0
        self.cooldown_reduction = 0

        # Skills general info
        self.skill_cooldown = 0
        self.burst_cooldown = 0
        self.energy = 0
        self.burst_cost = 0
        self._init_attacks()
        self._init_elemental_skill()
        self._init_elemental_burst()
        self._init_aone()
        self._init_afour()
        self._activate_constallations()

        # State
        self.hp_level = 1
        self.is_shielded = False

    def _activate_constallations(self):
        pass

    def _set_general_info(self):
        pass

    def _activate_base_stats(self):
        """
        Activate base stats and ascesntion stat
        """
        pass

    def _init_attacks(self):
        pass

    def _init_elemental_skill(self):
        pass

    def _init_elemental_burst(self):
        pass

    def _init_aone(self):
        pass

    def _init_afour(self):
        pass

    def inflict_dmg(self, dmg):
        percent_decrease = dmg / self.total_hp
        self.hp_level = self.hp_level - percent_decrease

    def heal_hp(self, healing):
        percent_increase = healing / self.total_hp
        self.hp_level = self.hp_level + percent_increase

    def check_set_bonus(self):
        for key, value in self.set_bonus_counter.items():
            if value not in (2, 4):
                continue
            if self.set_bonus1 == None:
                self.set_bonus1 = key(value)
            else:
                if isinstance(self.set_bonus1, key):
                    continue
                self.set_bonus2 = key(value)

    def total_hp(self):
        return self.base_hp * (1 + self.hp_percent) + self.flat_hp

    def total_atk(self):
        return self.base_atk * (1 + self.atk_percent) + self.flat_atk

    def total_def(self):
        return self.base_def * (1 + self.def_percent) + self.flat_def

    def wait(self, n_seconds:float):
        pass

    def swap(self):
        pass

    def jump(self):
        pass

    def dash(self):
        pass

    def normal_attack(self, N=1):
        pass

    def charged_attack(self):
        pass

    def plunge_attack(self):
        pass

    def elemental_skill(self):
        pass

    def elemental_burst(self):
        pass

    def time_passes(self, seconds:float):
        self.skill_cooldown = max(0, self.skill_cooldown - seconds)
        self.burst_cooldown = max(0, self.burst_cooldown - seconds)
        self.stamina_icd = max(0, self.stamina_icd - seconds)
        if self.stamina_icd == 0:
            self.stamina = min(240, self.stamina + 25 * seconds)
        self.dash_icd[0] = max(0, self.dash_icd - seconds)
        if self.dash_icd[0] == 0:
            self.dash_icd = [0, True]

    def hitlag_extension(self, seconds:float):
        self.stamina_icd = max(1.5, self.stamina_icd + seconds)
        self.dash_icd[0] = max(0.8, self.dash_icd[0] + seconds)

    def notify(self, event):
        pass

    def set_team(self, team):
        self.team: List[Character] = team

    def set_enemies(self, enemies):
        self.enemies: List[Enemy] = enemies
