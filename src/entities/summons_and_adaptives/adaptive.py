from src.entities.characters.character import Character, Entity
from src.entities.other.particle_set import ParticleSet
from src.entities.other.elemental_application_icd import *
from src.constants import *

class Adaptive(Entity):
    def __init__(self, summoner:Character):
        super().__init__()
        self.summoner = summoner
        self.particle_generation = None
        self.level = self.summoner.level
        self.elemental_type = self.summoner.elemental_type
        self.timedout = False
        self._init_particle_generation()

        self.base_hp = 0.0
        self.base_atk = 0.0
        self.base_def = 0.0
        self.flat_hp = 0.0
        self.flat_atk = 0.0
        self.flat_def = 0.0
        self.hp_percent = 0.0
        self.atk_percent = 0.0
        self.def_percent = 0.0
        self.em = 0.0
        self.er = 1.0
        self.anemo_dmg_bonus = 0.0
        self.hydro_dmg_bonus = 0.0
        self.electro_dmg_bonus = 0.0
        self.dendro_dmg_bonus = 0.0
        self.cryo_dmg_bonus = 0.0
        self.pyro_dmg_bonus = 0.0
        self.geo_dmg_bonus = 0.0
        self.phys_dmg_bonus = 0.0
        self.crit_ratio = 1/2
        self.cd = 0.5
        self.cr = 0.05
        self.healing_bonus = 0.0
        """
        Outgoing stats (other than "base" ones)
        Any adaptive can:
        1) Deal damage
        2) Apply an element
        3) Generate particles
        4) Heal/shield
        5) Reduce character's HP
        6) Create other summons
        """
        self.dmg_stats_ready = False
        self.mv_hp = 0
        self.mv_atk = 0
        self.mv_def = 0
        self.mv_em = 0
        self.flat_dmg = 0
        self.dmg_bonus = 0
        self.reaction_multiplier = 0
        self.reaction_bonus = 0
        self.quadratic_factor = 1
        self.attack_type = NONE
        self.dmg_type = NONE
        self.targets = [0]

        self.icd_group: DefaultICD = None
        self.gu = 0.0
        self.apply_to_enemy = True
        self.apply_to_character = False
        self.apply_to_weapon = False

        self.particle_set: ParticleSet = None

        self.heal_stats_ready = False
        self.heal_base_stat = 0
        self.heal_mv = 0
        self.healed_members = 0

        self.shield_stats_ready = False
        self.shield_base_stat = 0
        self.shield_mv = 0

        self.hp_reduced = 0

        self.summon: Entity = None
        self.summon_limit = 1

    def _init_particle_generation(self):
        """
        self.particle_generation - Tuple[chance_to_generate, respective_amount]
        """
        pass

    def time_passes(self, seconds: float):
        pass

    def hitlag_extension(self, seconds: float):
        pass

    def timeout(self):
        self.timedout = True

    def generate_particle_set(self):
        from src.entities.other.particle_set import ParticleSet
        from random import random
        n_particles = 0
        element = self.summoner.elemental_type
        if self.particle_generation is None:
            return
        elif len(self.particle_generation) == 1:
            n_particles = self.particle_generation[0][1]
            return ParticleSet(self.summoner.team, n_particles, element)
        elif len(self.particle_generation) == 2:
            randomed = random()
            if randomed < self.particle_generation[0][0]:
                n_particles = self.particle_generation[0][1]
            else:
                n_particles = self.particle_generation[1][1]
            return ParticleSet(self.summoner.team, n_particles, element)


class Action(Adaptive):
    def __init__(self, summoner:Character):
        super().__init__(summoner)
        # Action could be dash, jump, swap or do nothing
        # Action can also produce hitlag
        self.dash = False
        self.jump = False
        self.wait = False
        self.swap = False
        self.waittime = 0

        self.produce_hitlag = False

        self.er_stats_ready = False

class Swap(Action):
    def __init__(self, summoner: Character):
        super().__init__(summoner)
        self.swap = True
        self.latency = 0.07
        for char in summoner.team:
            if char.on_field:
                char.on_field = False
        summoner.on_field = True
        self.timedout = False
    
    def time_passes(self, seconds: float):
        self.latency -= seconds
        if self.latency <= 0:
            self.latency = 0
            self.timeout()

    def timeout(self):
        self.timedout = True

class Wait(Action):
    def __init__(self, summoner: Character, seconds:float):
        super().__init__(summoner)
        self.waittime = seconds
        self.wait = True
        self.timedout = False

    def time_passes(self, seconds: float):
        self.waittime -= seconds
        if self.waittime <= 0:
            self.waittime = 0
            self.timeout()

    def timeout(self):
        self.timedout = True

class Dash(Action):
    def __init__(self, summoner:Character):
        super().__init__(summoner)
        self.dash = True
        self.animation_time = 30 / FPS
        self.timedout = False

    def time_passes(self, seconds: float):
        if self.summoner.stamina >= 15 and self.summoner.dash_icd[1]:
            self.animation_time -= seconds
            if self.animation_time <= 0:
                self.animation_time = 0
                self.summoner.stamina -= 15 * (1 - self.summoner.dash_stamina_decrease)
                self.summoner.stamina_icd = 1.5
                if self.summoner.dash_icd[0] > 0:
                    self.summoner.dash_icd = [0.8, False]
                else:
                    self.summoner.dash_icd = [0.8, True]
                self.timeout()

    def timeout(self):
        self.timedout = True

