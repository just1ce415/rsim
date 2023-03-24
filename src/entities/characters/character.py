from src.entities.entity import Entity
from src.entities.weapons.weapon import Weapon
from src.entities.artifacts.flower import Flower
from src.entities.artifacts.feather import Feather
from src.entities.artifacts.sands import Sands
from src.entities.artifacts.goblet import Goblet
from src.entities.artifacts.circlet import Circlet
from src.constants import *

class Character(Entity):
    def __init__(
            self, level=90, talent_lvls=(9, 9, 9), constallation=0
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
        self.__set_bonus_count = {}
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

        self.cd = 0.5
        self.cr = 0.05
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

        # Skills general info
        self.skill_cd = 0
        # Tuple [chance to generate, respective amount]
        self.particle_generation = [(1/3, 1), (2/3, 2)]
        self.burst_cd = 0
        self.energy = 0
        self.burst_cost = 0
        self._init_attacks()
        self._init_elemental_skill()
        self._init_elemental_burst()
        self._init_aone()
        self._init_afour()
        self._activate_constallations()

        self.hp_level = 1

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

    def equip_weapon(self, weapon:Weapon):
        self.weapon = weapon
        self.weapon.holder = self
        self.base_atk += self.weapon.base
        self.atk_percent += self.weapon.atk_percent
        self.cd = self.weapon.cd
        self.cr = self.weapon.cr
        self.er = self.weapon.er
        self.em = self.weapon.em
        self.phys_dmg_bonus = self.weapon.phys_dmg_bonus
        self.hp_percent = self.weapon.hp_percent
        self.def_percent = self.weapon.def_percent
        self.weapon.activate_permanent_passive()
        if self.weapon_type != self.weapon.type:
            print("[WARNING] Equipped weapon with invalid type.")

    def __check_set_bonus(self):
        for key, value in self.__set_bonus_count.items():
            if value not in (2, 4):
                continue
            if self.set_bonus1 == None:
                self.set_bonus1 = key(value)
            else:
                if isinstance(self.set_bonus1, key):
                    continue
                self.set_bonus2 = key(value)

    def equip_flower(self, flower:Flower):
        assert self.flower is None
        self.flower = flower
        self.flower.holder = self
        self.flat_hp = self.flower.main_flat_hp
        self.flat_atk = self.flower.sub_flat_atk
        self.flat_def = self.flower.sub_flat_def
        self.hp_percent = self.flower.sub_hp_percent
        self.atk_percent = self.flower.sub_atk_percent
        self.def_percent = self.flower.sub_def_percent
        self.er = self.flower.sub_er
        self.em = self.flower.sub_em
        self.cd = self.feather.sub_cd
        self.cr = self.feather.sub_cr
        self.__set_bonus_count[self.flower.set_bonus] = self.__set_bonus_count.get(self.flower.set_bonus, 0) + 1
        self.__check_set_bonus()

    def equip_feather(self, feather:Feather):
        assert self.feather is None
        self.feather = feather
        self.feather.holder = self
        self.flat_hp = self.feather.sub_flat_hp
        self.flat_atk = self.feather.main_flat_atk
        self.flat_def = self.feather.sub_flat_def
        self.hp_percent = self.feather.sub_hp_percent
        self.atk_percent = self.flower.sub_atk_percent
        self.def_percent = self.sands.sub_def_percent
        self.er = self.feather.sub_er
        self.em = self.feather.sub_em
        self.cd = self.feather.sub_cd
        self.cr = self.feather.sub_cr
        self.__set_bonus_count[self.feather.set_bonus] = self.__set_bonus_count.get(self.feather.set_bonus, 0) + 1
        self.__check_set_bonus()

    def equip_sands(self, sands:Sands):
        assert self.sands is None
        self.sands = sands
        self.sands.holder = self
        self.flat_hp = self.sands.sub_flat_hp
        self.flat_atk = self.sands.sub_flat_atk
        self.flat_def = self.sands.sub_flat_def
        self.hp_percent = self.goblet.sub_hp_percent + self.sands.main_hp_percent
        self.atk_percent = self.goblet.sub_atk_percent + self.sands.main_atk_percent
        self.def_percent = self.goblet.sub_def_percent + self.sands.main_def_percent
        self.er = self.sands.sub_er + self.sands.main_er
        self.em = self.sands.sub_em + self.sands.main_em
        self.cd = self.sands.sub_cd
        self.cr = self.sands.sub_cr
        self.__set_bonus_count[self.sands.set_bonus] = self.__set_bonus_count.get(self.sands.set_bonus, 0) + 1
        self.__check_set_bonus()

    def equip_goblet(self, goblet:Goblet):
        assert self.goblet is None
        self.goblet = goblet
        self.goblet.holder = self
        self.anemo_dmg_bonus = self.goblet.main_anemo_dmg_bonus
        self.hydro_dmg_bonus = self.goblet.main_hydro_dmg_bonus
        self.electro_dmg_bonus = self.goblet.main_electro_dmg_bonus
        self.dendro_dmg_bonus = self.goblet.main_dendro_dmg_bonus
        self.cryo_dmg_bonus = self.goblet.main_cryo_dmg_bonus
        self.pyro_dmg_bonus = self.goblet.main_pyro_dmg_bonus
        self.geo_dmg_bonus = self.goblet.main_geo_dmg_bonus
        self.phys_dmg_bonus = self.goblet.main_phys_dmg_bonus
        self.flat_hp = self.goblet.sub_flat_hp
        self.flat_atk = self.goblet.sub_flat_atk
        self.flat_def = self.goblet.sub_flat_def
        self.hp_percent = self.circlet.sub_hp_percent + self.goblet.main_hp_percent
        self.atk_percent = self.circlet.sub_atk_percent + self.goblet.main_atk_percent
        self.def_percent = self.circlet.sub_def_percent + self.goblet.main_def_percent
        self.er = self.goblet.sub_er
        self.em = self.goblet.sub_em + self.goblet.main_em
        self.cd = self.goblet.sub_cd
        self.cr = self.goblet.sub_cr
        self.__set_bonus_count[self.goblet.set_bonus] = self.__set_bonus_count.get(self.goblet.set_bonus, 0) + 1
        self.__check_set_bonus()

    def equip_circlet(self, circlet:Circlet):
        assert self.circlet is None
        self.circlet = circlet
        self.circlet.holder = self
        self.flat_hp = self.circlet.sub_flat_hp
        self.flat_atk = self.circlet.sub_flat_atk
        self.flat_def = self.circlet.sub_flat_def
        self.hp_percent = self.flower.sub_hp_percent + self.circlet.main_hp_percent
        self.atk_percent = self.flower.sub_atk_percent + self.circlet.main_atk_percent
        self.def_percent = self.flower.sub_def_percent + self.circlet.main_def_percent
        self.er = self.circlet.sub_er
        self.em = self.circlet.sub_em + self.circlet.main_em
        self.cd = self.circlet.sub_cd + self.circlet.main_cd
        self.cr = self.circlet.sub_cr + self.circlet.main_cr
        self.__set_bonus_count[self.circlet.set_bonus] = self.__set_bonus_count.get(self.circlet.set_bonus, 0) + 1
        self.__check_set_bonus()

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
        self.skill_cd -= seconds
        self.burst_cd -= seconds

    def hitlag_extension(self, seconds:float):
        pass

    def notify(self, event):
        pass

    def set_env(self, env):
        self.env = env
