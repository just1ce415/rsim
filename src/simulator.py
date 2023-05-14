from src.configs.base_config import BaseConfig
from src.environment import Environment
from src.constants import *

class Simulator:
    def __init__(
        self, config:BaseConfig, n_rotations=10, n_targets=1,
        enemy_res={PHYS: 0.1, ANEMO: 0.1, HYDRO: 0.1, ELECTRO: 0.1, DENDRO: 0.1, CRYO: 0.1, PYRO: 0.1, GEO: 0.1},
        enemy_lvl=100
    ):
        self.enemy_res = enemy_res
        self.enemy_lvl = enemy_lvl
        self.config = config
        self.config.initialize_team()
        self.config.initialize_rotation()
        self.n_rotations = n_rotations
        self.n_targets = n_targets
        self.all_actions = config.rotation * n_rotations
        self.loggers = ""
        self.__simulate_test()
        self.__simulate()
        with open("logs/log_{}.txt".format(self.config.__class__.__name__), "w") as f:
            f.write(self.loggers)

    def __simulate_test(self):
        test_env = Environment(
        team=self.config.team, actions=self.all_actions, 
        n_targets=self.n_targets, enemy_res=self.enemy_res,
        enemy_lvl=self.enemy_lvl, loggers=self.loggers
        )
        test_env.start()
        self.config.set_artifact_params(test_env.data)
        self.config.initialize_artifacts()

    def __simulate(self):
        env = Environment(
        team=self.config.team, actions=self.all_actions,
        n_targets=self.n_targets, enemy_res=self.enemy_res,
        enemy_lvl=self.enemy_lvl, loggers=self.loggers
        )
        env.start()
