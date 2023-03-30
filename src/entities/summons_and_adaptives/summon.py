from src.entities.characters.character import Character, Entity
from src.constants import NONE

class Summon(Entity):
    def __init__(self, summoner:Character):
        super().__init__()
        self.summoner = summoner
        # Tuple [chance to generate, respective amount]
        self.particle_generation = None
        self._init_particle_generation()

        self.level = self.summoner.level
        self.elemental_type = self.summoner.elemental_type
        self.base_hp = self.summoner.base_hp
        self.base_atk = self.summoner.base_atk
        self.base_def = self.summoner.base_def
        self.flat_hp = self.summoner.flat_hp
        self.flat_atk = self.summoner.flat_atk
        self.flat_def = self.summoner.flat_def
        self.hp_percent = self.summoner.hp_percent
        self.atk_percent = self.summoner.atk_percent
        self.def_percent = self.summoner.def_percent
        self.em = self.summoner.em
        self.er = self.summoner.er
        self.swirl_reaction_bonus = self.summoner.swirl_reaction_bonus
        self.bloom_reaction_bonus = self.summoner.bloom_reaction_bonus
        self.burgeon_reaction_bonus = self.summoner.burgeon_reaction_bonus
        self.hyperbloom_reaction_bonus = self.summoner.hyperbloom_reaction_bonus
        self.aggravate_reaction_bonus = self.summoner.aggravate_reaction_bonus
        self.spread_reaction_bonus = self.summoner.spread_reaction_bonus
        self.overload_reaction_bonus = self.summoner.overload_reaction_bonus
        self.superconduct_reaction_bonus = self.summoner.superconduct_reaction_bonus
        self.electro_charged_reaction_bonus = self.summoner.electro_charged_reaction_bonus
        self.burning_reaction_bonus = self.summoner.burning_reaction_bonus
        self.vaporize_reaction_bonus = self.summoner.vaporize_reaction_bonus
        self.melt_reaction_bonus = self.summoner.melt_reaction_bonus
        self.anemo_dmg_bonus = self.summoner.anemo_dmg_bonus
        self.hydro_dmg_bonus = self.summoner.hydro_dmg_bonus
        self.electro_dmg_bonus = self.summoner.electro_dmg_bonus
        self.dendro_dmg_bonus = self.summoner.dendro_dmg_bonus
        self.cryo_dmg_bonus = self.summoner.cryo_dmg_bonus
        self.pyro_dmg_bonus = self.summoner.pyro_dmg_bonus
        self.geo_dmg_bonus = self.summoner.geo_dmg_bonus
        self.phys_dmg_bonus = self.summoner.phys_dmg_bonus
        self.na_dmg_bonus = self.summoner.na_dmg_bonus
        self.ca_dmg_bonus = self.summoner.ca_dmg_bonus
        self.pa_dmg_bonus = self.summoner.pa_dmg_bonus
        self.skill_dmg_bonus = self.summoner.skill_dmg_bonus
        self.burst_dmg_bonus = self.summoner.burst_dmg_bonus
        self.all_dmg_bonus = self.summoner.all_dmg_bonus
        self.all_cd = self.summoner.all_cd
        self.all_cr = self.summoner.all_cr
        self.anemo_cd = self.summoner.anemo_cd
        self.hydro_cd = self.summoner.hydro_cd
        self.electro_cd = self.summoner.electro_cd
        self.dendro_cd = self.summoner.dendro_cd
        self.cryo_cd = self.summoner.cryo_cd
        self.pyro_cd = self.summoner.pyro_cd
        self.geo_cd = self.summoner.geo_cd
        self.phys_cd = self.summoner.phys_cd
        self.na_cd = self.summoner.na_cd
        self.ca_cd = self.summoner.ca_cd
        self.pa_cd = self.summoner.pa_cd
        self.skill_cd = self.summoner.skill_cd
        self.burst_cd = self.summoner.burst_cd
        self.anemo_cr = self.summoner.anemo_cr
        self.hydro_cr = self.summoner.hydro_cr
        self.electro_cr = self.summoner.electro_cr
        self.dendro_cr = self.summoner.dendro_cr
        self.cryo_cr = self.summoner.cryo_cr
        self.pyro_cr = self.summoner.pyro_cr
        self.geo_cr = self.summoner.geo_cr
        self.phys_cr = self.summoner.phys_cr
        self.na_cr = self.summoner.na_cr
        self.ca_cr = self.summoner.ca_cr
        self.pa_cr = self.summoner.pa_cr
        self.skill_cr = self.summoner.skill_cr
        self.burst_cr = self.summoner.burst_cr
        self.healing_bonus = self.summoner.healing_bonus

        """
        Outgoing stats (other than "base" ones)
        Any summon can:
        1) Deal damage
        2) Apply an element
        3) Generate particles
        4) Heal/shield
        5) Reduce character's HP
        """
        self.dmg_stats_ready = False
        self.mv_hp = 0
        self.mv_atk = 0
        self.mv_def = 0
        self.mv_em = 0
        self.flat_dmg = 0
        self.dmg_bonus = 0
        self.crit_ratio = 0
        self.cd = 0
        self.cr = 0
        self.reaction_multiplier = 0
        self.reaction_bonus = 0
        self.quadratic_factor = 0
        self.dmg_type = NONE
        self.targets = [0]

        self.particle_set = None

        self.heal_stats_ready = False
        self.heal_base_stat = 0
        self.heal_mv = 0
        self.healed_members = 0

        self.shield_stats_ready = False
        self.shield_base_stat = 0
        self.shield_mv = 0

        self.hp_reduced = 0

    def _init_particle_generation(self):
        """
        self.particle_generation - Tuple[chance_to_generate, respective_amount]
        """
        pass

    def time_passes(self, seconds: float):
        pass

    def hitlag_extension(self, seconds: float):
        pass

    def timeout(self):
        pass

    def generate_particle_set(self):
        from src.entities.other.particle_set import ParticleSet
        from random import random
        n_particles = 0
        element = self.summoner.elemental_type
        if self.particle_generation is None:
            return
        elif len(self.particle_generation) == 1:
            n_particles = self.particle_generation[0][1]
            return ParticleSet(self.summoner.team, n_particles, element)
        elif len(self.particle_generation) == 2:
            randomed = random()
            if randomed < self.particle_generation[0][0]:
                n_particles = self.particle_generation[0][1]
            else:
                n_particles = self.particle_generation[1][1]
            return ParticleSet(self.summoner.team, n_particles, element)