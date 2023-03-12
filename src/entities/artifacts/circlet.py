from src.entities.artifacts.artifact import Artifact
from src.entities.artifacts.sets.set_bonus import SetBonus

class Circlet(Artifact):
    def __init__(
            self, set_bonus:SetBonus, main_atk_percent=False,
            main_hp_percent=False, main_def_percent=False, main_em=False,
            main_cd=False, main_cr=False, main_hb=False
        ):
        super().__init__(
            self, set_bonus=set_bonus, main_atk_percent=int(main_atk_percent)*0.466,
            main_hp_percent=int(main_hp_percent)*0.466, main_def_percent=int(main_def_percent)*0.466,
            main_em=int(main_em)*186.5, main_cd=int(main_cd)*0.622,
            main_cr=int(main_cr)*0.311, main_hb=int(main_hb)*0.359
        )
        assert (
            self.main_atk_percent > 0 or self.main_hp_percent > 0 or 
            self.main_def_percent > 0 or self.main_em > 0 or
            self.main_cd > 0 or self.main_cr > 0 or
            self.main_hb > 0
        )