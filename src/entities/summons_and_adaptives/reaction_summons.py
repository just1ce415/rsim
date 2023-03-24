from src.entities.summons_and_adaptives.summon import Summon, Entity, Character
from src.entities.other.gauge_status import GaugeStatus

class DendroCore(Summon):
    pass

class ElectroCharged(Summon):
    def __init__(self, gauge_status:GaugeStatus):
        self.gauge_status = gauge_status

    def set_summoner(self, summoner:Character):
        super().__init__(summoner)

class Burning(Summon):
    def __init__(self, gauge_status:GaugeStatus):
        self.gauge_status = gauge_status

    def set_summoner(self, summoner:Character):
        super().__init__(summoner)