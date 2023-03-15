from src.configs.base_config import BaseConfig
from src.entities.artifacts.flower import Flower
from src.entities.artifacts.feather import Feather
from src.entities.artifacts.sands import Sands
from src.entities.artifacts.goblet import Goblet
from src.entities.artifacts.circlet import Circlet
from src.entities.artifacts.artifact_generator import ArtifactGenerator

class KavehConfig(BaseConfig):
    def __init__(self):
        super().__init__(self)
        self._initialize_characters()
        self._initialize_rotation()

    def _initialize_characters(self):
        # 1st character in the team
        kaveh = Kaveh(constallation=0) # for now always lvl 90, talent lvls 9-9-9
        kaveh.equip_weapon(Aquamarine(refinement=5)) # for now always 90 lvl

        # 2nd character
        fischl = Fischl(constallation=4)
        fischl.equip_weapon(Stringless(refinement=5)) # for now always 90 lvl

        # 3rd character
        xingqiu = Xingqiu(constallation=4)
        xingqiu.equip_weapon(SacrificialSword(refinement=5)) # for now always 90 lvl

        # 4th character
        yaemiko = YaeMiko(constallation=0)
        yaemiko.equip_weapon(Widsith(refinement=5)) # for now always 90 lvl

        self.team = [kaveh, fischl, xingqiu, yaemiko]


    def _initialize_rotation(self):
        kaveh, fischl, xingqiu, yaemiko = self.team
        # Rotation
        self.rotation = [
            xingqiu.swap(),
            xingqiu.elemental_burst(),
            xingqiu.normal_attack(N=1),
            xingqiu.elemental_skill(),
            xingqiu.elemental_skill(),
            fischl.swap(),
            fischl.elemental_skill(),
            fischl.normal_attack(N=1),
            yaemiko.swap(),
            yaemiko.elemental_skill(),
            yaemiko.elemental_skill(),
            yaemiko.elemental_skill(),
            yaemiko.normal_attack(N=1),
            kaveh.swap(),
            kaveh.elemental_skill(),
            kaveh.elemental_burst(),
            kaveh.normal_attack(N=4),
            kaveh.normal_attack(N=4),
            kaveh.elemental_skill(),
            kaveh.normal_attack(N=4),
            yaemiko.swap(),
            yaemiko.normal_attack(N=1),
            yaemiko.elemetal_burst(),
            kaveh.elemental_skill()
        ]

    def initialize_artifacts(self):
        kaveh, fischl, xingqiu, yaemiko = self.team
        kaveh_er_info = self.er_info[kaveh]
        fischl_er_info = self.er_info[fischl]
        xingqiu_er_info = self.er_info[xingqiu]
        yaemiko_er_info = self.er_info[yaemiko]
        kaveh_dmg_info = self.dmg_info[kaveh]
        fischl_dmg_info = self.dmg_info[fischl]
        xingqiu_dmg_info = self.dmg_info[xingqiu]
        yaemiko_dmg_info = self.dmg_info[yaemiko]

        # Artifacts
        stat_value = 70 # between 0 and 100
        kaveh_flower, kaveh_feather, kaveh_sands, kaveh_goblet, kaveh_circlet = ArtifactGenerator(
            flower=Flower(set_bonus=DeepwoodMemories), feather=Feather(set_bonus=DeepwoodMemories),
            sands=Sands(set_bonus=DeepwoodMemories, main_em=True),
            goblet=Goblet(set_bonus=DeepwoodMemories, main_dendro_dmg_bonus=True),
            circlet=Circlet(set_bonus=DeepwoodMemories, main_cr=True)
        ).generate_substats_by_stat_value(
            stat_value=stat_value, dmg_info=kaveh_dmg_info, er_info=kaveh_er_info
        )
        kaveh.equip_flower(kaveh_flower)
        kaveh.equip_feather(kaveh_feather)
        kaveh.equip_sands(kaveh_sands)
        kaveh.equip_goblet(kaveh_goblet)
        kaveh.equip_circlet(kaveh_circlet)
        
        fischl_flower, fischl_feather, fischl_sands, fischl_goblet, fischl_circlet = ArtifactGenerator(
            flower=Flower(set_bonus=ThunderingFury), feather=Feather(set_bonus=ThunderingFury),
            sands=Sands(set_bonus=ThunderingFury, main_em=True),
            goblet=Goblet(set_bonus=GladiatorFinale, main_electro_dmg_bonus=True),
            circlet=Circlet(set_bonus=GladiatorFinale, main_cr=True)
        ).generate_substats_by_stat_value(
            stat_value=stat_value, dmg_info=fischl_dmg_info, er_info=fischl_er_info
        )
        fischl.equip_flower(fischl_flower)
        fischl.equip_feather(fischl_feather)
        fischl.equip_sands(fischl_sands)
        fischl.equip_goblet(fischl_goblet)
        fischl.equip_circlet(fischl_circlet)

        xingqiu_flower, xingqiu_feather, xingqiu_sands, xingqiu_goblet, xingqiu_circlet = ArtifactGenerator(
            flower=Flower(set_bonus=Emblem), feather=Feather(set_bonus=Emblem),
            sands=Sands(set_bonus=Emblem, main_atk_percent=True),
            goblet=Goblet(set_bonus=Emblem, main_hydro_dmg_bonus=True),
            circlet=Circlet(set_bonus=Emblem, main_cr=True)
        ).generate_substats_by_stat_value(
            stat_value=stat_value, dmg_info=xingqiu_dmg_info, er_info=xingqiu_er_info
        )
        xingqiu.equip_flower(xingqiu_flower)
        xingqiu.equip_feather(xingqiu_feather)
        xingqiu.equip_sands(xingqiu_sands)
        xingqiu.equip_goblet(xingqiu_goblet)
        xingqiu.equip_circlet(xingqiu_circlet)

        yaemiko_flower, yaemiko_feather, yaemiko_sands, yaemiko_goblet, yaemiko_circlet = ArtifactGenerator(
            flower=Flower(set_bonus=GuildedDreams), feather=Feather(set_bonus=GuildedDreams),
            sands=Sands(set_bonus=GuildedDreams, main_em=True),
            goblet=Goblet(set_bonus=GuildedDreams, main_electro_dmg_bonus=True),
            circlet=Circlet(set_bonus=GuildedDreams, main_cr=True)
        ).generate_substats_by_stat_value(
            stat_value=stat_value, dmg_info=yaemiko_dmg_info, er_info=yaemiko_er_info
        )
        yaemiko.equip_flower(yaemiko_flower)
        yaemiko.equip_feather(yaemiko_feather)
        yaemiko.equip_sands(yaemiko_sands)
        yaemiko.equip_goblet(yaemiko_goblet)
        yaemiko.equip_circlet(yaemiko_circlet)

        self.team = [kaveh, fischl, xingqiu, yaemiko]
