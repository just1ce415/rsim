from src.constants import *
from src.entities.entity import Entity

from typing import List

class GaugeStatus(Entity):
    def __init__(self):
        """
        :params:
        current_auras - {ELEMENT: [GU, decay_rate]}
        decay_rate - 1/11.875 (GU per sec) for A, etc.
        """
        self.current_auras = {
            ANEMO: [0, 0],
            HYDRO: [0, 0],
            ELECTRO: [0, 0],
            DENDRO: [0, 0],
            CRYO: [0, 0],
            PYRO: [0, 0],
            GEO: [0, 0],
            FROZEN: [0, 0],
            QUICKEN: [0, 0],
            BURNING: [0, 0]
        }

    def time_passes(self, seconds: float):
        for key, value in self.current_auras.items():
            # Dendro does not decay while burning
            if value[1] != 0 and ((key != DENDRO and key != QUICKEN) or self.current_auras[BURNING] == [0, 0]):
                gu_decayed = seconds * value[1]
                self.current_auras[key][0] -= gu_decayed
                if self.current_auras[key][0] <= 0:
                    self.current_auras[key][0] = 0
                    self.current_auras[key][1] = 0

    def hitlag_extension(self, seconds: float):
        """
        Auras are extendable by hitlag
        """
        for key, value in self.current_auras.items():
            if value[1] != 0:
                gu_recovered = seconds * value[1]
                self.current_auras[key][0] += gu_recovered

    def apply_element(self, element:str, gu:float) -> List[str]:
        """
        Returns the following nested list:
        [[reaction, special_multiplier, level_multiplier_factor, summon, response_application], [...], ...]
        reaction - name of the reaction
        special_multiplier - special multiplier of the triggered reaction:
        1.5 - reverse vape/melt
        2 - forward vape/melt
        0.6 - swirl
        1.15 - aggravate
        1.25 - spread
        1.2 - EC, first tik
        0.25 - burning, first tik
        0.5 - superconduct
        2 - overload
        level_multiplier_factor - 0 or 1; whether reaction requires level multiplier or no
        summon - None or summon object: DendroCore, ElectroCharged, Burning. If Burning or EC was retriggered,
        summon is None
        responce application - List[element, gu] - element and gauge units of the response
        application in case of swirl
        """
        from src.entities.summons_and_adaptives.reaction_summons import DendroCore
        reactions = []
        if gu <= 0:
            return reactions
        if element == ANEMO:
            if self.current_auras[ELECTRO] != [0, 0]:
                reactions, gu = self.__swirl(reactions, ELECTRO, gu)
                if gu == 0:
                    return reactions
            if self.current_auras[PYRO] != [0, 0]:
                # Anemo consume burning and pyro at the same time and triggers only pyro swirl
                if self.current_auras[BURNING][0] != 0:
                    self.current_auras[BURNING][0] = max(self.current_auras[BURNING][0] - 0.5*gu, 0)
                reactions, gu = self.__swirl(reactions, PYRO, gu)
                if gu == 0:
                    return reactions
            # Implies that there was burning, but no pyro
            if self.current_auras[BURNING] != [0, 0]:
                reactions, gu = self.__swirl(reactions, BURNING, gu)
                if gu == 0:
                    return reactions
            if self.current_auras[HYDRO] != [0, 0]:
                reactions, gu = self.__swirl(reactions, HYDRO, gu)
                if gu == 0:
                    return reactions
            if self.current_auras[CRYO] != [0, 0]:
                # In case of cryo+frozen, cryo swirl occurs, and if anemo gauge is not fully consumed, frozen gauge will
                # be consumed, but no reaction will be triggered
                if 0.5*gu >= self.current_auras[CRYO][0]:
                    reactions.append([CRYO_SWIRL, 0.6, 1, None, [CRYO, (self.current_auras[CRYO][0] - 0.04) * 1.25 + 1]])
                    gu = 2*(0.5*gu - self.current_auras[CRYO][0])
                    self.current_auras[CRYO] = [0, 0]
                    if 0.5*gu >= self.current_auras[FROZEN][0]:
                        gu = 2*(0.5*gu - self.current_auras[FROZEN][0])
                        self.current_auras[FROZEN] = [0, 0]
                    else:
                        self.current_auras[FROZEN][0] -= 0.5*gu
                        gu = 0
                else:
                    reactions.append([CRYO_SWIRL, 0.6, 1, None, [CRYO, (gu - 0.04) * 1.25 + 1]])
                    self.current_auras[CRYO][0] -= 0.5 * gu
                gu = 0
                return reactions
            if self.current_auras[FROZEN] != [0, 0]:
                reactions, gu = self.__swirl(reactions, FROZEN, gu)
                if gu == 0:
                    return reactions

        elif element == HYDRO:
            application = True
            if self.current_auras[PYRO] != [0, 0]:
                application = False
                reactions.append([FORWARD, 2, 0, None, None])
                # Both burning and pyro gauges will be consumed simultaneously and trigger only one reaction
                gu_b = 100
                if self.current_auras[BURNING] != [0, 0]:
                    gu_b = self.__consume_aura(BURNING, gu, 2)
                gu = self.__consume_aura(PYRO, gu, 2)
                gu = min(gu, gu_b)
                if gu == 0:
                    return reactions
            if self.current_auras[BURNING] != [0, 0]:
                application = False
                reactions.append([FORWARD, 2, 0, None, None])
                gu = self.__consume_aura(BURNING, gu, 2)
                if gu == 0:
                    return reactions
            if self.current_auras[ANEMO] != [0, 0]:
                application = False
                if gu == 0:
                    return reactions
                reactions.append([HYDRO_SWIRL, 0.6, 1, None, [HYDRO, (gu - 0.04) * 1.25 + 1]])
                gu = 0
                return reactions
            if self.current_auras[CRYO] != [0, 0]:
                application = False
                reactions.append([FROZEN, 0, 0, None, None])
                gu = self.__freeze(CRYO, gu)
                if gu == 0:
                    return reactions
            if self.current_auras[DENDRO] != [0, 0]:
                application = False
                # Hydro will consume dendro and quicken simulteneously
                gu_q = 100
                if self.current_auras[QUICKEN] != [0, 0]:
                    gu_q = self.__consume_aura(QUICKEN, gu, 0.5)
                gu = self.__consume_aura(DENDRO, gu, 0.5)
                gu = min(gu, gu_q)
                reactions.append([BLOOM, 0, 0, DendroCore(), None])
                if gu == 0:
                    return reactions
            # Implies that quicken was without dendro
            if self.current_auras[QUICKEN] != [0, 0]:
                application = False
                gu = self.__consume_aura(QUICKEN, gu, 0.5)
                reactions.append([BLOOM, 0, 0, DendroCore(), None])
                if gu == 0:
                    return reactions
            if self.current_auras[ELECTRO] != [0, 0]:
                application = False
                return self.__electro_charged(reactions, ELECTRO, HYDRO, gu)
            if application:
                self.__pure_application(HYDRO, gu)

        elif element == ELECTRO:
            application = True
            ## Aggravate does not consume quicken and lets trigger just to be applied
            if self.current_auras[QUICKEN] != [0, 0]:
                reactions.append([AGGRAVATE, 1.15, 1, None, None])
            if self.current_auras[PYRO] != [0, 0]:
                application = False
                reactions.append([OVERLOAD, 2, 1, None, None])
                gu_b = 100
                if self.current_auras[BURNING] != [0, 0]:
                    gu_b = self.__consume_aura(BURNING, gu, 1)
                gu = self.__consume_aura(PYRO, gu, 1)
                gu = min(gu, gu_b)
                if gu == 0:
                    return reactions
            if self.current_auras[ANEMO] != [0, 0]:
                application = False
                if gu == 0:
                    return reactions
                reactions.append([ELECTRO_SWIRL, 0.6, 1, None, [ELECTRO, (gu - 0.04) * 1.25 + 1]])
                gu = 0
                return reactions
            if self.current_auras[HYDRO] != [0, 0]:
                if self.current_auras[FROZEN] == [0, 0]:
                    application = False
                    return self.__electro_charged(reactions, HYDRO, ELECTRO, gu)
            if self.current_auras[CRYO] != [0, 0]:
                application = False
                reactions.append([SUPERCONDUCT, 0.5, 1, None, None])
                # Consumes cryo and then frozen if electro gauge is fully consumed, but only 1 superconduct occurs
                gu = self.__consume_aura(CRYO, gu, 1)
                if self.current_auras[FROZEN] != [0, 0] and gu != 0:
                    gu = self.__consume_aura(FROZEN, gu, 1)
                if gu == 0:
                    return reactions
            # Implies there was no cryo, only frozen
            if self.current_auras[FROZEN] != [0, 0]:
                application = False
                reactions.append([SUPERCONDUCT, 0.5, 1, None, None])
                gu = self.__consume_aura(FROZEN, gu, 1)
                if gu == 0:
                    return reactions
            if self.current_auras[DENDRO] != [0, 0]:
                application = False
                reactions.append([QUICKEN, 0, 0, None, None])
                gu = self.__quicken(DENDRO, gu)
                if gu == 0:
                    return reactions
            if application:
                self.__pure_application(ELECTRO, gu)

        elif element == DENDRO:
            application = True
            ## Spread does not consume quicken and lets trigger just to be applied
            if self.current_auras[QUICKEN] != [0, 0]:
                reactions.append([SPREAD, 1.25, 1, None, None])
            if self.current_auras[ELECTRO] != [0, 0]:
                application = False
                reactions.append([QUICKEN, 0, 0, None, None])
                gu = self.__quicken(ELECTRO, gu)
                if gu == 0:
                    return reactions
            if self.current_auras[PYRO] != [0, 0]:
                application = False
                reactions = self.__burning(reactions, PYRO, DENDRO, gu)
                return reactions
            if self.current_auras[HYDRO] != [0, 0]:
                application = False
                reactions.append([BLOOM, 0, 0, DendroCore(), None])
                gu = self.__consume_aura(HYDRO, gu, 2)
                if self.current_auras[QUICKEN] != [0, 0]:
                    reactions.append([BLOOM, 0, 0, DendroCore(), None])
                    if 2*self.current_auras[QUICKEN][0] > self.current_auras[HYDRO][0]:
                        self.current_auras[QUICKEN][0] = (2*self.current_auras[QUICKEN][0] - self.current_auras[HYDRO][0]) * 0.5
                        self.current_auras[HYDRO] = [0, 0]
                    elif 2*self.current_auras[QUICKEN][0] < self.current_auras[HYDRO][0]:
                        self.current_auras[HYDRO][0] = self.current_auras[HYDRO][0] - 2*self.current_auras[QUICKEN][0]
                        self.current_auras[QUICKEN] = [0, 0]
                if gu == 0:
                    return reactions
            if application:
                self.__pure_application(DENDRO, gu)

        elif element == CRYO:
            application = True
            if self.current_auras[ELECTRO] != [0, 0]:
                application = False
                reactions.append([SUPERCONDUCT, 0.5, 1, None, None])
                gu = self.__consume_aura(ELECTRO, gu, 1)
                if gu == 0:
                    return reactions
            if self.current_auras[PYRO] != [0, 0]:
                application = False
                # Consume both pyro and burning simultaneously
                gu_b = 100
                if self.current_auras[BURNING] != [0, 0]:
                    gu_b = self.__consume_aura(BURNING, gu, 0.5)
                reactions.append([REVERSE, 1.5, 0, None, None])
                gu = self.__consume_aura(PYRO, gu, 0.5)
                gu = min(gu_b, gu)
                if gu == 0:
                    return reactions
            # Implies that there was burning without pyro
            if self.current_auras[BURNING] != [0, 0]:
                application = False
                reactions.append([REVERSE, 1.5, 0, None, None])
                gu = self.__consume_aura(BURNING, gu, 0.5)
                if gu == 0:
                    return reactions
            if self.current_auras[ANEMO] != [0, 0]:
                application = False
                reactions.append([CRYO_SWIRL, 0.6, 1, None, [CRYO, (gu - 0.04) * 1.25 + 1]])
                gu = 0
                return reactions
            if self.current_auras[HYDRO] != [0, 0]:
                application = False
                reactions.append([FROZEN, 0, 0, None, None])
                gu = self.__freeze(HYDRO, gu)
                if gu == 0:
                    return reactions
            if application:
                self.__pure_application(CRYO, gu)

        elif element == PYRO:
            application = True
            if self.current_auras[ELECTRO] != [0, 0]:
                application = False
                reactions.append([OVERLOAD, 2, 1, None, None])
                gu = self.__consume_aura(ELECTRO, gu, 1)
                if gu == 0:
                    return reactions
            if self.current_auras[ANEMO] != [0, 0]:
                application = False
                reactions.append([PYRO_SWIRL, 0.6, 1, None, [PYRO, (gu - 0.04) * 1.25 + 1]])
                gu = 0
                return reactions
            if self.current_auras[HYDRO] != [0, 0]:
                application = False
                # By applying pyro on hydro+frozen you trigger only melt
                if self.current_auras[FROZEN] == [0, 0]:
                    reactions.append([REVERSE, 1.5, 0, None, None])
                    gu = self.__consume_aura(HYDRO, gu, 0.5)
            if self.current_auras[CRYO] != [0, 0]:
                application = False
                reactions.append([FORWARD, 2, 0, None, None])
                # Frozen and cryo are consumed simultaneosly
                gu_f = 100
                if self.current_auras[FROZEN] != [0, 0]:
                    gu_f = self.__consume_aura(FROZEN, gu, 2)
                gu = self.__consume_aura(CRYO, gu, 2)
                gu = min(gu, gu_f)
                if gu == 0:
                    return reactions
            # Implies frozen without cryo
            if self.current_auras[FROZEN] != [0, 0]:
                application = False
                reactions.append([FORWARD, 2, 0, None, None])
                gu = self.__consume_aura(FROZEN, gu, 2)
                if gu == 0:
                    return reactions
            if self.current_auras[DENDRO] != [0, 0]:
                application = False
                reactions = self.__burning(reactions, DENDRO, PYRO, gu)
                return reactions
            if self.current_auras[QUICKEN] != [0, 0]:
                application = False
                reactions = self.__burning(reactions, QUICKEN, PYRO, gu)
                return reactions
            if application:
                self.__pure_application(PYRO, gu)

        elif element == GEO:
            if self.current_auras[FROZEN] != [0, 0]:
                reactions.append([SHATTER, 1.5, 1, None, None])
                self.current_auras[FROZEN] = [0, 0]
            if self.current_auras[ELECTRO] != [0, 0]:
                reactions.append([ELECTRO_CRYSTALLIZE, 0, 0, None, None])
                gu = self.__cristallize(ELECTRO, gu)
                if gu == 0:
                    return reactions
            if self.current_auras[PYRO] != [0, 0]:
                reactions.append([PYRO_CRYSTALLIZE, 0, 0, None, None])
                gu = self.__cristallize(PYRO, gu)
                if gu == 0:
                    return reactions
            if self.current_auras[HYDRO] != [0, 0]:
                reactions.append([HYDRO_CRYSTALLIZE, 0, 0, None, None])
                gu = self.__cristallize(HYDRO, gu)
                if gu == 0:
                    return reactions
            if self.current_auras[CRYO] != [0, 0]:
                reactions.append([CRYO_CRYSTALLIZE, 0, 0, None, None])
                gu = self.__cristallize(CRYO, gu)
                if gu == 0:
                    return reactions
        return reactions

    def __burning(self, reactions:List, aura:str, trigger:str, trigger_gu:float):
        from src.entities.summons_and_adaptives.reaction_summons import Burning
        if self.current_auras[trigger] != [0, 0]:
            if self.current_auras[trigger][0] < trigger_gu:
                self.current_auras[trigger][0] = 0.8*trigger_gu
                if trigger == PYRO:
                    self.current_auras[PYRO][1] = 1 / (35/(4*trigger_gu) + 25/8)
            reactions.append([BURNING, 0, 0, None, None])
        elif trigger == PYRO and self.current_auras[BURNING] != [0, 0]:
            reactions.append([BURNING, 0, 0, None, None])
            self.current_auras[trigger][0] = 0.8*trigger_gu
            self.current_auras[PYRO][1] = 1 / (35/(4*trigger_gu) + 25/8)
        else:
            self.current_auras[trigger][0] = 0.8*trigger_gu
            self.current_auras[trigger][1] = 1 / (35/(4*trigger_gu) + 25/8)
            self.current_auras[BURNING] = [2, 0]
            self.current_auras[PYRO] = [1, 1 / (35/4 + 25/8)]
            self.current_auras[DENDRO][0] -= 0.1
            # Quicken and dendro are consumed simultaneously
            if self.current_auras[QUICKEN] != [0, 0]:
                self.current_auras[QUICKEN][0] -= 0.1
                if self.current_auras[QUICKEN][0] < 0:
                    self.current_auras[QUICKEN] = [0, 0]
            if self.current_auras[DENDRO][0] <= 0:
                self.current_auras[DENDRO] = [0, 0]
            reactions.append([BURNING, 0.25, 1, Burning(self), None])
        return reactions

    def __electro_charged(self, reactions:List, aura:str, trigger:str, trigger_gu:float):
        from src.entities.summons_and_adaptives.reaction_summons import ElectroCharged
        if self.current_auras[trigger] != [0, 0]:
            if self.current_auras[trigger][0] < trigger_gu:
                self.current_auras[trigger][0] = 0.8*trigger_gu
            reactions.append([ELECTRO_CHARGED, 0, 0, None, None])
        else:
            self.current_auras[trigger][0] = 0.8*trigger_gu
            self.current_auras[trigger][1] = 1 / (35/(4*trigger_gu) + 25/8)
            self.current_auras[aura][0] -= 0.4
            self.current_auras[trigger][0] -= 0.4
            if self.current_auras[trigger][0] <= 0:
                self.current_auras[trigger] = [0, 0]
            if self.current_auras[aura][0] <= 0:
                self.current_auras[aura] = [0, 0]
            reactions.append([ELECTRO_CHARGED, 1.2, 1, ElectroCharged(self), None])
        return reactions

    def __consume_aura(self, aura:str, trigger_gu:float, reaction_multiplier:float):
        if self.current_auras[aura][0] <= reaction_multiplier*trigger_gu:
            trigger_gu = (reaction_multiplier*trigger_gu - self.current_auras[aura][0]) * 1/reaction_multiplier
            self.current_auras[aura] = [0, 0]
        else:
            self.current_auras[aura][0] -= reaction_multiplier*trigger_gu
            trigger_gu = 0
        return trigger_gu

    def __cristallize(self, aura:str, trigger_gu:float):
        if 0.5*trigger_gu >= self.current_auras[aura][0]:
            trigger_gu = (0.5*trigger_gu - self.current_auras[aura][0])*2
            self.current_auras[aura] = [0, 0]
        else:
            self.current_auras[aura][0] -= 0.5 * trigger_gu
            trigger_gu = 0
        return trigger_gu

    def __swirl(self, reactions:List, aura:str, trigger_gu:float):
        if aura == BURNING:
            cap = PYRO
        elif aura == FROZEN:
            cap = CRYO
        else:
            cap = aura
        if 0.5*trigger_gu >= self.current_auras[aura][0]:
            reactions.append(["{} swirl".format(cap), 0.6, 1, None, [cap, (self.current_auras[aura][0] - 0.04) * 1.25 + 1]])
            trigger_gu = (0.5*trigger_gu - self.current_auras[aura][0])*2
            self.current_auras[aura] = [0, 0]
        else:
            reactions.append(["{} swirl".format(cap), 0.6, 1, None, [cap, (trigger_gu - 0.04) * 1.25 + 1]])
            self.current_auras[aura][0] -= 0.5 * trigger_gu
            trigger_gu = 0
        return reactions, trigger_gu

    def __freeze(self, aura:str, trigger_gu:float):
        frozen_gu = 2 * min(self.current_auras[aura][0], trigger_gu)
        frozen_duration = 2 * pow(5*frozen_gu + 4, 1/2) - 4
        if frozen_gu > self.current_auras[FROZEN][0]:
            self.current_auras[FROZEN][0] = frozen_gu
            self.current_auras[FROZEN][1] = frozen_gu / frozen_duration
        return self.__consume_aura(aura, trigger_gu, 1)

    def __quicken(self, aura:str, trigger_gu:float):
        quicken_gu = min(self.current_auras[aura][0], trigger_gu)
        quicken_duration = 5 * quicken_gu + 6
        if quicken_gu > self.current_auras[QUICKEN][0]:
            self.current_auras[QUICKEN][0] = quicken_gu
            self.current_auras[QUICKEN][1] = quicken_gu / quicken_duration
        return self.__consume_aura(aura, trigger_gu, 1)

    def __pure_application(self, element:str, gu:float):
        if self.current_auras[element] != [0, 0]:
            if self.current_auras[element][0] < 0.8*gu:
                self.current_auras[element][0] = 0.8*gu
                if element == PYRO:
                    self.current_auras[element][1] = 1 / (35/(4*gu) + 25/8)
        else:
            self.current_auras[element][0] = 0.8*gu
            self.current_auras[element][1] = 1 / (35/(4*gu) + 25/8)