from src.entities.artifacts.flower import Flower
from src.entities.artifacts.feather import Feather
from src.entities.artifacts.sands import Sands
from src.entities.artifacts.goblet import Goblet
from src.entities.artifacts.circlet import Circlet

from typing import Dict

class ArtifactGenerator:
    def __init__(self):
        self.flat_hp_roll = 298.75
        self.flat_atk_roll = 19.45
        self.flat_def_roll = 23.15
        self.hp_persent_roll = 0.0583
        self.atk_percent_roll = 0.0583
        self.def_percent_roll = 0.0729
        self.em_roll = 23.31
        self.er_roll = 0.0648
        self.cd_roll = 0.0777
        self.cr_roll = 0.0389

    def generate_substats_by_stat_value(
            self, stat_value:float, dmg_info:Dict, er_info:Dict,
            flower:Flower, feather:Feather, sands:Sands, goblet:Goblet, circlet:Circlet,
            target_er_from_arts:float=0
        ):
        """
        Sets of stats with the same stat value lead to (approximately) the same DPR.
        This dependency is linear.
        :params:
        stat_value - a float value between 0 and 100, where zero corresponds to DPR
        without substats and hundred corresponds to maximum possible DPR with substats
        (maximum substats 5(pieces) * (4+5)(substats each) = 45);
        dmg_info - dmg_info of holder (check structure src/data.json)
        er_info - er_info of holder (check structure src/data.json)
        """
        pass