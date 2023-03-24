from src.entities.entity import Entity
from src.environment import Environment
from src.constants import *

class ParticleSet(Entity):
    def __init__(self, env:Environment, n_particles:int, element:str):
        self.env = env
        self.n_particles = n_particles
        self.element = element
        # Seconds before particles will reach character
        self.lifetime = 1.2

    def hitlag_extension(self, seconds: float):
        """
        Can move during hitlag
        """
        pass

    def time_passes(self, seconds: float):
        self.lifetime -= seconds
        if self.lifetime <= 0:
            self.__funnel()
            self.timeout()

    def __funnel(self):
        for character in self.env.team:
            if self.element == CLEAR:
                if character.on_field:
                    character.energy += self.n_particles * 2
                else:
                    character.energy += self.n_particles * 1.2
            else:
                if character.on_field and self.element == character.elemental_type:
                    character.energy += self.n_particles * 3
                elif not character.on_field and self.element == character.elemental_type:
                    character.energy += self.n_particles * 1.8
                elif character.on_field and self.element != character.elemental_type:
                    character.energy += self.n_particles * 1
                elif not character.on_field and self.element != character.elemental_type:
                    character.energy += self.n_particles * 0.6
        self.env.loggers += "[INFO]: t={}; {} {} particles were funneled to the team.\n".format(
            self.env.time_passed, self.n_particles, self.element
        )


    def timeout(self):
        for i, particle_set in enumerate(self.env.particle_sets):
            if particle_set == self:
                del self.env.particle_sets[i]
