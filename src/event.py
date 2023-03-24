from src.entities.characters import Character

class Event:
    """
    Types of events:
    - (Character) triggered a (reaction);
    - (Character) performs/uses an (attack) of (type) with (elemental type)
    to the opponent affected by (element);
    - (Character's) (attack) of (type) hits an oponent affected by (element)
    with (elemental type) and (scored/not scored) CRIT;
    - (Character's) HP decreases by certain (amount);
    - (Character) heals other (character) by an (amount) of HP;
    - Swapped from (character) to (character);
    - (Character) picked up an elemental (orb/particle) of (elemental type);
    - (Character) jumped;
    - (Character) dashed;
    """
    def __init__(
            self, event_type:str, character_one:Character, character_two:Character,
            attack:str, attack_type:str, affected_by_element:str, attack_elemental_type:str,
            scored_crit:bool, hp_decreased_amount:float, hp_healed_amount:float,
            particle_type:str
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
        self.particle_type = particle_type

    