from src.entities.characters.character import Character, Entity
from src.entities.other.particle_set import ParticleSet
from src.entities.other.elemental_application_icd import *
from src.constants import *

class Summon(Entity):
    def __init__(self, summoner:Character):
        super().__init__()
        self.summoner = summoner
        self.timedout = False
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
        self.anemo_dmg_bonus = self.summoner.anemo_dmg_bonus
        self.hydro_dmg_bonus = self.summoner.hydro_dmg_bonus
        self.electro_dmg_bonus = self.summoner.electro_dmg_bonus
        self.dendro_dmg_bonus = self.summoner.dendro_dmg_bonus
        self.cryo_dmg_bonus = self.summoner.cryo_dmg_bonus
        self.pyro_dmg_bonus = self.summoner.pyro_dmg_bonus
        self.geo_dmg_bonus = self.summoner.geo_dmg_bonus
        self.phys_dmg_bonus = self.summoner.phys_dmg_bonus
        self.crit_ratio = self.summoner.crit_ratio
        self.cd = self.summoner.cd
        self.cr = self.summoner.cr
        self.healing_bonus = self.summoner.healing_bonus

        """
        Outgoing stats (other than "base" ones)
        Any summon can:
        1) Deal damage
        2) Apply an element
        3) Generate particles
        4) Heal/shield
        5) Reduce character's HP
        6) Create other summons
        """
        self.dmg_stats_ready = False
        self.mv_hp = 0
        self.mv_atk = 0
        self.mv_def = 0
        self.mv_em = 0
        self.flat_dmg = 0
        self.dmg_bonus = 0
        self.reaction_multiplier = 0
        self.reaction_bonus = 0
        self.quadratic_factor = 1
        self.attack_type = NONE
        self.dmg_type = NONE
        self.targets = [0]

        self.icd_group: DefaultICD = None
        self.gu = 0.0
        self.apply_to_enemy = True
        self.apply_to_character = False
        self.apply_to_weapon = False

        self.particle_set: ParticleSet = None

        self.heal_stats_ready = False
        self.heal_base_stat = 0
        self.heal_mv = 0
        self.healed_members = 0

        self.shield_stats_ready = False
        self.shield_base_stat = 0
        self.shield_mv = 0

        self.hp_reduced = 0

        self.summon:Entity = None
        self.summon_limit = 1

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