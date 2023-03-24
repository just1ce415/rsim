from src.entities.artifacts.artifact import Artifact, SetBonus

class Goblet(Artifact):
    def __init__(self, set_bonus:SetBonus, main_atk_percent=0,
            main_hp_percent=False, main_def_percent=False, main_em=False, main_anemo_dmg_bonus=False,
            main_hydro_dmg_bonus=False, main_electro_dmg_bonus=False, main_dendro_dmg_bonus=False,
            main_cryo_dmg_bonus=False, main_pyro_dmg_bonus=False, main_geo_dmg_bonus=False,
            main_phys_dmg_bonus=False, flat_hp_rolls=0,
            flat_atk_rolls=0, flat_def_rolls=0, hp_percent_rolls=0,
            atk_percent_rolls=0, def_percent_rolls=0, er_rolls=0,
            em_rolls=0, cd_rolls=0, cr_rolls=0
        ):
        super().__init__(
            set_bonus=set_bonus, main_atk_percent=int(main_atk_percent)*0.466,
            main_hp_percent=int(main_hp_percent)*0.466, main_def_percent=int(main_def_percent)*0.583, main_em=int(main_em)*186.5,
            main_anemo_dmg_bonus=int(main_anemo_dmg_bonus)*0.466, main_hydro_dmg_bonus=int(main_hydro_dmg_bonus)*0.466,
            main_electro_dmg_bonus=int(main_electro_dmg_bonus)*0.466,
            main_dendro_dmg_bonus=int(main_dendro_dmg_bonus)*0.466, main_cryo_dmg_bonus=int(main_cryo_dmg_bonus)*0.466,
            main_pyro_dmg_bonus=int(main_pyro_dmg_bonus)*0.466, main_geo_dmg_bonus=int(main_geo_dmg_bonus)*0.466,
            main_phys_dmg_bonus=int(main_phys_dmg_bonus)*0.583, flat_hp_rolls=flat_hp_rolls,
            flat_atk_rolls=flat_atk_rolls, flat_def_rolls=flat_def_rolls, hp_percent_rolls=hp_percent_rolls,
            atk_percent_rolls=atk_percent_rolls, def_percent_rolls=def_percent_rolls, er_rolls=er_rolls,
            em_rolls=em_rolls, cd_rolls=cd_rolls, cr_rolls=cr_rolls
        )
        assert (
            self.main_atk_percent > 0 or self.main_hp_percent > 0 or 
            self.main_def_percent > 0 or self.main_em > 0 or
            self.main_anemo_dmg_bonus > 0 or self.main_hydro_dmg_bonus > 0 or
            self.main_electro_dmg_bonus > 0 or self.main_dendro_dmg_bonus > 0 or
            self.main_cryo_dmg_bonus > 0 or self.main_pyro_dmg_bonus > 0 or
            self.main_geo_dmg_bonus > 0 or self.main_phys_dmg_bonus > 0
        )
