from src.entities.characters.character import Character
from src.entities.enemies.enemy import Enemy

class Event:
    """
    Types of events:
    - (Character) is going to trigger a (reaction) on (enemy);
    - (Character) triggered a (reaction) on (enemy);
    - (Character) performs/uses an (attack) of (type) with (elemental type)
    to the (opponent);
    - (Character's) (attack) of (type) hits an (oponent)
    with (elemental type) and (scored/not scored) CRIT;
    - (Character's) HP decreases by certain (amount);
    - (Character) heals other (character) by an (amount) of HP;
    - Swapped from (character) to (character);
    - (Character) picked up an elemental (orb/particle) of (elemental type);
    - (Character) jumped;
    - (Character) dashed;
    """
    def __init__(
            self, event_type:str, character_one:Character=None, reaction:str=None, character_two:Character=None,
            attack_type:str=None, dmg_type:str=None, attack_elemental_type:str=None,
            enemy:Enemy=None, scored_crit:bool=None, hp_decreased_amount:float=None, hp_healed_amount:float=None,
            particle_type:str=None
        ):
        self.event_type = event_type
        self.character_one = character_one
        self.reaction = reaction
        self.character_two = character_two
        self.attack_type = attack_type
        self.dmg_type = dmg_type
        self.enemy = enemy
        self.attack_elemental_type = attack_elemental_type
        self.scored_crit = scored_crit
        self.hp_decreased_amount = hp_decreased_amount
        self.hp_healed_amount = hp_healed_amount
        self.particle_type = particle_type

    