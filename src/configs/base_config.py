
class BaseConfig:
    def __init__(self):
        self.team = []
        self.rotation = []

        # to optimize artifacts
        self.target_ers = [1, 1, 1, 1]
        self.mv_params = [{}, {}, {}, {}]

    def _initialize_rotation(self):
        self.action_generator = self.__action_generator_method()

    def _initialize_characters(self):
        pass

    def initialize_artifacts(self):
        pass

    def __action_generator_method(self):
        for action in self.rotation:
            yield action

    def set_artifacts_params(self, target_ers, mv_params):
        """
        :params:
        target_ers - preferable amount of ER for each character respectively for given rotation
        mv_params - a list of dictionaries which contain dmg source distribution information e.g.:
        "mv_atk" - attack motion value
        "mv_hp" - HP motion value
        "mv_def" - DEF motion value
        "n_spreads" - number of spreads
        "n_aggravates" - number of aggravates
        "mv_flat" - motion values of flat dmg that scales of character stat (Cinnibar Spindle)
        "flat_dmg" - total flat dmg obtained by buffs which scales of other character stat (Shenhe)
        "n_swirls" - number of swirls
        "n_burning_tiks" - number of burning tiks
        "n_ec_tiks" - number of electro-charged tiks
        "n_blooms" - number of blooms
        "n_burgeons" - number of burgeons
        "n_hyperblooms" - number of hyperblooms
        "n_overloads" - number of overloads
        "n_superconduct" - number of superconducts
        """
        self.target_ers = target_ers
        self.mv_params = mv_params