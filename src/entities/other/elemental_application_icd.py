from src.entities.entity import Entity

class DefaultICD(Entity):
    def __init__(self, hit_limit=3, time_limit=2.5):
        """
        :params:
        icds - {enemy: [hits, timer]}
        """
        self.icds = {}
        self.hit_limit = hit_limit
        self.time_limit = time_limit

    def time_passes(self, seconds: float):
        for key, value in self.icds.items():
            hits, _ = value
            # If timer was started (there was an application in the past), update time rule
            if hits > 0:
                self.icds[key][1] += seconds
            # If CD passed, zero time rule and hit rule
            if self.icds[key][1] >= self.time_limit:
                self.icds[key][0] = 0
                self.icds[key][1] = 0

    def try_apply_element(self, enemy):
        """
        This function is invoked every time elemental attack hits a specific
        opponent and tries to apply an element. Returns True or False on
        whether element is applied or not.
        """
        try:
            hits, timer = self.icds[enemy]
        except KeyError:
            self.icds[enemy] = [0, 0]
            hits, timer = self.icds[enemy]
        # If CD is not active, apply element
        if hits == 0 and timer == 0:
            # Always update hit rule
            self.icds[enemy][0] += 1
            # If hit limit is reached, zero time rule and hit rule
            if self.icds[enemy][0] >= self.hit_limit:
                self.icds[enemy][0] = 0
                self.icds[enemy][1] = 0
            return True
        # If CD is active, do not apply element
        else:
            self.icds[enemy][0] += 1
            if self.icds[enemy][0] >= self.hit_limit:
                self.icds[enemy][0] = 0
                self.icds[enemy][1] = 0
            return False

class ThrustingAttackICD(DefaultICD):
    def __init__(self):
        super().__init__(3, 0.5)

class NoICD(DefaultICD):
    def __init__(self):
        super().__init__(hit_limit=1, time_limit=0)
