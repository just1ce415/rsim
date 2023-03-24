from src.entities.artifacts.set_bonus import SetBonus
from src.constants import *

from random import choice

class Artifact:
    def __init__(
            self, set_bonus:SetBonus, main_flat_hp=0, main_flat_atk=0, main_atk_percent=0,
            main_hp_percent=0, main_def_percent=0, main_er=0, main_em=0, main_anemo_dmg_bonus=0,
            main_hydro_dmg_bonus=0, main_electro_dmg_bonus=0, main_dendro_dmg_bonus=0,
            main_cryo_dmg_bonus=0, main_pyro_dmg_bonus=0, main_geo_dmg_bonus=0,
            main_phys_dmg_bonus=0, main_cd=0, main_cr=0, main_hb=0, flat_hp_rolls=0,
            flat_atk_rolls=0, flat_def_rolls=0, hp_percent_rolls=0,
            atk_percent_rolls=0, def_percent_rolls=0, er_rolls=0,
            em_rolls=0, cd_rolls=0, cr_rolls=0
        ):
        self.holder = None
        self.set_bonus = set_bonus

        self.main_flat_hp = main_flat_hp
        self.main_flat_atk = main_flat_atk
        self.main_atk_percent = main_atk_percent
        self.main_hp_percent = main_hp_percent
        self.main_def_percent = main_def_percent
        self.main_er = main_er
        self.main_em = main_em
        self.main_anemo_dmg_bonus = main_anemo_dmg_bonus
        self.main_hydro_dmg_bonus= main_hydro_dmg_bonus
        self.main_electro_dmg_bonus = main_electro_dmg_bonus
        self.main_dendro_dmg_bonus = main_dendro_dmg_bonus
        self.main_cryo_dmg_bonus = main_cryo_dmg_bonus
        self.main_pyro_dmg_bonus = main_pyro_dmg_bonus
        self.main_geo_dmg_bonus = main_geo_dmg_bonus
        self.main_phys_dmg_bonus = main_phys_dmg_bonus
        self.main_cd = main_cd
        self.main_cr = main_cr
        self.main_hb = main_hb

        assert (flat_hp_rolls + flat_atk_rolls + flat_def_rolls + hp_percent_rolls +
            atk_percent_rolls + def_percent_rolls + er_rolls + em_rolls + 
            cd_rolls + cr_rolls <= MAX_ROLLS
            )

        possible_rolls = [1, 0.9, 0.8, 0.7]
        self.sub_flat_hp = flat_hp_rolls * FLAT_HP_ROLL * choice(possible_rolls)
        self.sub_flat_atk = flat_atk_rolls * FLAT_ATK_ROLL * choice(possible_rolls)
        self.sub_flat_def = flat_def_rolls * FLAT_DEF_ROLL * choice(possible_rolls)
        self.sub_hp_percent = hp_percent_rolls * HP_PERSENT_ROLL * choice(possible_rolls)
        self.sub_atk_percent = atk_percent_rolls * ATK_PERCENT_ROLL * choice(possible_rolls)
        self.sub_def_percent = def_percent_rolls * DEF_PERCENT_ROLL * choice(possible_rolls)
        self.sub_er = er_rolls * ER_ROLL * choice(possible_rolls)
        self.sub_em = em_rolls * EM_ROLL * choice(possible_rolls)
        self.sub_cd = cd_rolls * CD_ROLL * choice(possible_rolls)
        self.sub_cr = cr_rolls * CR_ROLL * choice(possible_rolls)

    def __str__(self):
        if self.main_flat_hp:
            main_stat = "HP"
            main_stat_value = self.main_flat_hp
        elif self.main_flat_atk:
            main_stat = "ATK"
            main_stat_value = self.main_flat_atk
        elif self.main_atk_percent:
            main_stat = "ATK%"
            main_stat_value = self.main_atk_percent
        elif self.main_hp_percent:
            main_stat = "HP%"
            main_stat_value = self.main_hp_percent
        elif self.main_def_percent:
            main_stat = "DEF%"
            main_stat_value = self.main_def_percent
        elif self.main_er:
            main_stat = "Energy Recharge"
            main_stat_value = self.main_er
        elif self.main_em:
            main_stat = "Elemental Mastery"
            main_stat_value = self.main_em
        elif self.main_anemo_dmg_bonus:
            main_stat = "Anemo Dmg Bonus"
            main_stat_value = self.main_anemo_dmg_bonus
        elif self.main_hydro_dmg_bonus:
            main_stat = "Hydro Dmg Bonus"
            main_stat_value = self.main_hydro_dmg_bonus
        elif self.main_electro_dmg_bonus:
            main_stat = "Electro Dmg Bonus"
            main_stat_value = self.main_electro_dmg_bonus
        elif self.main_dendro_dmg_bonus:
            main_stat = "Dendro Dmg Bonus"
            main_stat_value = self.main_dendro_dmg_bonus
        elif self.main_cryo_dmg_bonus:
            main_stat = "Cryo Dmg Bonus"
            main_stat_value = self.main_cryo_dmg_bonus
        elif self.main_pyro_dmg_bonus:
            main_stat = "Pyro Dmg Bonus"
            main_stat_value = self.main_pyro_dmg_bonus
        elif self.main_geo_dmg_bonus:
            main_stat = "Geo Dmg Bonus"
            main_stat_value = self.main_geo_dmg_bonus
        elif self.main_phys_dmg_bonus:
            main_stat = "Phys dmg Bonus"
            main_stat_value = self.main_phys_dmg_bonus
        elif self.main_cd:
            main_stat = "CRIT DMG"
            main_stat_value = self.main_cd
        elif self.main_cr:
            main_stat = "CRIT Rate"
            main_stat_value = self.main_cr
        elif self.main_hb:
            main_stat = "Healing Bonus"
            main_stat_value = self.main_hb

        sub1_val = 0
        sub2_val = 0
        sub3_val = 0
        sub4_val = 0
        sub1 = None
        sub2 = None
        sub3 = None
        sub4 = None
        if self.sub_flat_hp:
            sub1_val = self.sub_flat_hp
            sub1 = "HP"
        if self.sub_flat_atk:
            if sub1_val:
                sub2_val = self.sub_flat_atk
                sub2 = "ATK"
            else:
                sub1_val = self.sub_flat_atk
                sub1 = "ATK"
        if self.sub_flat_def:
            if sub2_val:
                sub3_val = self.sub_flat_def
                sub3 = "DEF"
            elif sub1_val:
                sub2_val = self.sub_flat_def
                sub2 = "DEF"
            else:
                sub1_val = self.sub_flat_def
                sub1 = "DEF"
        if self.sub_atk_percent:
            if sub3_val:
                sub4_val = self.sub_atk_percent
                sub4 = "ATK%"
            elif sub2_val:
                sub3_val = self.sub_atk_percent
                sub3 = "ATK%"
            elif sub1_val:
                sub2_val = self.sub_atk_percent
                sub2 = "ATK%"
            else:
                sub1_val = self.sub_atk_percent
                sub1 = "ATK%"
        if self.sub_hp_percent:
            if sub3_val:
                sub4_val = self.sub_hp_percent
                sub4 = "HP%"
            elif sub2_val:
                sub3_val = self.sub_hp_percent
                sub3 = "HP%"
            elif sub1_val:
                sub2_val = self.sub_hp_percent
                sub2 = "HP%"
            else:
                sub1_val = self.sub_hp_percent
                sub1 = "HP%"
        if self.sub_def_percent:
            if sub3_val:
                sub4_val = self.sub_def_percent
                sub4 = "DEF%"
            elif sub2_val:
                sub3_val = self.sub_def_percent
                sub3 = "DEF%"
            elif sub1_val:
                sub2_val = self.sub_def_percent
                sub2 = "DEF%"
            else:
                sub1_val = self.sub_def_percent
                sub1 = "DEF%"
        if self.sub_er:
            if sub3_val:
                sub4_val = self.sub_er
                sub4 = "Energy Recharge"
            elif sub2_val:
                sub3_val = self.sub_er
                sub3 = "Energy Recharge"
            elif sub1_val:
                sub2_val = self.sub_er
                sub2 = "Energy Recharge"
            else:
                sub1_val = self.sub_er
                sub1 = "Energy Recharge"
        if self.sub_em:
            if sub3_val:
                sub4_val = self.sub_em
                sub4 = "Elemental Mastery"
            elif sub2_val:
                sub3_val = self.sub_em
                sub3 = "Elemental Mastery"
            elif sub1_val:
                sub2_val = self.sub_em
                sub2 = "Elemental Mastery"
            else:
                sub1_val = self.sub_em
                sub1 = "Elemental Mastery"
        if self.sub_cd:
            if sub3_val:
                sub4_val = self.sub_cd
                sub4 = "CRIT DMG"
            elif sub2_val:
                sub3_val = self.sub_cd
                sub3 = "CRIT DMG"
            elif sub1_val:
                sub2_val = self.sub_cd
                sub2 = "CRIT DMG"
            else:
                sub1_val = self.sub_cd
                sub1 = "CRIT DMG"
        if self.sub_cr:
            if sub3_val:
                sub4_val = self.sub_cr
                sub4 = "CRIT Rate"
            elif sub2_val:
                sub3_val = self.sub_cr
                sub3 = "CRIT Rate"
            elif sub1_val:
                sub2_val = self.sub_cr
                sub2 = "CRIT Rate"
            else:
                sub1_val = self.sub_cr
                sub1 = "CRIT Rate"

        return "{}\nMain stat:\n{}: {}\nSubstats:\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n".format(
            self.__class__.__name__, main_stat, main_stat_value, sub1, sub1_val, sub2, sub2_val, sub3,
            sub3_val, sub4, sub4_val
        )