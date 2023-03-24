from src.entities.entity import Entity

class SetBonus(Entity):
    def __init__(self, holder, n_pieces=0):
        self.holder = holder
        self.n_pieces = n_pieces