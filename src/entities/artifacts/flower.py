from src.entities.artifacts.artifact import Artifact, SetBonus

class Flower(Artifact):
    def __init__(self, set_bonus:SetBonus, flat_hp_rolls=0,
            flat_atk_rolls=0, flat_def_rolls=0, hp_percent_rolls=0,
            atk_percent_rolls=0, def_percent_rolls=0, er_rolls=0,
            em_rolls=0, cd_rolls=0, cr_rolls=0):
        super().__init__(set_bonus=set_bonus, main_flat_hp=4780, flat_hp_rolls=flat_hp_rolls,
            flat_atk_rolls=flat_atk_rolls, flat_def_rolls=flat_def_rolls, hp_percent_rolls=hp_percent_rolls,
            atk_percent_rolls=atk_percent_rolls, def_percent_rolls=def_percent_rolls, er_rolls=er_rolls,
            em_rolls=em_rolls, cd_rolls=cd_rolls, cr_rolls=cr_rolls)
        assert self.main_flat_hp > 0
        assert self.sub_flat_hp == 0