from src.entities.artifacts.artifact import Artifact, SetBonus

class Sands(Artifact):
    def __init__(
            self, set_bonus:SetBonus, main_hp_percent=False, main_atk_percent=False,
            main_def_percent=False, main_er=False, main_em=False, flat_hp_rolls=0,
            flat_atk_rolls=0, flat_def_rolls=0, hp_percent_rolls=0,
            atk_percent_rolls=0, def_percent_rolls=0, er_rolls=0,
            em_rolls=0, cd_rolls=0, cr_rolls=0
        ):
        super().__init__(
            set_bonus=set_bonus, main_hp_percent=int(main_hp_percent)*0.466, main_atk_percent=int(main_atk_percent)*0.466,
            main_def_percent=int(main_def_percent)*0.583, main_er=int(main_er)*0.518, main_em=int(main_em)*186.5,
            flat_hp_rolls=flat_hp_rolls, flat_atk_rolls=flat_atk_rolls, flat_def_rolls=flat_def_rolls,
            hp_percent_rolls=hp_percent_rolls, atk_percent_rolls=atk_percent_rolls, def_percent_rolls=def_percent_rolls,
            er_rolls=er_rolls, em_rolls=em_rolls, cd_rolls=cd_rolls, cr_rolls=cr_rolls
            )
        assert (
            self.main_atk_percent > 0 or self.main_hp_percent > 0 or 
            self.main_def_percent > 0 or self.main_er > 0 or
            self.main_em > 0
        )