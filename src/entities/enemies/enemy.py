# BATCHEST
from src.entities.entity import Entity
from src.entities.other.gauge_status import GaugeStatus

from typing import Dict

class Enemy(Entity):
    def __init__(self, level:int, resistance:Dict[str:float]):
        self.level = level
        self.resistance = resistance
        self.gauge_status = GaugeStatus()