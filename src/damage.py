from src.constants import *

def total_hp(base_hp, hp_percent, flat_hp):
    return base_hp * (1 + hp_percent) + flat_hp

def total_atk(base_atk, atk_percent, flat_atk):
    return base_atk * (1 + atk_percent) + flat_atk

def total_def(base_def, def_percent, flat_def):
    return base_def * (1 + def_percent) + flat_def

def level_multiplier(level):
    if level == 100:
        return 2030.071808
    elif level == 90:
        return 1446.853458
    elif level == 80:
        return 1077.443668
    elif level == 70:
        return 756.640231
    else:
        raise Exception("Illegal level value.")

def effective_talent(base_stat, cd, cr, crit_ratio, dmg_bonus):
    """
    Effective talent dmg.
    :params:
    dmg_bonus - without adding 1
    """
    cv = 2*cr + cd
    return base_stat * get_cm(cv, crit_ratio) * (1 + dmg_bonus)

def effective_flat(base_dmg, cd, cr, crit_ratio, dmg_bonus):
    """
    Effective flat dmg (Shenhe, Cinnibar Spindle, aggravate)
    :params:
    dmg_bonus - without adding 1
    """
    cv = 2*cr + cd
    return base_dmg * get_cm(cv, crit_ratio) * (1 + dmg_bonus)

def general_dmg(
    base_hp, base_atk, base_def, flat_hp, flat_atk, flat_def,
    hp_percent, atk_percent, def_percent, em, mv_hp, mv_atk, mv_def,
    mv_em, flat_dmg, dmg_bonus, crit_ratio, cd, cr, is_spread,
    is_aggravate, is_swirl, is_bloom, is_burgeon, is_hyperbloom,
    is_burning, is_electro_charged, is_overload, is_superconduct,
    is_forward_multiplicative, is_reverse_multiplicative, level,
    reaction_bonus
):
    """
    Function for calculating dmg if you do not know which stats to use.
    Does not account for enemy resistance and defense.
    """
    t_atk = total_atk(base_atk, atk_percent, flat_atk)
    t_hp = total_hp(base_hp, hp_percent, flat_hp)
    t_def = total_def(base_def, def_percent, flat_def)
    spread_dmg = int(is_spread) * additive_reaction_dmg(SPREAD, level, em, reaction_bonus)
    aggravate_dmg = int(is_aggravate) * additive_reaction_dmg(AGGRAVATE, level, em, reaction_bonus)
    swirl_dmg = int(is_swirl) * transformative_reaction_dmg(SWIRL, level, em, reaction_bonus)
    bloom_dmg = int(is_bloom) * transformative_reaction_dmg(BLOOM, level, em, reaction_bonus)
    burgeon_dmg = int(is_burgeon) * transformative_reaction_dmg(BURGEON, level, em, reaction_bonus)
    hyperbloom_dmg = int(is_hyperbloom) * transformative_reaction_dmg(HYPERBLOOM, level, em, reaction_bonus)
    burning_dmg = int(is_burning) * transformative_reaction_dmg(BURNING, level, em, reaction_bonus)
    electro_charged_dmg = int(is_electro_charged) * transformative_reaction_dmg(ELECTRO_CHARGED, level, em, reaction_bonus)
    overload_dmg = int(is_overload) * transformative_reaction_dmg(OVERLOAD, level, em, reaction_bonus)
    superconduct_dmg = int(is_superconduct) * transformative_reaction_dmg(SUPERCONDUCT, level, em, reaction_bonus)
    reverse_multiplier = multipicative_reaction_factor(REVERSE, em, reaction_bonus) if is_reverse_multiplicative else 1
    forward_multiplier = multipicative_reaction_factor(FORWARD, em, reaction_bonus) if is_forward_multiplicative else 1
    cv = 2*cr + cd
    cm = get_cm(cv, crit_ratio)
    return ((t_atk * mv_atk + t_hp * mv_hp + t_def * mv_def + em * mv_em + flat_dmg + spread_dmg + aggravate_dmg) *
        (1 + dmg_bonus) * cm * reverse_multiplier * forward_multiplier + swirl_dmg + bloom_dmg + burgeon_dmg +
        hyperbloom_dmg + burning_dmg + electro_charged_dmg + overload_dmg + superconduct_dmg)

def talent_dmg(effective_talent, mv):
    return effective_talent * mv

def outgoing_dmg_multiplicative(dmg, character_level, enemy_level, enemy_resistance, def_shred, def_ignore):
    return dmg * res_multiplier(enemy_resistance) * def_multiplier(character_level, enemy_level, def_shred, def_ignore)

def res_multiplier(enemy_resistance):
    if enemy_resistance < 0:
        return 1 - (enemy_resistance / 2)
    elif 0 <= enemy_resistance < 0.75:
        return 1 - enemy_resistance
    else:
        1 / (4*enemy_resistance + 1)

def def_multiplier(character_level, enemy_level, def_shred, def_ignore):
    return (character_level + 100) / ((1 - def_shred)*(1 - def_ignore)*(enemy_level + 100) + character_level + 100)

def get_cm(cv, crit_ratio=1/2):
    """
    Artificial crit ratio
    """
    # if CRIT Rate is less than 1
    if cv <= 1 + 1/crit_ratio:
        return 1 + crit_ratio * pow(cv, 2) / (4 * pow(crit_ratio + 0.5, 2))
    else:
        return 1 + 1 * (cv - 2)

def transformative_reaction_dmg(reaction, level, em, reaction_bonus):
    if reaction == SWIRL:
        special_multiplier = 0.6
    elif reaction in (BLOOM, OVERLOAD):
        special_multiplier = 2
    elif reaction in (BURGEON, HYPERBLOOM):
        special_multiplier = 3
    elif reaction == ELECTRO_CHARGED:
        special_multiplier = 1.2
    elif reaction == BURNING:
        special_multiplier = 0.25
    elif reaction == SUPERCONDUCT:
        special_multiplier = 0.5
    emm = 16 * em + (2000 + em)
    return special_multiplier * level_multiplier(level) * (1 + emm + reaction_bonus)

def outgoing_transformative(reaction_dmg, enemy_resistance):
    return reaction_dmg * res_multiplier(enemy_resistance)

def additive_reaction_dmg(reaction, level, em, reaction_bonus):
    if reaction == AGGRAVATE:
        special_multiplier = 1.15
    elif reaction == SPREAD:
        special_multiplier = 1.25
    emm = 5 * em + (1200 + em)
    return special_multiplier * level_multiplier(level) * (1 + emm + reaction_bonus)

def multipicative_reaction_factor(reaction, em, reaction_bonus):
    if reaction == FORWARD:
        special_multiplier = 2
    elif reaction == REVERSE:
        special_multiplier = 1.5
    emm = 2.78 * em + (1400 + em)
    return special_multiplier * (1 + emm + reaction_bonus)
