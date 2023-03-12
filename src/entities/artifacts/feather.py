from src.entities.artifacts.artifact import Artifact
from src.entities.artifacts.sets.set_bonus import SetBonus

class Feather(Artifact):
    def __init__(self, set_bonus:SetBonus):
        super().__init__(self, set_bonus=set_bonus, main_flat_atk=311)
        assert self.main_flat_atk > 0
        assert self.sub_flat_atk == 0