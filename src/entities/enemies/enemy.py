# BATCHEST
from src.entities.entity import Entity
from src.entities.other.gauge_status import GaugeStatus
from src.constants import *

from typing import Dict

class Enemy(Entity):
    def __init__(self, level:int=100,
    resistance:Dict[str, float]={PHYS: 0.1, ANEMO: 0.1, HYDRO: 0.1, ELECTRO: 0.1, DENDRO: 0.1, CRYO: 0.1, PYRO: 0.1, GEO: 0.1}):
        self.level = level
        self.resistance = resistance
        self.gauge_status = GaugeStatus()
        self.def_shred = 0
        self.def_ignore = 0