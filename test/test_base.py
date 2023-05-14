import sys
import os
import platform

if platform.system() == 'Windows':
    src_path = os.getcwd()
    if src_path not in sys.path:
        sys.path.append(src_path)
else:
    src_path = os.getcwd()
    if src_path not in sys.path:
        sys.path.append(src_path)

from src.entities.other.gauge_status import GaugeStatus
from src.entities.summons_and_adaptives.reaction_summons import DendroCore, ElectroCharged, Burning
from src.entities.summons_and_adaptives.adaptive import ElectroResonance, CryoResonance, GeoResonance, DendroResonance
from src.entities.other.particle_set import ParticleSet
from src.entities.enemies.enemy import Enemy
from src.event import Event
from src.entities.characters.character import Character
from src.constants import *

import pytest

def is_close(actual, expected, epsilon=1e-4):
    assert type(actual) == type(expected)
    if isinstance(actual, list):
        for i in range(len(actual)):
            assert abs(actual[i] - expected[i]) < epsilon
    else:
        assert abs(actual - expected) < epsilon

class TestGaugeStatus:

    def test_apply_anemo_and_geo(self):
        g = GaugeStatus()
        g.apply_element(ANEMO, 2)
        assert g.current_auras[ANEMO] == [0, 0]
        g.apply_element(GEO, 1)
        assert g.current_auras[GEO] == [0, 0]

    def test_decay_rate_a(self):
        g = GaugeStatus()
        reations = g.apply_element(HYDRO, 1)
        assert reations == []
        assert g.current_auras[HYDRO] == [0.8, 1/11.875]
        g.time_passes(9.4)
        assert g.current_auras[HYDRO][0] != 0
        g.time_passes(0.1001)
        assert g.current_auras[HYDRO] == [0, 0]

    def test_decay_rate_b(self):
        g = GaugeStatus()
        g.apply_element(HYDRO, 2)
        assert g.current_auras[HYDRO] == [1.6, 1/7.5]
        g.time_passes(11.9)
        assert g.current_auras[HYDRO][0] != 0
        g.time_passes(0.1001)
        assert g.current_auras[HYDRO] == [0, 0]

    def test_hitlag_extension(self):
        g = GaugeStatus()
        g.apply_element(HYDRO, 1)
        g.hitlag_extension(40/FPS)
        g.time_passes(9.5)
        assert g.current_auras[HYDRO][0] != 0
        g.time_passes(41/FPS)
        assert g.current_auras[HYDRO] == [0, 0]

    def test_decay_rate_heritage(self):
        g = GaugeStatus()
        reactions = g.apply_element(DENDRO, 1)
        assert reactions == []
        assert g.current_auras[DENDRO] == [0.8, 1/11.875]
        g.apply_element(DENDRO, 2)
        assert g.current_auras[DENDRO] == [1.6, 1/11.875]

    def test_pyro_decay_rate_heritage(self):
        g = GaugeStatus()
        g.apply_element(PYRO, 1)
        assert g.current_auras[PYRO] == [0.8, 1/11.875]
        g.apply_element(PYRO, 2)
        assert g.current_auras[PYRO] == [1.6, 1/7.5]

    def test_superconduct(self):
        g = GaugeStatus()
        g.apply_element(ELECTRO, 1)
        reactions = g.apply_element(CRYO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == SUPERCONDUCT
        assert g.current_auras[ELECTRO] == [0, 0]
        assert g.current_auras[CRYO] == [0, 0]
        g.apply_element(CRYO, 2)
        reactions = g.apply_element(ELECTRO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == SUPERCONDUCT
        assert g.current_auras[ELECTRO] == [0, 0]
        is_close(g.current_auras[CRYO], [0.6, 1/7.5], 1e-4)

    def test_overload(self):
        g = GaugeStatus()
        g.apply_element(ELECTRO, 1)
        reactions = g.apply_element(PYRO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == OVERLOAD
        assert g.current_auras[ELECTRO] == [0, 0]
        assert g.current_auras[PYRO] == [0, 0]
        g.apply_element(PYRO, 2)
        reactions = g.apply_element(ELECTRO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == OVERLOAD
        assert g.current_auras[ELECTRO] == [0, 0]
        is_close(g.current_auras[PYRO], [0.6, 1/7.5], 1e-4)

    def test_forward_melt(self):
        g = GaugeStatus()
        g.apply_element(CRYO, 2)
        reactions = g.apply_element(PYRO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == FORWARD
        assert reactions[0][1] == 2
        assert g.current_auras[CRYO] == [0, 0]
        assert g.current_auras[PYRO] == [0, 0]

    def test_forward_vape(self):
        g = GaugeStatus()
        g.apply_element(PYRO, 2)
        reactions = g.apply_element(HYDRO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == FORWARD
        assert reactions[0][1] == 2
        assert g.current_auras[HYDRO] == [0, 0]
        assert g.current_auras[PYRO] == [0, 0]

    def test_forward_bloom(self):
        g = GaugeStatus()
        g.apply_element(HYDRO, 2)
        reactions = g.apply_element(DENDRO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == BLOOM
        assert isinstance(reactions[0][3], DendroCore)
        assert g.current_auras[HYDRO] == [0, 0]
        assert g.current_auras[PYRO] == [0, 0]
        dendrocore = reactions[0][3]
        c = Character()
        dendrocore.set_summoner(c)
        assert not dendrocore.dmg_stats_ready
        dendrocore.time_passes(6)
        assert dendrocore.dmg_stats_ready
        assert dendrocore.timedout

    def test_reverse_melt(self):
        g = GaugeStatus()
        g.apply_element(PYRO, 2)
        reactions = g.apply_element(CRYO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == REVERSE
        assert reactions[0][1] == 1.5
        assert g.current_auras[CRYO] == [0, 0]
        is_close(g.current_auras[PYRO][0], 1.1)

    def test_reverse_vape(self):
        g = GaugeStatus()
        g.apply_element(HYDRO, 1)
        reactions = g.apply_element(PYRO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == REVERSE
        assert reactions[0][1] == 1.5
        assert g.current_auras[PYRO] == [0, 0]
        is_close(g.current_auras[HYDRO][0], 0.3)

    def test_reverse_bloom(self):
        g = GaugeStatus()
        g.apply_element(DENDRO, 1)
        reactions = g.apply_element(HYDRO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == BLOOM
        assert reactions[0][1] == 0
        assert g.current_auras[HYDRO] == [0, 0]
        is_close(g.current_auras[DENDRO][0], 0.3)
        assert isinstance(reactions[0][3], DendroCore)

    def test_freeze(self):
        g = GaugeStatus()
        g.apply_element(CRYO, 2)
        reactions = g.apply_element(HYDRO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == FROZEN
        assert g.current_auras[HYDRO] == [0, 0]
        is_close(g.current_auras[CRYO][0], 0.6)
        is_close(g.current_auras[FROZEN][0], 2)
        frozen_duration = 2 * pow(5*2 + 4, 1/2) - 4
        g.time_passes(frozen_duration - 0.001)
        assert g.current_auras[FROZEN] != [0, 0]
        g.time_passes(0.002)
        assert g.current_auras[FROZEN] == [0, 0]
        g.time_passes(5)
        assert g.current_auras[CRYO] == [0, 0]
        g.apply_element(HYDRO, 1)
        g.apply_element(CRYO, 1)
        assert g.current_auras[HYDRO] == [0, 0]
        assert g.current_auras[CRYO] == [0, 0]
        is_close(g.current_auras[FROZEN][0], 1.6)
        frozen_duration = 2 * pow(5*1.6 + 4, 1/2) - 4
        g.time_passes(frozen_duration - 0.001)
        assert g.current_auras[FROZEN] != [0, 0]
        g.time_passes(0.002)
        assert g.current_auras[FROZEN] == [0, 0]

    def test_quicken(self):
        g = GaugeStatus()
        g.apply_element(ELECTRO, 2)
        reactions = g.apply_element(DENDRO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == QUICKEN
        assert g.current_auras[DENDRO] == [0, 0]
        is_close(g.current_auras[ELECTRO][0], 0.6)
        is_close(g.current_auras[QUICKEN][0], 1)
        quicken_duration = 11
        g.time_passes(quicken_duration - 0.001)
        assert g.current_auras[QUICKEN] != [0, 0]
        g.time_passes(0.002)
        assert g.current_auras[QUICKEN] == [0, 0]
        g.time_passes(5)
        assert g.current_auras[ELECTRO] == [0, 0]
        g.apply_element(DENDRO, 1)
        g.apply_element(ELECTRO, 1)
        assert g.current_auras[DENDRO] == [0, 0]
        assert g.current_auras[ELECTRO] == [0, 0]
        is_close(g.current_auras[QUICKEN][0], 0.8)
        quicken_duration = 5*0.8 + 6
        g.time_passes(quicken_duration - 0.001)
        assert g.current_auras[QUICKEN] != [0, 0]
        g.time_passes(0.002)
        assert g.current_auras[QUICKEN] == [0, 0]

    def test_aggravate(self):
        g = GaugeStatus()
        g.apply_element(ELECTRO, 2)
        g.apply_element(DENDRO, 1)
        reactions = g.apply_element(ELECTRO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == AGGRAVATE
        assert reactions[0][1] == 1.15
        assert g.current_auras[QUICKEN][0] == 1
        assert g.current_auras[ELECTRO][0] == 0.8
        reactions = g.apply_element(DENDRO, 2)
        assert len(reactions) == 2
        assert reactions[1][0] == QUICKEN
        assert g.current_auras[QUICKEN][0] == 1
        reactions = g.apply_element(ELECTRO, 2)
        assert reactions[0][0] == AGGRAVATE
        assert g.current_auras[ELECTRO][0] == 1.6

    def test_spread(self):
        g = GaugeStatus()
        g.apply_element(DENDRO, 2)
        g.apply_element(ELECTRO, 1)
        reactions = g.apply_element(DENDRO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == SPREAD
        assert reactions[0][1] == 1.25
        assert g.current_auras[QUICKEN][0] == 1
        assert g.current_auras[DENDRO][0] == 0.8
        reactions = g.apply_element(ELECTRO, 2)
        assert len(reactions) == 2
        assert reactions[1][0] == QUICKEN
        assert g.current_auras[QUICKEN][0] == 1
        reactions = g.apply_element(DENDRO, 2)
        assert reactions[0][0] == SPREAD
        assert g.current_auras[DENDRO][0] == 1.6

    def test_swirl_crystallize_st(self):
        g = GaugeStatus()
        g.apply_element(ELECTRO, 2)
        reactions = g.apply_element(ANEMO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == ELECTRO_SWIRL
        assert g.current_auras[ELECTRO][0] == 1.1
        reactions = g.apply_element(GEO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == ELECTRO_CRYSTALLIZE
        is_close(g.current_auras[ELECTRO][0], 0.6)
        g.time_passes(7.5)
        reactions = g.apply_element(DENDRO, 1)
        assert len(reactions) == 0
        reactions = g.apply_element(ANEMO, 1)
        assert len(reactions) == 0
        reactions = g.apply_element(GEO, 1)
        assert len(reactions) == 0
        assert g.current_auras[DENDRO][0] == 0.8

    def test_swirl_aoe(self):
        g = GaugeStatus()
        g.apply_element(HYDRO, 1)
        reactions = g.apply_element(ANEMO, 1)
        is_close(g.current_auras[HYDRO][0], 0.3)
        swirl_aura, gu = reactions[0][4]
        assert swirl_aura == HYDRO
        assert gu == 2.2
        g.apply_element(CRYO, 1)
        reactions = g.apply_element(ANEMO, 1)
        is_close(g.current_auras[FROZEN][0], .1)
        assert reactions[0][0] == CRYO_SWIRL
        swirl_aura, gu = reactions[0][4]
        assert swirl_aura == CRYO
        is_close(gu, 2.2)
        g.time_passes(5)
        g.apply_element(DENDRO, 2)
        reactions = g.apply_element(PYRO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == BURNING
        g.apply_element(CRYO, 2)
        is_close(g.current_auras[BURNING][0], 1.0)
        is_close(g.current_auras[PYRO][0], 0)
        is_close(g.current_auras[DENDRO][0], 1.5)
        reactions = g.apply_element(ANEMO, 2)
        assert reactions[0][0] == PYRO_SWIRL
        swirl_aura, gu = reactions[0][4]
        assert swirl_aura == PYRO
        is_close(gu, 2.2)

    def test_electro_charged(self):
        g = GaugeStatus()
        g.apply_element(HYDRO, 1)
        reactions = g.apply_element(ELECTRO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == ELECTRO_CHARGED
        assert reactions[0][1] == 1.2
        assert g.current_auras[HYDRO][0] == 0.4
        assert g.current_auras[ELECTRO][0] == 0.4
        electrocharged = reactions[0][3]
        assert isinstance(electrocharged, ElectroCharged)
        c1 = Character()
        c1.em = 10
        electrocharged.set_summoner(c1)
        assert electrocharged.em == 10
        electrocharged.time_passes(0.5)
        assert not electrocharged.dmg_stats_ready
        assert g.current_auras[HYDRO][0] == 0.4
        assert g.current_auras[ELECTRO][0] == 0.4
        reactions = g.apply_element(HYDRO, 1)
        assert reactions[0][0] == ELECTRO_CHARGED
        assert reactions[0][1] == 0
        assert g.current_auras[HYDRO][0] == 0.8
        c2 = Character()
        c2.em = 20
        electrocharged.set_summoner(c2)
        assert electrocharged.em == 20
        electrocharged.time_passes(0.5001)
        assert electrocharged.dmg_stats_ready
        electrocharged.time_passes(0.001)
        assert electrocharged.timedout
        assert not electrocharged.dmg_stats_ready
        assert g.current_auras[HYDRO][0] == 0.4
        assert g.current_auras[ELECTRO][0] == 0.0

    def test_burning(self):
        g = GaugeStatus()
        g.apply_element(PYRO, 1)
        reactions = g.apply_element(DENDRO, 2)
        assert len(reactions) == 1
        assert reactions[0][0] == BURNING
        assert reactions[0][1] == 0.25
        assert g.current_auras[PYRO][0] == 1.0
        assert g.current_auras[DENDRO][0] == 1.5
        assert g.current_auras[BURNING] == [2, 0]
        burning = reactions[0][3]
        assert isinstance(burning, Burning)
        c1 = Character()
        c1.em = 10
        burning.set_summoner(c1)
        assert burning.em == 10
        burning.time_passes(0.24999)
        assert not burning.dmg_stats_ready
        burning.time_passes(0.001)
        assert burning.dmg_stats_ready
        g.time_passes(0.5)
        assert g.current_auras[DENDRO][0] == 1.4
        assert g.current_auras[PYRO][0] != 1.0
        assert g.current_auras[BURNING] == [2, 0]
        burning.time_passes(0.001)
        assert not burning.dmg_stats_ready
        reactions = g.apply_element(PYRO, 1)
        assert reactions[0][0] == BURNING
        assert reactions[0][1] == 0
        assert g.current_auras[PYRO][0] == 0.8
        c2 = Character()
        c2.em = 20
        burning.set_summoner(c2)
        assert burning.em == 20
        burning.time_passes(0.25)
        assert burning.dmg_stats_ready
        is_close(g.current_auras[DENDRO][0], 1.3)
        assert not burning.timedout
        burning.time_passes(0.001)
        assert not burning.dmg_stats_ready
        burning.time_passes(1.5)
        # Doesn't supposed to be like that but should be fine, if we take smaller dt
        is_close(g.current_auras[DENDRO][0], 1.2)
        assert burning.dmg_stats_ready
        assert g.current_auras[PYRO][0] == 1.0
        assert burning.pyro_app_icd == 2

    def test_electro_hydro(self):
        g = GaugeStatus()
        g.apply_element(ELECTRO, 1)
        g.apply_element(HYDRO, 1)
        reactions = g.apply_element(PYRO, 1)
        assert len(reactions) == 2
        assert reactions[0][0] == OVERLOAD
        assert reactions[1][0] == REVERSE
        is_close(g.current_auras[HYDRO][0], 0.1)
        assert g.current_auras[ELECTRO] == [0, 0]
        g.time_passes(4)
        g.apply_element(ELECTRO, 1)
        g.apply_element(HYDRO, 1)
        reactions = g.apply_element(CRYO, 1)
        assert len(reactions) == 2
        assert reactions[0][0] == SUPERCONDUCT
        assert reactions[1][0] == FROZEN
        assert g.current_auras[HYDRO] == [0, 0]
        assert g.current_auras[ELECTRO] == [0, 0]
        assert g.current_auras[FROZEN][0] == 0.8
        g.time_passes(4)
        g.apply_element(ELECTRO, 1)
        g.apply_element(HYDRO, 4)
        reactions = g.apply_element(DENDRO, 1)
        assert len(reactions) == 3
        assert reactions[0][0] == QUICKEN
        assert reactions[1][0] == BLOOM
        assert reactions[2][0] == BLOOM
        is_close(g.current_auras[HYDRO][0], 0.8)
        assert g.current_auras[DENDRO] == [0, 0]
        assert g.current_auras[ELECTRO] == [0, 0]
        assert g.current_auras[QUICKEN] == [0, 0]
        g.apply_element(ELECTRO, 1)
        g.apply_element(HYDRO, 4)
        reactions = g.apply_element(ANEMO, 1)
        assert len(reactions) == 2
        assert reactions[0][0] == ELECTRO_SWIRL
        assert reactions[1][0] == HYDRO_SWIRL

    def test_quicken_electro(self):
        g = GaugeStatus()
        g.apply_element(ELECTRO, 2)
        g.apply_element(DENDRO, 1)
        g.time_passes(1)
        reactions = g.apply_element(HYDRO, 2)
        assert len(reactions) == 2
        assert reactions[0][0] == BLOOM
        assert reactions[1][0] == ELECTRO_CHARGED
        g.time_passes(5)
        g.apply_element(ELECTRO, 2)
        g.apply_element(DENDRO, 1)
        reactions = g.apply_element(PYRO, 1)
        assert len(reactions) == 2
        assert reactions[0][0] == OVERLOAD
        assert reactions[1][0] == BURNING
        assert g.current_auras[QUICKEN][0] == 0.9
        assert g.current_auras[PYRO][0] == 1.0
        assert g.current_auras[DENDRO] == [0, 0]
        burning = reactions[1][3]
        assert isinstance(burning, Burning)
        burning.time_passes(0.26)
        is_close(g.current_auras[QUICKEN][0], 0.8)
        assert g.current_auras[DENDRO] == [0, 0]

    def test_quicken_dendro(self):
        g = GaugeStatus()
        g.apply_element(DENDRO, 2)
        g.apply_element(ELECTRO, 1)
        reactions = g.apply_element(PYRO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == BURNING
        is_close(g.current_auras[DENDRO][0], 0.5)
        is_close(g.current_auras[QUICKEN][0], 0.9)
        burning = reactions[0][3]
        assert isinstance(burning, Burning)
        burning.time_passes(0.26)
        is_close(g.current_auras[DENDRO][0], 0.4)
        is_close(g.current_auras[QUICKEN][0], 0.8)
        reactions = g.apply_element(HYDRO, 2)
        assert len(reactions) == 2
        assert reactions[0][0] == FORWARD
        assert reactions[1][0] == BLOOM
        is_close(g.current_auras[QUICKEN][0], 0.3)

    def test_dendro_cryo(self):
        g = GaugeStatus()
        g.apply_element(DENDRO, 1)
        reactions = g.apply_element(CRYO, 1)
        assert len(reactions) == 0
        reactions = g.apply_element(PYRO, 1)
        assert len(reactions) == 2
        assert reactions[0][0] == FORWARD
        assert reactions[1][0] == BURNING
        assert g.current_auras[CRYO] == [0, 0]
        reactions = g.apply_element(CRYO, 4)
        assert len(reactions) == 1
        assert reactions[0][0] == REVERSE
        assert g.current_auras[BURNING] == [0, 0]
        assert g.current_auras[PYRO] == [0, 0]
        is_close(g.current_auras[DENDRO][0], 0.7)
        g.apply_element(CRYO, 1)
        reactions = g.apply_element(ELECTRO, 1)
        assert len(reactions) == 2
        assert reactions[0][0] == SUPERCONDUCT
        assert reactions[1][0] == QUICKEN
        assert g.current_auras[CRYO] == [0, 0]
        g.current_auras[QUICKEN] = [0, 0]
        g.apply_element(DENDRO, 1)
        g.apply_element(CRYO, 1)
        reactions = g.apply_element(HYDRO, 1)
        assert len(reactions) == 2
        assert reactions[0][0] == FROZEN
        assert reactions[1][0] == BLOOM

    def test_cryo_quicken(self):
        g = GaugeStatus()
        g.current_auras[QUICKEN] = [0.8, 0]
        reactions = g.apply_element(CRYO, 1)
        assert len(reactions) == 0
        reactions = g.apply_element(PYRO, 1)
        assert len(reactions) == 2
        assert reactions[0][0] == FORWARD
        assert reactions[1][0] == BURNING
        assert g.current_auras[CRYO] == [0, 0]
        reactions = g.apply_element(CRYO, 4)
        assert len(reactions) == 1
        assert reactions[0][0] == REVERSE
        assert g.current_auras[BURNING] == [0, 0]
        assert g.current_auras[PYRO] == [0, 0]
        is_close(g.current_auras[QUICKEN][0], 0.7)
        g.apply_element(CRYO, 1)
        reactions = g.apply_element(ELECTRO, 1)
        assert len(reactions) == 2
        assert reactions[0][0] == AGGRAVATE
        assert reactions[1][0] == SUPERCONDUCT
        assert g.current_auras[CRYO] == [0, 0]
        is_close(g.current_auras[QUICKEN][0], 0.7)
        g.apply_element(CRYO, 1)
        reactions = g.apply_element(HYDRO, 1)
        assert len(reactions) == 2
        assert reactions[0][0] == FROZEN
        assert reactions[1][0] == BLOOM

    def test_dendro_cryo_quicken(self):
        g = GaugeStatus()
        g.apply_element(DENDRO, 2)
        g.apply_element(ELECTRO, 1)
        reactions = g.apply_element(CRYO, 1)
        assert len(reactions) == 0
        reactions = g.apply_element(PYRO, 1)
        assert len(reactions) == 2
        assert reactions[0][0] == FORWARD
        assert reactions[1][0] == BURNING
        assert g.current_auras[CRYO] == [0, 0]
        is_close(g.current_auras[DENDRO][0], 0.5)
        is_close(g.current_auras[QUICKEN][0], 0.9)
        burning = reactions[1][3]
        assert isinstance(burning, Burning)
        burning.time_passes(0.26)
        is_close(g.current_auras[DENDRO][0], 0.4)
        is_close(g.current_auras[QUICKEN][0], 0.8)
        reactions = g.apply_element(CRYO, 4)
        assert len(reactions) == 1
        assert reactions[0][0] == REVERSE
        assert g.current_auras[BURNING] == [0, 0]
        assert g.current_auras[PYRO] == [0, 0]
        is_close(g.current_auras[QUICKEN][0], 0.8)
        g.apply_element(CRYO, 1)
        reactions = g.apply_element(ELECTRO, 1)
        assert len(reactions) == 3
        assert reactions[0][0] == AGGRAVATE
        assert reactions[1][0] == SUPERCONDUCT
        assert reactions[2][0] == QUICKEN
        assert g.current_auras[CRYO] == [0, 0]
        is_close(g.current_auras[QUICKEN][0], 0.8)
        is_close(g.current_auras[DENDRO][0], 0.2)
        g.apply_element(CRYO, 1)
        reactions = g.apply_element(HYDRO, 1)
        assert len(reactions) == 2
        assert reactions[0][0] == FROZEN
        assert reactions[1][0] == BLOOM
        assert g.current_auras[CRYO] == [0, 0]
        is_close(g.current_auras[FROZEN][0], 1.6)
        is_close(g.current_auras[DENDRO][0], 0.1)
        is_close(g.current_auras[QUICKEN][0], 0.7)

    def test_frozen_cryo_dendro(self):
        g = GaugeStatus()
        g.apply_element(CRYO, 2)
        g.apply_element(HYDRO, 1)
        g.apply_element(DENDRO, 1)
        reactions = g.apply_element(PYRO, 2)
        assert len(reactions) == 2
        assert reactions[0][0] == FORWARD
        assert reactions[1][0] == BURNING
        assert g.current_auras[FROZEN] == [0, 0]
        assert g.current_auras[CRYO] == [0, 0]
        reactions = g.apply_element(CRYO, 4)
        assert len(reactions) == 1
        assert reactions[0][0] == REVERSE
        assert g.current_auras[BURNING] == [0, 0]
        assert g.current_auras[PYRO] == [0, 0]
        is_close(g.current_auras[DENDRO][0], 0.7)
        g.time_passes(9.5)
        g.apply_element(CRYO, 2)
        g.apply_element(HYDRO, 1)
        g.apply_element(DENDRO, 2)
        reactions = g.apply_element(ELECTRO, 4)
        assert len(reactions) == 2
        assert reactions[0][0] == SUPERCONDUCT
        assert reactions[1][0] == QUICKEN
        assert g.current_auras[CRYO] == [0, 0]
        assert g.current_auras[FROZEN] == [0, 0]
        is_close(g.current_auras[QUICKEN][0], 1.4)
        is_close(g.current_auras[DENDRO][0], 0.2)
        g.time_passes(15)
        g.apply_element(CRYO, 2)
        g.apply_element(HYDRO, 1)
        g.apply_element(DENDRO, 1)
        reactions = g.apply_element(HYDRO, 1)
        assert len(reactions) == 2
        assert reactions[0][0] == FROZEN
        assert reactions[1][0] == BLOOM
        assert g.current_auras[CRYO] == [0, 0]
        is_close(g.current_auras[FROZEN][0], 2)
        is_close(g.current_auras[DENDRO][0], 0.6)

    def test_frozen_hydro(self):
        g = GaugeStatus()
        g.apply_element(HYDRO, 2)
        g.apply_element(CRYO, 1)
        reactions = g.apply_element(PYRO, 2)
        assert len(reactions) == 1
        assert reactions[0][0] == FORWARD
        assert g.current_auras[FROZEN] == [0, 0]
        is_close(g.current_auras[HYDRO][0], 0.6)
        g.time_passes(7.5)
        g.apply_element(HYDRO, 2)
        g.apply_element(CRYO, 1)
        reactions = g.apply_element(ELECTRO, 4)
        assert len(reactions) == 1
        assert reactions[0][0] == SUPERCONDUCT
        assert g.current_auras[FROZEN] == [0, 0]
        is_close(g.current_auras[HYDRO][0], 0.6)
        g.time_passes(7.5)
        g.apply_element(HYDRO, 2)
        g.apply_element(CRYO, 1)
        reactions = g.apply_element(ANEMO, 2)
        assert len(reactions) == 2
        assert reactions[0][0] == HYDRO_SWIRL
        assert reactions[1][0] == CRYO_SWIRL

    def test_frozen_cryo(self):
        g = GaugeStatus()
        g.apply_element(CRYO, 2)
        g.apply_element(HYDRO, 1)
        reactions = g.apply_element(PYRO, 2)
        assert len(reactions) == 1
        assert reactions[0][0] == FORWARD
        assert g.current_auras[FROZEN] == [0, 0]
        assert g.current_auras[CRYO] == [0, 0]
        g.apply_element(CRYO, 2)
        g.apply_element(HYDRO, 1)
        reactions = g.apply_element(ELECTRO, 2)
        assert len(reactions) == 1
        assert reactions[0][0] == SUPERCONDUCT
        is_close(g.current_auras[FROZEN][0], 0.6)
        g.time_passes(7.5)
        g.apply_element(CRYO, 2)
        g.apply_element(HYDRO, 1)
        reactions = g.apply_element(ANEMO, 2)
        assert len(reactions) == 1
        assert reactions[0][0] == CRYO_SWIRL
        is_close(g.current_auras[FROZEN][0], 1.6)

    def test_burning_multiaura(self):
        g = GaugeStatus()
        g.apply_element(DENDRO, 1)
        g.apply_element(PYRO, 1)
        reactions = g.apply_element(ELECTRO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == OVERLOAD
        assert g.current_auras[PYRO] == [0, 0]
        is_close(g.current_auras[BURNING][0], 1)
        g.apply_element(PYRO, 1)
        reactions = g.apply_element(ANEMO, 1)
        assert len(reactions) == 1
        assert reactions[0][0] == PYRO_SWIRL
        is_close(g.current_auras[PYRO][0], 0.3)
        is_close(g.current_auras[BURNING][0], 0.5)

class TestResonances:
    c1 = Character()
    c2 = Character()
    c3 = Character()
    c4 = Character()
    c1.em = 100
    c2.all_cr += 0.3
    c3.em = 40
    team = [c1, c2, c3, c4]
    enemy = [Enemy()]
    c1.set_team(team)
    c1.set_enemies(enemy)
    c2.set_team(team)
    c2.set_enemies(enemy)
    c3.set_team(team)
    c3.set_enemies(enemy)
    c4.set_team(team)
    c4.set_enemies(enemy)

    def test_electro_resonance(self):
        electro_resonance = ElectroResonance(self.c1)
        assert electro_resonance.particle_set == None
        electro_resonance.time_passes(5)
        assert electro_resonance.particle_set == None
        electro_resonance.notify(Event(event_type=REACTION, reaction=ELECTRO_CHARGED))
        assert electro_resonance.particle_set != None
        electro_resonance.time_passes(0.1)
        assert electro_resonance.particle_set != None
        assert electro_resonance.particle_set.element == ELECTRO
        assert electro_resonance.particle_set.n_particles == 1
        particle_set = electro_resonance.particle_set
        assert isinstance(particle_set, ParticleSet)
        electro_resonance.time_passes(1.21)
        particle_set.time_passes(1.21)
        assert electro_resonance.particle_set == None
        assert particle_set.timedout
        electro_resonance.notify(Event(event_type=REACTION, reaction=AGGRAVATE))
        assert electro_resonance.particle_set == None
        electro_resonance.time_passes(4)
        electro_resonance.notify(Event(event_type=REACTION, reaction=QUICKEN))
        assert electro_resonance.particle_set != None

    def test_cryo_resonance(self):
        cryo_resonance = CryoResonance(self.c1)
        self.enemy[0].gauge_status.current_auras[CRYO] = [1, 0]
        cryo_resonance.notify(Event(event_type=CHARACTER_ATTACKS, character_one=self.c1, enemy=self.enemy[0]))
        assert self.c1.all_cr == 0.2
        cryo_resonance.notify(Event(event_type=CHARACTER_HITS, character_one=self.c1, enemy=self.enemy[0]))
        is_close(self.c1.all_cr, 0.05)
        self.enemy[0].gauge_status.current_auras[CRYO] = [0, 0]
        self.enemy[0].gauge_status.current_auras[FROZEN] = [1, 0]
        cryo_resonance.notify(Event(event_type=CHARACTER_ATTACKS, character_one=self.c2, enemy=self.enemy[0]))
        is_close(self.c2.all_cr, 0.5)
        cryo_resonance.notify(Event(event_type=CHARACTER_HITS, character_one=self.c2, enemy=self.enemy[0]))
        is_close(self.c2.all_cr, 0.35)

    def test_geo_resonance(self):
        geo_resonance = GeoResonance(self.c1)
        assert self.c1.all_dmg_bonus == 0
        assert self.c2.all_dmg_bonus == 0
        assert self.c3.all_dmg_bonus == 0
        assert self.c4.all_dmg_bonus == 0
        self.c1.on_field = True
        self.c1.is_shielded = True
        self.c2.is_shielded = True
        geo_resonance.time_passes(0.01)
        assert self.c1.all_dmg_bonus == 0.15
        assert self.c2.all_dmg_bonus == 0
        self.c1.on_field = False
        self.c2.on_field = True
        geo_resonance.time_passes(0.01)
        assert self.c1.all_dmg_bonus == 0
        assert self.c2.all_dmg_bonus == 0.15
        assert self.c3.all_dmg_bonus == 0
        geo_resonance.notify(Event(event_type=CHARACTER_HITS, character_one=self.c2, enemy=self.enemy[0]))
        assert self.enemy[0].resistance[GEO] == -.1
        geo_resonance.notify(Event(event_type=CHARACTER_HITS, character_one=self.c1, enemy=self.enemy[0]))
        assert self.enemy[0].resistance[GEO] == -.1
        geo_resonance.time_passes(10)
        assert self.enemy[0].resistance[GEO] == -.1
        assert self.c1.all_dmg_bonus == 0
        assert self.c2.all_dmg_bonus == 0.15
        assert geo_resonance.res_shred_dict[self.enemy[0]][0]
        assert geo_resonance.res_shred_dict[self.enemy[0]][1] == 5
        geo_resonance.notify(Event(event_type=CHARACTER_HITS, character_one=self.c1, enemy=self.enemy[0]))
        assert self.enemy[0].resistance[GEO] == -.1
        assert geo_resonance.res_shred_dict[self.enemy[0]][1] == 15
        geo_resonance.time_passes(16)
        assert self.enemy[0].resistance[GEO] == .1
        assert not geo_resonance.res_shred_dict[self.enemy[0]][0]
        assert geo_resonance.res_shred_dict[self.enemy[0]][1] == 0

    def test_dendro_resonance(self):
        dendro_resonance = DendroResonance(self.c1)
        dendro_resonance.notify(Event(event_type=REACTION, reaction=QUICKEN))
        dendro_resonance.time_passes(2)
        assert dendro_resonance.bqb_em_timer == 4
        assert self.c1.em == 130
        assert self.c2.em == 30
        dendro_resonance.notify(Event(event_type=REACTION, reaction=BLOOM))
        assert dendro_resonance.bqb_em_timer == 6
        assert self.c1.em == 130
        assert self.c2.em == 30
        dendro_resonance.notify(Event(event_type=REACTION, reaction=HYPERBLOOM))
        dendro_resonance.time_passes(1)
        assert dendro_resonance.ashb_em_timber == 5
        assert dendro_resonance.bqb_em_timer == 5
        assert self.c1.em == 150
        assert self.c2.em == 50

if __name__ == "__main__":
    t = TestResonances()
    t.test_geo_resonance()