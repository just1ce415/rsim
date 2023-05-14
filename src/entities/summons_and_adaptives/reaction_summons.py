from src.entities.summons_and_adaptives.summon import Summon, Character
from src.entities.other.gauge_status import GaugeStatus
from src.constants import *

class DendroCore(Summon):
    def __init__(self):
        self.timer = 6
        self.timedout = False

        # Constant stats for environment
        self.special_multiplier = 2
        self.elemental_type = DENDRO

        self.hyperbloom_timer = 0

    def time_passes(self, seconds: float):
        if self.timedout:
            return
        if self.hyperbloom_timer == 0:
            self.timer -= seconds
            if self.timer <= 0:
                self.dmg_stats_ready = True
                self.timeout()
        else:
            self.hyperbloom_timer -= seconds
            if self.hyperbloom_timer <= 0:
                self.dmg_stats_ready = True
                self.timeout()

    def apply_element(self, element: str, gu: float):
        if element == PYRO:
            self.targets = [0, 1, 2, 3]
            self.reaction_multiplier = 3
            self.dmg_stats_ready = True
            self.timeout()
        elif element == ELECTRO:
            self.targets = [0]
            self.special_multiplier = 3
            self.hyperbloom_timer = 1
        else:
            return

    def timeout(self):
        self.timedout = True

    def set_summoner(self, summoner:Character):
        super().__init__(summoner)
        self.reaction_bonus = self.bloom_reaction_bonus

class ElectroCharged(Summon):
    def __init__(self, gauge_status:GaugeStatus):
        self.gauge_status = gauge_status
        self.timer = 1
        self.timedout = False

        # Constant stats for environment
        self.special_multiplier = 1.2
        self.elemental_type = ELECTRO

    def set_summoner(self, summoner:Character):
        super().__init__(summoner)
        self.reaction_bonus = self.electro_charged_reaction_bonus

    def time_passes(self, seconds: float):
        self.dmg_stats_ready = False
        if self.gauge_status.current_auras[ELECTRO] == [0, 0] or self.gauge_status.current_auras[HYDRO] == [0, 0]:
            self.timeout()
            return
        self.timer -= seconds
        if self.timer <= 0:
            self.gauge_status.current_auras[ELECTRO][0] -= 0.4
            self.gauge_status.current_auras[HYDRO][0] -= 0.4
            self.dmg_stats_ready = True
            if self.gauge_status.current_auras[ELECTRO][0] <= 0:
                self.gauge_status.current_auras[ELECTRO] = [0, 0]
            if self.gauge_status.current_auras[HYDRO][0] <= 0:
                self.gauge_status.current_auras[HYDRO] = [0, 0]
            self.timer = 1

    def hitlag_extension(self, seconds: float):
        self.timer += seconds

    def timeout(self):
        self.timedout = True

class Burning(Summon):
    def __init__(self, gauge_status:GaugeStatus):
        self.gauge_status = gauge_status
        self.tik_timer = 0.25
        self.pyro_app_icd = 2
        self.timedout = False

        # Stats for environment
        self.special_multiplier = 0.25
        self.elemental_type = PYRO

    def set_summoner(self, summoner:Character):
        super().__init__(summoner)
        self.reaction_bonus = self.burning_reaction_bonus

    def time_passes(self, seconds: float):
        self.dmg_stats_ready = False
        if not ((self.gauge_status.current_auras[DENDRO] != [0, 0] or
            self.gauge_status.current_auras[QUICKEN] != [0, 0]) and self.gauge_status.current_auras[BURNING] != [0, 0]):
            self.timeout()
            return
        self.pyro_app_icd -= seconds
        self.tik_timer -= seconds
        if self.tik_timer <= 0:
            # Consumes both dendro and quicken simulataneoaly
            if self.gauge_status.current_auras[DENDRO][0] != 0:
                self.gauge_status.current_auras[DENDRO][0] -= 0.1
                if self.gauge_status.current_auras[DENDRO][0] <= 0:
                    self.gauge_status.current_auras[DENDRO] = [0, 0]

            if self.gauge_status.current_auras[QUICKEN][0] != 0:
                self.gauge_status.current_auras[QUICKEN][0] -= 0.1
                if self.gauge_status.current_auras[QUICKEN][0] <= 0:
                    self.gauge_status.current_auras[QUICKEN] = [0, 0]
            self.dmg_stats_ready = True
            self.tik_timer = 0.25
        if self.pyro_app_icd <= 0:
            self.gauge_status.current_auras[PYRO] = [1, 1 / (35/4 + 25/8)]
            self.pyro_app_icd = 2

    def hitlag_extension(self, seconds: float):
        self.pyro_app_icd += seconds
        self.tik_timer += seconds

    def timeout(self):
        self.timedout = True