from src.entities.entity import Entity
from src.constants import *

class Weapon(Entity):
    def __init__(self, holder, level=90, refinement=0):
        # General info
        self.holder = holder
        self.type = NONE
        self.level = level
        self.refinement = refinement

        # Stats
        self.base = 0
        self.atk_percent = 0
        self.cd = 0
        self.cr = 0
        self.er = 0
        self.em = 0
        self.phys_dmg_bonus = 0
        self.hp_percent = 0
        self.def_percent = 0
        self._activate_stats()
        self._activate_passive()
        self._activate_refinement()


    def _activate_refinement():
        pass

    def _activate_stats():
        """
        Activate base and substat
        """
        pass

    def _activate_passive():
        pass