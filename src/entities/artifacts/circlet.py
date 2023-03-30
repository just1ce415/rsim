from src.entities.artifacts.artifact import Artifact
from src.entities.characters.character import Character
from src.constants import *

class Circlet(Artifact):
    def __init__(
            self, set_bonus, main_atk_percent=False,
            main_hp_percent=False, main_def_percent=False, main_em=False,
            main_cd=False, main_cr=False, main_hb=False, flat_hp_rolls=0,
            flat_atk_rolls=0, flat_def_rolls=0, hp_percent_rolls=0,
            atk_percent_rolls=0, def_percent_rolls=0, er_rolls=0,
            em_rolls=0, cd_rolls=0, cr_rolls=0
        ):
        super().__init__(
            set_bonus=set_bonus, main_atk_percent=int(main_atk_percent)*0.466,
            main_hp_percent=int(main_hp_percent)*0.466, main_def_percent=int(main_def_percent)*0.466,
            main_em=int(main_em)*186.5, main_cd=int(main_cd)*0.622,
            main_cr=int(main_cr)*0.311, main_hb=int(main_hb)*0.359, flat_hp_rolls=flat_hp_rolls,
            flat_atk_rolls=flat_atk_rolls, flat_def_rolls=flat_def_rolls, hp_percent_rolls=hp_percent_rolls,
            atk_percent_rolls=atk_percent_rolls, def_percent_rolls=def_percent_rolls, er_rolls=er_rolls,
            em_rolls=em_rolls, cd_rolls=cd_rolls, cr_rolls=cr_rolls

        )
        assert (
            self.main_atk_percent > 0 or self.main_hp_percent > 0 or 
            self.main_def_percent > 0 or self.main_em > 0 or
            self.main_cd > 0 or self.main_cr > 0 or
            self.main_hb > 0
        )

    def equip(self, holder:Character):
        self.set_holder(holder)
        assert self.circlet is None
        self.holder.circlet = self
        self.holder.flat_hp += self.sub_flat_hp
        self.holder.flat_atk += self.sub_flat_atk
        self.holder.flat_def += self.sub_flat_def
        self.holder.hp_percent += self.sub_hp_percent if self.main_hp_percent == 0.0 else self.main_hp_percent
        self.holder.atk_percent += self.sub_atk_percent if self.main_atk_percent == 0.0 else self.main_atk_percent
        self.holder.def_percent += self.sub_def_percent if self.main_def_percent == 0.0 else self.main_def_percent
        self.holder.er += self.sub_er
        self.holder.em += self.sub_em + self.main_em
        self.holder.all_cd += self.sub_cd if self.main_cd == 0.0 else self.main_cd
        self.holder.all_cr += self.sub_cr if self.main_cr == 0.0 else self.main_cr
        self.holder.set_bonus_counter[self.set_bonus] = self.holder.set_bonus_counter.get(self.set_bonus, 0) + 1
        self.holder.check_set_bonus()
