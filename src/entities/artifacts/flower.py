from src.entities.artifacts.artifact import Artifact
from src.entities.artifacts.sets.set_bonus import SetBonus

class Flower(Artifact):
    def __init__(self, set_bonus:SetBonus):
        super().__init__(self, set_bonus=set_bonus, main_flat_hp=4780)
        assert self.main_flat_hp > 0
        assert self.sub_flat_hp == 0