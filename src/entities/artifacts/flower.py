from src.entities.artifacts.artifact import Artifact
from src.entities.characters.character import Character

class Flower(Artifact):
    def __init__(self, set_bonus,
            flat_atk_rolls=0, flat_def_rolls=0, hp_percent_rolls=0,
            atk_percent_rolls=0, def_percent_rolls=0, er_rolls=0,
            em_rolls=0, cd_rolls=0, cr_rolls=0):
        super().__init__(set_bonus=set_bonus, main_flat_hp=4780,
            flat_atk_rolls=flat_atk_rolls, flat_def_rolls=flat_def_rolls, hp_percent_rolls=hp_percent_rolls,
            atk_percent_rolls=atk_percent_rolls, def_percent_rolls=def_percent_rolls, er_rolls=er_rolls,
            em_rolls=em_rolls, cd_rolls=cd_rolls, cr_rolls=cr_rolls)
        assert self.main_flat_hp > 0
        assert self.sub_flat_hp == 0

    def equip(self, holder:Character):
        self.set_holder(holder)
        assert self.holder.flower is None
        self.holder.flower = self
        self.holder.flat_hp += self.main_flat_hp
        self.holder.flat_atk += self.sub_flat_atk
        self.holder.flat_def += self.sub_flat_def
        self.holder.hp_percent += self.sub_hp_percent
        self.holder.atk_percent += self.sub_atk_percent
        self.holder.def_percent += self.sub_def_percent
        self.holder.er += self.sub_er
        self.holder.em += self.sub_em
        self.holder.all_cd += self.sub_cd
        self.holder.all_cr += self.sub_cr
        self.holder.set_bonus_counter[self.set_bonus] = self.holder.set_bonus_counter.get(self.set_bonus, 0) + 1
        self.holder.check_set_bonus()
