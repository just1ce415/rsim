from src.entities.artifacts.artifact import Artifact
from src.entities.artifacts.sets.set_bonus import SetBonus

class Goblet(Artifact):
    def __init__(self, set_bonus:SetBonus, main_atk_percent=0,
            main_hp_percent=False, main_def_percent=False, main_em=False, main_anemo_dmg_bonus=False,
            main_hydro_dmg_bonus=False, main_electro_dmg_bonus=False, main_dendro_dmg_bonus=False,
            main_cryo_dmg_bonus=False, main_pyro_dmg_bonus=False, main_geo_dmg_bonus=False,
            main_phys_dmg_bonus=False
        ):
        super().__init__(
            self, set_bonus=set_bonus, main_atk_percent=int(main_atk_percent)*0.466,
            main_hp_percent=int(main_hp_percent)*0.466, main_def_percent=int(main_def_percent)*0.583, main_em=int(main_em)*186.5,
            main_anemo_dmg_bonus=int(main_anemo_dmg_bonus)*0.466, main_hydro_dmg_bonus=int(main_hydro_dmg_bonus)*0.466,
            main_electro_dmg_bonus=int(main_electro_dmg_bonus)*0.466,
            main_dendro_dmg_bonus=int(main_dendro_dmg_bonus)*0.466, main_cryo_dmg_bonus=int(main_cryo_dmg_bonus)*0.466,
            main_pyro_dmg_bonus=int(main_pyro_dmg_bonus)*0.466, main_geo_dmg_bonus=int(main_geo_dmg_bonus)*0.466,
            main_phys_dmg_bonus=int(main_phys_dmg_bonus)*0.583
        )
        assert (
            self.main_atk_percent > 0 or self.main_hp_percent > 0 or 
            self.main_def_percent > 0 or self.main_em > 0 or
            self.main_anemo_dmg_bonus > 0 or self.main_hydro_dmg_bonus > 0 or
            self.main_electro_dmg_bonus > 0 or self.main_dendro_dmg_bonus > 0 or
            self.main_cryo_dmg_bonus > 0 or self.main_pyro_dmg_bonus > 0 or
            self.main_geo_dmg_bonus > 0 or self.main_phys_dmg_bonus > 0
        )