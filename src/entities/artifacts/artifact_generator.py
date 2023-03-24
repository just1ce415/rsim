from src.entities.artifacts.flower import Flower
from src.entities.artifacts.feather import Feather
from src.entities.artifacts.sands import Sands
from src.entities.artifacts.goblet import Goblet
from src.entities.artifacts.circlet import Circlet
from src.damage import general_dmg
from src.constants import *

from typing import Dict

class ArtifactGenerator:
    def __init__(
            self, flower:Flower, feather:Feather, sands:Sands,
            goblet:Goblet, circlet:Circlet
        ):
        self.flower = flower
        self.feather = feather
        self.sands = sands
        self.goblet = goblet
        self.circlet = circlet

        self.max_flat_hp_rolls = 24
        self.max_flat_atk_rolls = 24
        self.max_flat_def_rolls = 30
        self.max_hp_percent_rolls = 30
        self.max_atk_percent_rolls = 30
        self.max_def_percent_rolls = 30
        self.max_er_rolls = 30
        self.max_em_rolls = 30
        self.max_cd_rolls = 30
        self.max_cr_rolls = 30
        self.max_rolls_total = 45
        self.min_rolls_total = 40

        self.flower_substat_distr = {
            "flat_atk": 0.1579,
            "flat_def": 0.1579,
            "hp_percent": 0.1053,
            "atk_percent": 0.1053,
            "def_percent": 0.1053,
            "er": 0.1053,
            "em": 0.1053,
            "cd": 0.0789,
            "cr": 0.0789,
        }
        self.feather_substats_distr = {
            "flat_hp": 0.1579,
            "flat_def": 0.1579,
            "hp_percent": 0.1053,
            "atk_percent": 0.1053,
            "def_percent": 0.1053,
            "er": 0.1053,
            "em": 0.1053,
            "cd": 0.0789,
            "cr": 0.0789,
        }
        sands_substats_rates = {
            "flat_hp": 0.15,
            "flat_def": 0.15,
            "flat_atk": 0.15,
            "hp_percent": 0.10,
            "atk_percent": 0.10,
            "def_percent": 0.10,
            "er": 0.10,
            "em": 0.10,
            "cd": 0.075,
            "cr": 0.075
        }
        goblet_substats_rates = {
            "flat_hp": 0.1364,
            "flat_def": 0.1364,
            "flat_atk": 0.1364,
            "hp_percent": 0.0909,
            "atk_percent": 0.0909,
            "def_percent": 0.0909,
            "er": 0.0909,
            "em": 0.0909,
            "cd": 0.0682,
            "cr": 0.0682
        }
        circlet_substats_rates = {
            "flat_hp": 0.1463,
            "flat_def": 0.1463,
            "flat_atk": 0.1463,
            "hp_percent": 0.0976,
            "atk_percent": 0.0976,
            "def_percent": 0.0976,
            "er": 0.0976,
            "em": 0.0976,
            "cd": 0.0732,
            "cr": 0.0732
        }

        self.sands_substat_distr = sands_substats_rates
        if self.sands.main_hp_percent > 0:
            self.max_hp_percent_rolls -= 6
            self.sands_substat_distr["hp_percent"] = 0
        elif self.sands.main_atk_percent > 0:
            self.max_atk_percent_rolls -= 6
            self.sands_substat_distr["atk_percent"] = 0
        elif self.sands.main_def_percent > 0:
            self.max_def_percent_rolls -= 6
            self.sands_substat_distr["def_percent"] = 0
        elif self.sands.main_er > 0:
            self.max_er_rolls -= 6
            self.sands_substat_distr["er"] = 0
        elif self.sands.main_em > 0:
            self.max_em_rolls -= 6
            self.sands_substat_distr["em"] = 0
        else:
            raise ValueError("Sands mainstat modCheck?")

        self.goblet_substat_distr = sands_substats_rates
        if self.goblet.main_hp_percent > 0:
            self.max_hp_percent_rolls -= 6
            self.goblet_substat_distr["hp_percent"] = 0
        elif self.goblet.main_atk_percent > 0:
            self.max_atk_percent_rolls -= 6
            self.goblet_substat_distr["atk_percent"] = 0
        elif self.goblet.main_def_percent > 0:
            self.max_def_percent_rolls -= 6
            self.goblet_substat_distr["def_percent"] = 0
        elif self.goblet.main_er > 0:
            self.max_er_rolls -= 6
            self.goblet_substat_distr["er"] = 0
        elif self.goblet.main_em > 0:
            self.max_em_rolls -= 6
            self.goblet_substat_distr["em"] = 0
        else:
            self.goblet_substat_distr = goblet_substats_rates

        self.circlet_substat_distr = sands_substats_rates
        if self.circlet.main_hp_percent > 0:
            self.max_hp_percent_rolls -= 6
            self.circlet_substat_distr["hp_percent"] = 0
        elif self.circlet.main_atk_percent > 0:
            self.max_atk_percent_rolls -= 6
            self.circlet_substat_distr["atk_percent"] = 0
        elif self.circlet.main_def_percent > 0:
            self.max_def_percent_rolls -= 6
            self.circlet_substat_distr["def_percent"] = 0
        elif self.circlet.main_er > 0:
            self.max_er_rolls -= 6
            self.circlet_substat_distr["er"] = 0
        elif self.circlet.main_em > 0:
            self.max_em_rolls -= 6
            self.circlet_substat_distr["em"] = 0
        else:
            self.circlet_substat_distr = circlet_substats_rates
            if self.circlet.main_cd > 0:
                self.max_cd_rolls -= 6
                self.circlet_substat_distr["cd"] = 0
            elif self.circlet.main_cr> 0:
                self.max_cr_rolls -= 6
                self.circlet_substat_distr["cr"] = 0
            else:
                ValueError("Circlet mainstat modCheck?")


    def generate_substats_by_stat_value(
            self, stat_value:float, dmg_info:Dict, er_info:Dict,
        ):
        """
        Sets of stats with the same stat value lead to (approximately) the same DPR.
        This dependency is linear.
        :params:
        stat_value - a float value between 0 and 100, where zero corresponds to DPR
        without substats and hundred corresponds to maximum possible DPR with substats
        (maximum substats 5(pieces) * (4+5)(substats each) = 45);
        dmg_info - dmg_info of holder (check structure src/protocol.json)
        er_info - er_info of holder (check structure src/protocol.json)
        """
        generated_energies = er_info["particle_energy_each_rotation"]
        costs = er_info["cost_each_rotation"]
        current_ers = er_info["actual_er_each_rotation"]
        n_rotations = len(generated_energies)
        recommended_ers = [costs[i] / generated_energies[i] for i in range(len(n_rotations))]
        recommended_additional_ers = [recommended_ers[i] - current_ers[i] for i in range(n_rotations)]
        target_er = max(recommended_additional_ers)
        target_er = target_er - self.sands.main_er

    def __calculate_total_dmg(
            self, dmg_info, flat_hp, flat_atk, flat_def, hp_percent, atk_percent,
            def_percent, em, cd, cr
        ):
        total_dmg = 0
        for i in range(len(dmg_info["base_hp"])):
            new_flat_hp = flat_hp + dmg_info["flat_hp"]
            new_flat_atk = flat_atk + dmg_info["flat_atk"]
            new_flat_def = flat_def + dmg_info["flat_def"]
            new_hp_percent = hp_percent + dmg_info["hp_percent"]
            new_atk_percent = atk_percent + dmg_info["atk_percent"]
            new_def_percent = def_percent + dmg_info["def_percent"]
            new_em = em + dmg_info["em"]
            new_cd = cd + dmg_info["cd"]
            new_cr = cr + dmg_info["cr"]
            dmg = general_dmg(
                dmg_info["base_hp"], dmg_info["base_atk"], dmg_info["base_def"], new_flat_hp,
                new_flat_atk, new_flat_def, new_hp_percent, new_atk_percent, new_def_percent,
                new_em, dmg_info["mv_hp"], dmg_info["mv_atk"], dmg_info["mv_def"], dmg_info["mv_em"],
                dmg_info["flat_dmg"], dmg_info["dmg_bonus"], dmg_info["crit_ratio"], new_cd,
                new_cr, dmg_info["is_spread"], dmg_info["is_aggravate"], dmg_info["is_swirl"],
                dmg_info["is_bloom"], dmg_info["is_burgeon"], dmg_info["is_hyperbloom"],
                dmg_info["is_burning"], dmg_info["is_electro_charged"], dmg_info["is_overload"],
                dmg_info["is_superconduct"], dmg_info["is_forward_multiplicative"],
                dmg_info["is_reverse_multiplicative"], dmg_info["level"], dmg_info["reaction_bonus"]
            )
            total_dmg = total_dmg + dmg
        return total_dmg

    def __constraint_function(self, flat_hp, flat_atk, flat_def, hp_percent, atk_percent,
            def_percent, em, cd, cr):
        return (flat_hp / self.flat_hp_roll + flat_atk / self.flat_atk_roll + flat_def / self.flat_def_roll +
                hp_percent / self.hp_persent_roll + atk_percent / self.atk_percent_roll +
                def_percent / self.def_percent_roll + em / self.em_roll + cd / self.cd_roll + cr / self.cr_roll - 
                self.max_rolls_total)

    def lagrangian(self, dmg_info, flat_hp, flat_atk, flat_def, hp_percent, atk_percent,
            def_percent, em, cd, cr, la):
        return self.__calculate_total_dmg(dmg_info, flat_hp, flat_atk, flat_def, hp_percent, atk_percent,
            def_percent, em, cd, cr) + la * self.__constraint_function(flat_hp, flat_atk, flat_def, hp_percent,
            atk_percent, def_percent, em, cd, cr)

    def sample_substats(
        self, flat_atk_rolls=-1, flat_hp_rolls=-1, flat_def_rolls=-1, hp_percent_rolls=-1,
        atk_percent_rolls=-1, def_percent_rolls=-1, er_rolls=-1, em_rolls=-1,
        cd_rolls=-1, cr_rolls=-1
        ):
        """
        Samples three-four (1:1) substats from stat disribution for each artifact
        and upgrades them randomly 1:1:1:1 4-5 times unless params have specifications
        """
        pass