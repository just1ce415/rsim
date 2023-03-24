from src.entities.entity import Entity
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

    def activate_permanent_passive(self):
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