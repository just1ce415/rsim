from src.entities.characters import Character
from typing import Tuple

class Event:
    """
    Types of events:
    - (Character) triggered a (reaction)
    - (Character's) (attack) of (type) hits an oponent affected by (element)
    with (elemental type) and (scored/not scored) CRIT. Note: this event is meant
    to be three kinds of events: (character) performs/uses an (attack),
    (character) is going to hit an enemy affected by (element) with (attack)
    and (character) hits the enemy (...)
    - (Character's) HP decreases by certain (amount)
    - (Character) heals other (character) by an (amount) of HP
    - (Character's) shielded
    - (Character's) HP satisfies (threshold)
    - Swapped from (character) to (character)
    - (Character) picked up an elemental (orb/particle) of (elemental type)
    - (Character) jumped
    - (Character) dashed
    """
    def __init__(
            self, event_type:str, character_one:Character, character_two:Character,
            attack:str, attack_type:str, affected_by_element:str, attack_elemental_type:str,
            scored_crit:bool, hp_decreased_amount:float, hp_healed_amount:float,
            hp_threshold: Tuple[str, float], particle_type:str
        ):
        self.event_type = event_type
        self.character_one = character_one
        self.character_two = character_two
        self.attack = attack
        self.attack_type = attack_type
        self.affected_by_element = affected_by_element
        self.attack_elemental_type = attack_elemental_type
        self.scored_crit = scored_crit
        self.hp_decreased_amount = hp_decreased_amount
        self.hp_healed_amount = hp_healed_amount
        self.hp_threshold = hp_threshold
        self.particle_type = particle_type

    