from src.entities.characters.character import Character, Entity
from src.entities.other.gauge_status import GaugeStatus
from src.constants import *

class Weapon(Entity):
    def __init__(self, level=90, refinement=0):
        # General info
        self.holder = None
        self.type = NONE
        self.level = level
        self.refinement = refinement
        self._activate_general_info()
        if self.type in (SWORD, POLEARM, CLAYMORE):
            self.gauge_status = GaugeStatus()
        else:
            self.gauge_status = None

        # Stats
        self.base = 0
        self.atk_percent = 0
        self.cd = 0
        self.cr = 0
        self.er = 0
        self.em = 0
        self.hp_percent = 0
        self.def_percent = 0
        self.phys_dmg_bonus = 0
        self._activate_stats()
        self._activate_passive()
        self._activate_refinement()

    def set_holder(self, holder:Character):
        self.holder = holder

    def _activate_permanent_passive(self):
        pass

    def _activate_general_info(self):
        pass

    def _activate_refinement(self):
        pass

    def _activate_stats(self):
        """
        Activate base and substat
        """
        pass

    def _activate_passive(self):
        pass

    def time_passes(self, seconds: float):
        pass

    def hitlag_extension(self, seconds: float):
        pass

    def equip(self, character:Character):
        self.set_holder(character)
        self.holder.weapon = self
        self.holder.base_atk += self.base
        self.holder.atk_percent += self.atk_percent
        self.holder.all_cd += self.cd
        self.holder.all_cr += self.cr
        self.holder.er += self.er
        self.holder.em += self.em
        self.holder.phys_dmg_bonus += self.phys_dmg_bonus
        self.holder.hp_percent += self.hp_percent
        self.holder.def_percent += self.def_percent
        self.holder.weapon._activate_permanent_passive()
        if self.holder.weapon_type != self.type:
            print("[WARNING] Equipped weapon with invalid type.")