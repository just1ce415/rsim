
class Artifact:
    def __init__(
            self, set_bonus, main_flat_hp=0, main_flat_atk=0, main_atk_percent=0,
            main_hp_percent=0, main_def_percent=0, main_er=0, main_em=0, main_anemo_dmg_bonus=0,
            main_hydro_dmg_bonus=0, main_electro_dmg_bonus=0, main_dendro_dmg_bonus=0,
            main_cryo_dmg_bonus=0, main_pyro_dmg_bonus=0, main_geo_dmg_bonus=0,
            main_phys_dmg_bonus=0, main_cd=0, main_cr=0, main_hb=0
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

        self.sub_flat_hp = 0
        self.sub_flat_atk = 0
        self.sub_flat_def = 0
        self.sub_atk_percent = 0
        self.sub_hp_percent = 0
        self.sub_def_percent = 0
        self.sub_er = 0
        self.sub_em = 0
        self.sub_cd = 0
        self.sub_cr = 0
