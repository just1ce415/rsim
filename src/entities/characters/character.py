from src.entities.entity import Entity
from src.constants import *

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

        self.swirl_reaction_bonus = 0
        self.bloom_reaction_bonus = 0
        self.burgeon_reaction_bonus = 0
        self.hyperbloom_reaction_bonus = 0
        self.aggravate_reaction_bonus = 0
        self.spread_reaction_bonus = 0
        self.overload_reaction_bonus = 0
        self.superconduct_reaction_bonus = 0
        self.electro_charged_reaction_bonus = 0
        self.burning_reaction_bonus = 0
        self.vaporize_reaction_bonus = 0
        self.melt_reaction_bonus = 0
        # Potentially add shatter

        self.anemo_dmg_bonus = 0
        self.hydro_dmg_bonus = 0
        self.electro_dmg_bonus = 0
        self.dendro_dmg_bonus = 0
        self.cryo_dmg_bonus = 0
        self.pyro_dmg_bonus = 0
        self.geo_dmg_bonus = 0
        self.phys_dmg_bonus = 0
        self.na_dmg_bonus = 0
        self.ca_dmg_bonus = 0
        self.pa_dmg_bonus = 0
        self.skill_dmg_bonus = 0
        self.burst_dmg_bonus = 0
        self.all_dmg_bonus = 0

        self.crit_ratio = crit_ratio
        self.all_cd = 0.5
        self.all_cr = 0.05
        self.anemo_cd = 0
        self.hydro_cd = 0
        self.electro_cd = 0
        self.dendro_cd = 0
        self.cryo_cd = 0
        self.pyro_cd = 0
        self.geo_cd = 0
        self.phys_cd = 0
        self.na_cd = 0
        self.ca_cd = 0
        self.pa_cd = 0
        self.skill_cd = 0
        self.burst_cd = 0
        self.anemo_cr = 0
        self.hydro_cr = 0
        self.electro_cr = 0
        self.dendro_cr = 0
        self.cryo_cr = 0
        self.pyro_cr = 0
        self.geo_cr = 0
        self.phys_cr = 0
        self.na_cr = 0
        self.ca_cr = 0
        self.pa_cr = 0
        self.skill_cr = 0
        self.burst_cr = 0

        self.healing_bonus = 0
        self.healing_received = 0
        self.shield_strength = 0

        # Skills general info
        self.skill_cd = 0
        self.burst_cd = 0
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
        self.skill_cd = max(0, self.skill_cd - seconds)
        self.burst_cd = max(0, self.burst_cd - seconds)

    def hitlag_extension(self, seconds:float):
        pass

    def notify(self, event):
        pass

    def set_team(self, team):
        self.team = team

    def set_enemies(self, enemies):
        self.enemies = enemies
