from configs import BaseConfig
from environment import Environment

class Simulator:
    def __init__(
        self, config:BaseConfig, n_rotations=10, n_targets=1,
        enemy_res={"phys": 1.1, "anemo": 1.1, "hydro": 1.1, "electro": 1.1, "dendro": 1.1, "cryo": 1.1, "pyro": 1.1, "geo": 1.1},
        enemy_lvl=100
    ):
        self.config = config
        self.n_rotations = n_rotations
        self.targets = n_targets
        self.__test_env = Environment(
        team=config.team, action_genrator=config.action_generator, 
        n_rotations=n_rotations, n_targets=n_targets, enemy_res=enemy_res,
        enemy_lvl=enemy_lvl
        )
        self.loggers = ""
        self.data = {}
        self.__simulate_test()
        self.__simulate()

    def __simulate_test(self):
        self.__test_env.start(self.loggers, self.data)
        self.config.set_artifacts_params(self.data["target_ers"], self.data["mv_params"])
        self.config.initialize_artifacts()

    def __simulate(self):
        self.__env = Environment(
        team=self.config.team, action_genrator=self.config.action_generator, 
        n_rotations=self.n_rotations, n_targets=self.n_targets, enemy_res=self.__test_env.enemy.enemy_res,
        enemy_lvl=self.__test_env.enemy.enemy_lvl
        )
        self.__env.start(self.loggers, self.data)
