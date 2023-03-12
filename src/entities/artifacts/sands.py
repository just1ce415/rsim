from src.entities.artifacts.artifact import Artifact
from src.entities.artifacts.sets.set_bonus import SetBonus

class Sands(Artifact):
    def __init__(
            self, set_bonus:SetBonus, main_hp_percent=False, main_atk_percent=False,
            main_def_percent=False, main_er=False, main_em=False
        ):
        super().__init__(
            self, set_bonus=set_bonus, main_hp_percent=int(main_hp_percent)*0.466,
            main_atk_percent=int(main_atk_percent)*0.466, main_def_percent=int(main_def_percent)*0.583,
            main_er=int(main_er)*0.518, main_em=int(main_em)*186.5
            )
        assert (
            self.main_atk_percent > 0 or self.main_hp_percent > 0 or 
            self.main_def_percent > 0 or self.main_er > 0 or
            self.main_em > 0
        )