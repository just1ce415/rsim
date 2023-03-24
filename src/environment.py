from src.constants import *
from entities.characters.character import Character
from entities.enemies.enemy import Enemy

from typing import List, Dict

class Environment:
    def __init__(
            self, team:List[Character], actions:List,
            n_targets:int, enemy_res:Dict[str: float], enemy_lvl:int,
            loggers:str
        ):
        self.data = {}
        self.time_passed = 0
        self.loggers = loggers
        self.team = team
        for character in self.team:
            character.set_env(self)
        self.weapons = [character.weapon for character in self.team]
        self.set_bonuses = [character.dynamic_set_bonus for character in self.team]
        self.summons_and_adaptives = []
        self.current_action = None
        self.particle_sets = []
        self.actions = actions
        self.n_targets = n_targets
        self.enemies = [Enemy(enemy_lvl, enemy_res) for _ in range(self.n_targets)]

    def start(self):
        while len(self.actions) > 0 or self.current_action is not None:
            self.time_passed += 1/FPS