class Jump(Action):
    def __init__(self, summoner: Character):
        super().__init__(summoner)
        self.jump = True
        self.animation_time = 40 / FPS
        self.timedout = False

    def time_passes(self, seconds: float):
        self.animation_time -= seconds
        if self.animation_time <= 0:
            self.animation_time = 0
            self.timeout()

    def timeout(self):
        self.timedout = True

class ElectroResonance(Adaptive):
    from src.event import Event

    def __init__(self, summoner: Character):
        super().__init__(summoner)
        self.particle_gen_cd = 0

    def notify(self, event:Event):
        if event.event_type == REACTION:
            if (event.reaction == SUPERCONDUCT or event.reaction == OVERLOAD or event.reaction == ELECTRO_CHARGED or
                event.reaction == QUICKEN or event.reaction == AGGRAVATE or event.reaction == HYPERBLOOM) and self.particle_gen_cd == 0:
                self.particle_set = ParticleSet(self.summoner.team, 1, ELECTRO)
                self.particle_gen_cd = 5

    def time_passes(self, seconds: float):
        if self.particle_gen_cd == 5:
            self.particle_gen_cd = max(0, self.particle_gen_cd - seconds)
        elif self.particle_gen_cd == 0:
            return
        else:
            self.particle_set = None
            self.particle_gen_cd = max(0, self.particle_gen_cd - seconds)

class CryoResonance(Adaptive):
    from src.event import Event

    def __init__(self, summoner: Character):
        super().__init__(summoner)

    def notify(self, event:Event):
        if event.event_type == CHARACTER_ATTACKS:
            if event.enemy.gauge_status.current_auras[CRYO] != [0, 0] or event.enemy.gauge_status.current_auras[FROZEN] != [0 ,0]:
                event.character_one.all_cr += 0.15
        if event.event_type == CHARACTER_HITS:
            if event.enemy.gauge_status.current_auras[CRYO] != [0, 0] or event.enemy.gauge_status.current_auras[FROZEN] != [0 ,0]:
                event.character_one.all_cr -= 0.15

class GeoResonance(Adaptive):
    from src.event import Event
    def __init__(self, summoner: Character):
        super().__init__(summoner)
        self.dmg_buff_dict = {
            self.summoner.team[0]: False,
            self.summoner.team[1]: False,
            self.summoner.team[2]: False,
            self.summoner.team[3]: False
        }
        self.res_shred_dict = {}
        for enemy in self.summoner.enemies:
            self.res_shred_dict[enemy] = [False, 0]

    def notify(self, event:Event):
        if event.event_type == CHARACTER_HITS:
            if not self.res_shred_dict[event.enemy][0]:
                event.enemy.resistance[GEO] -= 0.2
            self.res_shred_dict[event.enemy] = [True, 15]

    def time_passes(self, seconds: float):
        for char, is_active in self.dmg_buff_dict.items():
            if char.on_field and char.is_shielded:
                if not is_active:
                    self.dmg_buff_dict[char] = True
                    char.all_dmg_bonus += 0.15
            elif not char.on_field or not char.is_shielded:
                if is_active:
                    char.all_dmg_bonus -= 0.15
                    self.dmg_buff_dict[char] = False
        
        for enemy in self.res_shred_dict.keys():
            if self.res_shred_dict[enemy][0]:
                self.res_shred_dict[enemy][1] -= seconds
                if self.res_shred_dict[enemy][1] <= 0:
                    self.res_shred_dict[enemy][0] = False
                    self.res_shred_dict[enemy][1] = 0
                    enemy.resistance[GEO] += 0.2

class DendroResonance(Adaptive):
    from src.event import Event

    def __init__(self, summoner: Character):
        super().__init__(summoner)
        self.bqb_em_timer = 0
        self.ashb_em_timber = 0

    def notify(self, event:Event):
        if event.event_type == REACTION:
            if event.reaction in (QUICKEN, BURNING, BLOOM):
                if self.bqb_em_timer == 0:
                    for char in self.summoner.team:
                        char.em += 30
                self.bqb_em_timer = 6
            elif event.reaction in (AGGRAVATE, SPREAD, HYPERBLOOM, BURGEON):
                if self.ashb_em_timber == 0:
                    for char in self.summoner.team:
                        char.em += 20
                self.ashb_em_timber = 6

    def time_passes(self, seconds: float):
        if self.bqb_em_timer > 0:
            self.bqb_em_timer -= seconds
            if self.bqb_em_timer <= 0:
                self.bqb_em_timer = 0
                for char in self.summoner.team:
                    char.em -= 30
        if self.ashb_em_timber > 0:
            self.ashb_em_timber -= seconds
            if self.ashb_em_timber <= 0:
                self.ashb_em_timber = 0
                for char in self.summoner.team:
                    char.em -= 20
