from character import Character, Trait
from consts import EventType


class Event:
    def __init__(self, char1: Character, char2: Character, trait: Trait):
        self.char1 = char1
        self.char2 = char2
        self.type = EventType.random()
        self.trait = trait

    def info(self):
        """
        显示事件详情
        """
        verb1 = '+'
        verb2 = '+'
        char1_difference, char2_difference, detail = self.process_event()
        if char1_difference < 0:
            verb1 = '-'
            descriptor1 = ", %s的%s %s%d" % \
                          (self.char1.name, self.char1.trait_info(self.trait), verb1, 0-char1_difference)
        elif char1_difference > 0:
            descriptor1 = ", %s的%s %s%d" % \
                          (self.char1.name, self.char1.trait_info(self.trait), verb1, char1_difference)
        else:
            descriptor1 = ""
        if char2_difference < 0:
            verb2 = '-'
            descriptor2 = ", %s的%s %s%d" % \
                          (self.char2.name, self.char2.trait_info(self.trait), verb2, 0-char2_difference)
        elif char2_difference > 0:
            descriptor2 = ", %s的%s %s%d" % \
                          (self.char2.name, self.char2.trait_info(self.trait), verb2, char2_difference)
        else:
            descriptor2 = ""
        info = "%s和%s触发了【%s事件】: %s%s%s\r\n" % \
               (self.char1.name, self.char2.name, self.type.value, detail,
                descriptor1, descriptor2)
        print(info)

        if char1_difference != 0:
            origin_tag = self.char1.tag_info()
            self.char1.refresh_behavior()
            if self.char1.tag_info() != origin_tag:
                cypher = "【%s】性格从%s变为%s\r\n" % \
                         (self.char1.name, origin_tag, self.char1.tag_info())
                print(cypher)
        if char2_difference != 0:
            origin_tag = self.char2.tag_info()
            self.char2.refresh_behavior()
            if self.char2.tag_info() != origin_tag:
                cypher = "【%s】性格从%s变为%s\r\n" % \
                         (self.char2.name, origin_tag, self.char2.tag_info())
                print(cypher)

    def process_event(self):
        """
        处理事件碰撞
        :return: char1, char2
        """
        if self.type is EventType.POSITIVE_SUM:
            """
            正和博弈（一起玩耍、一起学习）
                情况1：一人得利    ->  Harm && Harmed
                情况2：两人得利    
            """
            if self.char2.will_harm() and self.char1.will_be_harmed():
                return 0, self.char2.inc_trait(self.trait) + self.char2.inc_trait(self.trait), \
                       "%s独占了所有利益" % self.char2.name
            elif self.char1.will_harm() and self.char2.will_be_harmed():
                return self.char1.inc_trait(self.trait) + self.char1.inc_trait(self.trait), 0, \
                       "%s独占了所有利益" % self.char1.name
            else:
                return self.char1.inc_trait(self.trait), self.char2.inc_trait(self.trait), \
                       "两人共享了利益"
        elif self.type is EventType.NEGATIVE_SUM:
            """
            负和博弈（一起闯祸，散布谣言）
                情况1：一人受害    ->  Harm && Harmed
                情况2：两人一起受害
            """
            if self.char2.will_harm() and self.char1.will_be_harmed():
                return 0, self.char2.dec_trait(self.trait) + self.char2.dec_trait(self.trait), \
                       "%s出卖了%s，只有%s受罚" % (self.char1.name, self.char2.name, self.char2.name)
            elif self.char1.will_harm() and self.char2.will_be_harmed():
                return self.char1.dec_trait(self.trait) + self.char1.dec_trait(self.trait), 0, \
                       "%s出卖了%s，只有%s受罚" % (self.char2.name, self.char1.name, self.char1.name)
            else:
                return self.char1.dec_trait(self.trait), self.char2.dec_trait(self.trait), \
                       "两人共同承担，一起受罚"
        elif self.type is EventType.ZERO_SUM:
            """
            零和博弈（比赛，权/钱/名利）
                情况1：一人得利一人受害    -> Harm && Harmed
                情况2：两人无人得利
            """
            if self.char2.will_harm() and self.char1.will_be_harmed():
                return self.char1.dec_trait(self.trait), self.char2.inc_trait(self.trait), \
                       "%s伤害了%s，%s获利，%s受罚" % \
                       (self.char2.name, self.char1.name, self.char2.name, self.char1.name)
            elif self.char1.will_harm() and self.char2.will_be_harmed():
                return self.char1.inc_trait(self.trait), self.char2.dec_trait(self.trait), \
                       "%s伤害了%s，%s获利，%s受罚" % \
                       (self.char1.name, self.char2.name, self.char1.name, self.char2.name)
            else:
                return 0, 0, \
                       "两人相安无事，无事发生"
        elif self.type is EventType.PRISONER:
            """
            囚徒困境
                情况1：两人得利 -> ~Harm && ~Harm
                情况2：一人得利一人受害 -> Harm && ~ Harm
                情况3：无人得利 -> Harm && Harm
            """
            if not self.char1.will_harm() and not self.char2.will_harm():
                return self.char1.inc_trait(self.trait), self.char2.inc_trait(self.trait), \
                       "两人携手互助，共渡难关"
            elif self.char2.will_harm() and not self.char1.will_harm():
                return self.char1.dec_trait(self.trait), self.char2.inc_trait(self.trait), \
                       "%s背叛了%s, %s获利，%s受罚" % \
                       (self.char2.name, self.char1.name, self.char2.name, self.char1.name)
            elif self.char1.will_harm() and not self.char2.will_harm():
                return self.char1.inc_trait(self.trait), self.char2.dec_trait(self.trait), \
                       "%s背叛了%s, %s获利，%s受罚" % \
                       (self.char1.name, self.char2.name, self.char1.name, self.char2.name)
            else:
                return 0, 0, "两人同时背叛了对方，无人获利"
        elif self.type is EventType.RESCUE:
            """
            救援（1遇险，2可选择是否救人）
                情况1：救    -> 2.Save
                情况2：不救  -> 2.~Save
            """
            self.trait = Trait.KINDNESS
            if self.char2.will_save():
                return self.char1.inc_trait(self.trait), 0, \
                       "%s遇险，%s伸出了援手" % (self.char1.name, self.char2.name)
            else:
                return self.char1.dec_trait(self.trait), 0, \
                       "%s遇险，%s看到了但没有救" % (self.char1.name, self.char2.name)
