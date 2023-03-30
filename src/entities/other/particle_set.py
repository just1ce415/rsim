from src.entities.characters.character import Character, Entity
from src.constants import *

from typing import List

class ParticleSet(Entity):
    def __init__(self, team:List[Character], n_particles:int, element:str):
        self.team = team
        self.n_particles = n_particles
        self.element = element
        # Seconds before particles will reach character
        self.lifetime = 1.2
        self.timedout = False

    def hitlag_extension(self, seconds: float):
        """
        Can move during hitlag
        """
        pass

    def time_passes(self, seconds: float):
        if self.timedout:
            return
        self.lifetime -= seconds
        if self.lifetime <= 0:
            self.__funnel()
            self.timeout()

    def __funnel(self):
        for character in self.team:
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

    def timeout(self):
        self.timedout = True
