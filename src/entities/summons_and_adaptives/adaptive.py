from src.entities.characters.character import Character, Entity
from src.constants import NONE

class Adaptive(Entity):
    def __init__(self, summoner:Character):
        super().__init__()
        self.summoner = summoner
        self.particle_generation = None
        self.elemental_type = self.summoner.elemental_type

        """
        Outgoing stats (other than "base" ones)
        Any adaptive can:
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
        self.crit_ratio = 1/2
        self.cd = 0
        self.cr = 0
        self.reaction_multiplier = 0
        self.reaction_bonus = 0
        self.quadratic_factor = 1
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


class Action(Adaptive):
    def __init__(self, summoner:Character):
        super().__init__(summoner)
        # Apart from what any adaptive can do, any action can also create a summon/adaptive
        self.summon = None