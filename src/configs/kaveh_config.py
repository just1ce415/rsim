from src.configs.base_config import BaseConfig

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
        super()._initialize_rotation(self)

    def initialize_artifacts(self):
        kaveh, fischl, xingqiu, yaemiko = self.team
        kaveh_er, fisch_er, xingqui_er, yaemiko_er = self.target_ers
        kaveh_mv_params, fischl_mv_params, xingqui_mv_params, yaemiko_mv_params = self.mv_params

        # Artifacts
        total_stat_value = 70 # between 0 and 100
        kaveh_stat_value_distribution = kaveh.get_stat_value_distribution(kaveh_mv_params)
        kaveh_flower, kaveh_feather, kaveh_sands, kaveh_goblet, kaveh_circlet = ArtifactGenerator().generate_set_by_stat_value(
            total_stat_value=total_stat_value, stat_value_distribution=kaveh_stat_value_distribution, art_set=(DeepwoodMemories),
            sands_main_stat="ATK%", goblet_main_stat="Dendro DMG Bonus", circlet_main_stat="CR", target_er=kaveh_er
        )
        kaveh.equip_flower(kaveh_flower)
        kaveh.equip_feather(kaveh_feather)
        kaveh.equip_sands(kaveh_sands)
        kaveh.equip_goblet(kaveh_goblet)
        kaveh.equip_circlet(kaveh_circlet)
        
        fischl_stat_value_distribution = fischl.get_stat_value_distribution(fischl_mv_params)
        fischl_flower, fischl_feather, fischl_sands, fischl_goblet, fischl_circlet = ArtifactGenerator().generate_set_by_stat_value(
            total_stat_value=total_stat_value, stat_value_distribution=fischl_stat_value_distribution, art_set=(ThunderingFury, GladiatorFinale),
            sands_main_stat="EM", goblet_main_stat="Electro DMG Bonus", circlet_main_stat="CR", target_er=fisch_er
        )
        fischl.equip_flower(fischl_flower)
        fischl.equip_feather(fischl_feather)
        fischl.equip_sands(fischl_sands)
        fischl.equip_goblet(fischl_goblet)
        fischl.equip_circlet(fischl_circlet)

        xingqiu_stat_value_distribution = xingqiu.get_stat_value_distribution(xingqui_mv_params)
        xingqiu_flower, xingqiu_feather, xingqiu_sands, xingqiu_goblet, xingqiu_circlet = ArtifactGenerator().generate_set_by_stat_value(
            total_stat_value=total_stat_value, stat_value_distribution=xingqiu_stat_value_distribution, art_set=(Emblem),
            sands_main_stat="EM", goblet_main_stat="Electro DMG Bonus", circlet_main_stat="CR", target_er=xingqui_er
        )
        xingqiu.equip_flower(xingqiu_flower)
        xingqiu.equip_feather(xingqiu_feather)
        xingqiu.equip_sands(xingqiu_sands)
        xingqiu.equip_goblet(xingqiu_goblet)
        xingqiu.equip_circlet(xingqiu_circlet)

        yaemiko_stat_value_distribution = yaemiko.get_stat_value_distribution(yaemiko_mv_params)
        yaemiko_flower, yaemiko_feather, yaemiko_sands, yaemiko_goblet, yaemiko_circlet = ArtifactGenerator().generate_set_by_stat_value(
            total_stat_value=total_stat_value, stat_value_distribution=yaemiko_stat_value_distribution, art_set=(GuildedDreams),
            sands_main_stat="EM", goblet_main_stat="Electro DMG Bonus", circlet_main_stat="CR", target_er=yaemiko_er
        )
        yaemiko.equip_flower(yaemiko_flower)
        yaemiko.equip_feather(yaemiko_feather)
        yaemiko.equip_sands(yaemiko_sands)
        yaemiko.equip_goblet(yaemiko_goblet)
        yaemiko.equip_circlet(yaemiko_circlet)

        self.team = [kaveh, fischl, xingqiu, yaemiko]
